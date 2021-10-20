# (c) 2021 Red Hat Inc.
# (c) 2021 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible_collections.ansible.snmp.plugins.modules.get import (
    DOCUMENTATION,
)

from ansible_collections.ansible.snmp.plugins.plugin_utils.snmp_action_base import (
    SnmpActionBase,
)


class ActionModule(SnmpActionBase):
    """action module"""

    def run(self, tmp=None, task_vars=None):
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._task_vars = task_vars

        self._check_argspec(DOCUMENTATION)
        if self._result.get("failed"):
            return self._result
        
        self._result.update({'elapsed': {"total": 0}})
        self._result.update({"changed": False})


        self._connection.configure(self._task.args)
        error, elapsed, result = self._connection.get()
        self._result['elapsed']['get'] = elapsed
        self._result['elapsed']['total'] += elapsed


        if error:
            self._result.update({"failed": True, "msg": error})
        else:
            self._result.update({"result": result})

        return self._result
