# (c) 2021 Red Hat Inc.
# (c) 2021 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from copy import deepcopy

from ansible_collections.ansible.snmp.plugins.modules.set import (
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

    
        # pre set get
        # Note: although we are doing a get, the netsnmp varbind _can_ have values
        # they are disregarded when doing a get
        self._connection.configure(self._task.args)
        error, elapsed, pre_set_result = self._connection.get()
        self._result['elapsed']['pre_set_get'] = elapsed
        self._result['elapsed']['total'] += elapsed

        if error:
            final_error = f"SNMP get (pre-set)failed. The error was: '{error}'"
            self._result.update({"failed": True, "msg": final_error})
            return self._result
        else:
            self._result.update({"before": pre_set_result})
        # close the connection, because the netsnmp session cannot be reused
        self._connection.close()


        # set
        self._connection.configure(self._task.args)
        error, elapsed = self._connection.set()
        self._result['elapsed']['set'] = elapsed
        self._result['elapsed']['total'] += elapsed

        if error:
            final_error = f"SNMP set failed. The error was: '{error}'"
            self._result.update({"failed": True, "msg": final_error})
            return self._result
        # close the connection, because the netsnmp session cannot be reused
        self._connection.close()

        
        
        # post set get
        # Note: although we are doing a get, the netsnmp varbind _can_ have values
        # they are disregarded when doing a get
        self._connection.configure(self._task.args)
        error, elapsed, post_set_result = self._connection.get()
        self._result['elapsed']['post_set_get'] = elapsed
        self._result['elapsed']['total'] += elapsed

        if error:
            final_error = f"SNMP get (post-set)failed. The error was: '{error}'"
            self._result.update({"failed": True, "msg": final_error})
            return self._result
        else:
            self._result.update({"after": post_set_result})


        if pre_set_result != post_set_result:
            self._result.update({"changed": True})

        return self._result
