# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The base class for SNMP connections
"""

from __future__ import absolute_import, division, print_function

# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from typing import Dict
from typing import List

from ansible.plugins.connection import ConnectionBase, ensure_connect
from ansible.module_utils.basic import missing_required_lib

from ansible.errors import AnsibleError
from ansible.utils.display import Display

# pylint: disable=import-error

from .netsnmp_defs import SnmpConfiguration
from .netsnmp_defs import SnmpResponse

from .netsnmp_instance import SnmpInstance
from .netsnmp_instance import HAS_NETSNMP

# pylint: enable=import-error


class SnmpConnectionBase(ConnectionBase):
    """The base class for SNMP connections"""

    transport = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._connection: SnmpConnectionBase
        self._configuration: SnmpConfiguration
        self._display = Display()
        self._instance: SnmpInstance
        self._oids: List
        if not HAS_NETSNMP:
            msg = "python bindings for netsnmp "
            msg += (
                "(See the README for the ansible.snmp collection for details."
            )
            raise AnsibleError(missing_required_lib(msg))

    def _connect(self) -> None:
        """Make the connection

        Note: We never set self._connected true because the netsnmp session cannont be reused
        this forces task executor to create a new connection for every task, or looped task
        """
        if not self._connected:
            for param in self._connection.set:
                setattr(self._connection, param, self.get_option(param))

            for param in self._connection.not_set:
                value = self.get_option(param)
                if value is not None:
                    setattr(self._connection, param, value)
            host = self._play_context.remote_addr
            version = self.get_option("version")
            self._display.vvv(
                f"ESTABLISHED SNMP v{version} CONNECTION: {host}"
            )

        self._instance = SnmpInstance(
            connection=self._connection,
            configuration=self._configuration,
        )
        self._instance.set_oids(self._oids)

        return self

    def close(self) -> None:
        if self._connected:
            host = self._play_context.remote_addr
            version = self.get_option("version")
            self._display.vvv(f"CLOSED SNMP v{version} CONNECTION: {host}")
            self._connected = False

    def exec_command(self, cmd, in_data=None, sudoable=True):
        pass

    def fetch_file(self, in_path, out_path):
        pass

    def put_file(self, in_path, out_path):
        pass

    def configure(self, task_args: Dict) -> None:
        """Confgiure the SNMP connection

        :param task_args: The args passed to the task
        :type task_args: dict
        """
        self._configuration = SnmpConfiguration()

        for param in self._configuration.set:
            if param in task_args:
                setattr(self._configuration, param, task_args[param])

        for param in self._configuration.not_set:
            if param in task_args:
                value = task_args[param]
                if value is not None:
                    setattr(self._configuration, param, value)

        self._oids = []
        for entry in task_args["oids"]:
            _entry = {}
            _entry["tag"] = entry["oid"]
            if "iid" in entry:
                _entry["iid"] = entry["iid"]
            if "value" in entry:
                _entry["val"] = entry["value"]
            if "type" in entry:
                _entry["type_arg"] = entry["type"]
            self._oids.append(_entry)

    @ensure_connect
    def get(self) -> SnmpResponse:
        """Perform the SNMP get"""
        return self._instance.get()

    @ensure_connect
    def set(self) -> SnmpResponse:
        """Perform the SNMP set"""
        return self._instance.set()

    @ensure_connect
    def walk(self) -> SnmpResponse:
        """Perform the SNMP walk"""
        return self._instance.walk()
