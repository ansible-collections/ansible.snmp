# (c) 2021 Red Hat Inc.
# (c) 2021 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.plugins.action import ActionBase
from ansible_collections.ansible.snmp.plugins.plugin_utils.snmp_wrapper import (
    SnmpConfiguration,
    Snmpv2cConnection,
    SnmpInstance,
)
from ansible_collections.ansible.snmp.plugins.modules.walk import (
    DOCUMENTATION,
)

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)



class ActionModule(ActionBase):
    """action module"""

    def _check_argspec(self):
        aav = AnsibleArgSpecValidator(
            data=self._task.args,
            schema=DOCUMENTATION,
            schema_format="doc",
            name=self._task.action,
        )
        valid, errors, self._task.args = aav.validate()
        if not valid:
            self._result["failed"] = True
            self._result["msg"] = errors

    def run(self, tmp=None, task_vars=None):
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._task_vars = task_vars

        self._check_argspec()
        if self._result.get("failed"):
            return self._result

        host = self.get_connection_option('host')
        port = self.get_connection_option("port")
        if self._connection.transport == "v2":
            community = self.get_connection_option("community")
            connection = Snmpv2cConnection(
                dest_host=host, community=community, timeout=50000000
            )

        configuration = SnmpConfiguration(
            best_guess=self._task.args["best_guess"],
            use_enums=self._task.args["enums"],
            use_long_names=self._task.args["long_names"],
            use_numeric=self._task.args['numeric'],
            use_sprint_value=self._task.args["sprint_value"],

        )

        instance = SnmpInstance(
            connection=connection, configuration=configuration
        )
        instance.set_oids(self._task.args["oids"])

        error, elapsed, result = instance.walk()

        self._result.update({"changed": False})

        if error:
            self._result.update(
                {"failed": True, "msg": error}
            )
        else:
            self._result.update({"elapsed": elapsed, "result": result})
        
        return self._result
