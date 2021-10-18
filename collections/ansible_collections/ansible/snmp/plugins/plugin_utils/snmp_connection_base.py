from typing import List

from ansible.plugins.connection import ConnectionBase, ensure_connect
from ansible.utils.display import Display

from .netsnmp_wrapper import (
    SnmpConfiguration,
    SnmpInstance,
)

display = Display()


class SnmpConnectionBase(ConnectionBase):
    def __init__(self, *args, **kwargs):
        super(SnmpConnectionBase, self).__init__(*args, **kwargs)
        self._connection: SnmpConnectionBase
        self._configuration: SnmpConfiguration
        self._oids: List
    
    def _connect(self):
        self._instance = SnmpInstance(
            connection=self._connection, configuration=self._configuration
        )
        self._instance.set_oids(self._oids)
        if not self._connected:
            display.vvv(u"ESTABLISHED SNMPv2c CONNECTION: {host}".format(host=self._play_context.remote_addr))
        if not self._connected:
            self._connected = True
        return self


    def close(self):
        if self._connected:
            display.vvv(u"CLOSED SNMPv2c CONNECTION: {host}".format(host=self._play_context.remote_addr))
        self._connected = False

    def exec_command(self, cmd, in_data=None, sudoable=True):
        pass

    def fetch_file(self, in_path, out_path):
        pass
    
    def put_file(self, in_path, out_path):
        pass

    def configure(self, task_args):
        self._configuration = SnmpConfiguration(
            best_guess=task_args["best_guess"],
            use_enums=task_args["enums"],
            use_long_names=task_args["long_names"],
            use_numeric=task_args['numeric'],
            use_sprint_value=task_args["sprint_value"],
        )
        self._oids = task_args["oids"]

    @ensure_connect
    def get(self):
        return self._instance.get()
    
    @ensure_connect
    def walk(self):
        return self._instance.walk()
    

    
    

    

