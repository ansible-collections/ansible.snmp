from typing import List

from ansible.plugins.connection import ConnectionBase, ensure_connect
from ansible.module_utils.basic import missing_required_lib

from ansible.errors import AnsibleError
from ansible.utils.display import Display

try:
    from .netsnmp_wrapper import (
        SnmpConfiguration,
        SnmpInstance,
    )

    HAS_NETSNMP = True
except ImportError:
    HAS_NETSNMP = False

display = Display()


class SnmpConnectionBase(ConnectionBase):
    def __init__(self, *args, **kwargs):
        super(SnmpConnectionBase, self).__init__(*args, **kwargs)
        self._connection: SnmpConnectionBase
        self._configuration: SnmpConfiguration
        self._oids: List
        if not HAS_NETSNMP:
            raise AnsibleError(
                missing_required_lib(
                    "python bindings for netsnmp (See the README for the ansible.snmp collection for details.)"
                )
            )

    def _connect(self):
        """ Make the connection
        
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
            display.vvv(
                u"ESTABLISHED SNMP v{version} CONNECTION: {host}".format(
                    host=self._play_context.remote_addr,
                    version=self.get_option("version"),
                )
            )

        self._instance = SnmpInstance(
            connection=self._connection,
            configuration=self._configuration,
        )
        self._instance.set_oids(self._oids)

        return self

    def close(self):
        if self._connected:
            display.vvv(
                u"CLOSED SNMP v{version} CONNECTION: {host}".format(
                    host=self._play_context.remote_addr,
                    version=self.get_option("version"),
                )
            )
            self._connected = False

    def exec_command(self, cmd, in_data=None, sudoable=True):
        pass

    def fetch_file(self, in_path, out_path):
        pass

    def put_file(self, in_path, out_path):
        pass

    def configure(self, task_args):
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
    def get(self):
        return self._instance.get()

    @ensure_connect
    def set(self):
        return self._instance.set()

    @ensure_connect
    def walk(self):
        return self._instance.walk()
