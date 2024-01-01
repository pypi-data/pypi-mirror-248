import logging
from typing import Dict, Any, List, Optional
import json

import click

from .unix_user import UnixUser
from ..process_utils import (
    run_process,
    run_process_single_result,
    process_output_as_json
)
from ..platform_utils import is_linux


logger = logging.getLogger(__name__)


class DockerDaemonInfo(object):
    def __init__(self, docker_host: Optional[str] = ''):
        self._docker_host = docker_host
        self._info = self._read_daemon_info(docker_host)
        self._user_info = UnixUser()

    def is_rootless(self) -> bool:
        """
        Detects rootless docker security option
        :return: boolean of rootless or not
        """
        if 'SecurityOptions' not in self._info:
            click.echo("Unable to determine docker security options. Is the daemon running properly?")
            raise click.Abort()

        sec_options = self._info['SecurityOptions']
        if sec_options:
            for opt in sec_options:
                if 'rootless' in opt:
                    return True
        return False

    def docker_socket(self) -> str:
        """
        Returns the path to the Docker socket
        :return:
        """
        if is_linux():
            if self.is_rootless():
                return f'/var/run/user/{self._user_info.uid}/docker.sock'
            else:
                return '/var/run/docker.sock'
        else:
            return '/var/run/docker.sock.raw'

    def docker_internal_socket(self) -> str:
        """
        Returns the path to the Docker socket that should be use when launching
        containers from inside the CLI that need to mount the docker socket
        :return:
        """
        if self.is_rootless():
            return f'/var/run/user/{self._user_info.uid}/docker.sock'
        else:
            return '/var/run/docker.sock'

    def network_exists(self, network_name: str) -> bool:
        for net in self._read_networks(self._docker_host):
            if network_name == net['Name']:
                return True
        return False

    def create_network(self, network_name: str) -> None:
        """
        Creates a bridged network
        :return: None
        """
        if not self.network_exists(network_name):
            logger.info(f'Creating network: {network_name}')
            rs = run_process(f'docker network create {network_name}')
            for line in rs:
                logger.debug(line)
        else:
            logger.warning(f'Network {network_name} already exists')

    @property
    def info(self) -> Dict[str, Any]:
        return self._info

    @property
    def containers(self) -> Optional[List[Dict[str, Any]]]:
        cont = self._read_containers(self._docker_host)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Docker containers:')
            for c in cont:
                logger.debug(c)
        return cont

    @property
    def networks(self) -> Optional[List[Dict[str, Any]]]:
        nets = self._read_networks(self._docker_host)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Docker networks:')
            for n in nets:
                logger.debug(n)
        return nets

    @classmethod
    def build(cls) -> 'DockerDaemonInfo':
        return DockerDaemonInfo()

    @classmethod
    def build_with_docker_host(cls, docker_host: str) -> 'DockerDaemonInfo':
        return DockerDaemonInfo(docker_host=docker_host)

    @staticmethod
    def _read_daemon_info(docker_host: Optional[str] = '') -> Dict[str, Any]:
        """
        Returns the output of `docker info` as a dictionary
        :return:
        """
        env = None
        if docker_host:
            env = {'DOCKER_HOST': docker_host}
        info_str = run_process_single_result('docker info --format "{{json .}}"', env)
        return json.loads(info_str)

    @staticmethod
    def _read_containers(docker_host: Optional[str] = '') -> Optional[List[Dict[str, Any]]]:
        env = None
        if docker_host:
            env = {'DOCKER_HOST': docker_host}
        rs = run_process('docker container ls -a --format "{{json .}}"', env)
        return process_output_as_json(rs)

    @staticmethod
    def _read_networks(docker_host: Optional[str] = '') -> Optional[List[Dict[str, Any]]]:
        env = None
        if docker_host:
            env = {'DOCKER_HOST': docker_host}
        rs = run_process('docker network ls --format "{{json .}}"', env)
        return process_output_as_json(rs)


