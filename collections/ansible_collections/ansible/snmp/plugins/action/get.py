# (c) 2021 Red Hat Inc.
# (c) 2021 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.plugins.action import ActionBase
from ansible_collections.ansible.snmp.plugins.plugin_utils.snmp_wrapper import (
    SnmpConfiguration,
    Snmpv2cConnection,
    SnmpInstance,
)


class ActionModule(ActionBase):
    """action module"""

    def run(self, tmp=None, task_vars=None):
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._task_vars = task_vars
        host = self.get_connection_option('host')
        port = self.get_connection_option("port")
        use_enums = self._task.args["use_enums"]
        use_sprint_value = self._task.args["use_sprint_value"]
        if self._connection.transport == "v2":
            community = self.get_connection_option("community")
            connection = Snmpv2cConnection(
                dest_host=host, community=community, timeout=50000000
            )

        configuration = SnmpConfiguration(
            use_enums=self._task.args["use_enums"],
            use_sprint_value=self._task.args["use_sprint_value"],
        )

        instance = SnmpInstance(
            connection=connection, configuration=configuration
        )
        instance.set_oids(self._task.args["oids"])

        error, elapsed, result = instance.get()

        self._result.update({"changed": False})

        if error:
            self._result.update(
                {"failed": True, "msg": error}
            )
        else:
            self._result.update({"elapsed": elapsed, "result": result})
        
        return self._result
