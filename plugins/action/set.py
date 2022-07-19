# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The set action plugin
"""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from typing import Dict, Union

# pylint: disable=import-error
from ansible_collections.ansible.snmp.plugins.modules.set import DOCUMENTATION
from ansible_collections.ansible.snmp.plugins.plugin_utils.snmp_action_base import SnmpActionBase


# pylint: enable=import-error


class ActionModule(SnmpActionBase):
    """action module"""

    # pylint: disable=too-few-public-methods
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._result: Dict
        self._task_vars: Dict

    def run(
        self,
        tmp: None = None,
        task_vars: Union[Dict, None] = None,
    ) -> Dict:
        """The std execution entry pt for an action plugin

        :param tmp: no longer used
        :type tmp: none
        :param task_vars: The vars provided when the task is run
        :type task_vars: dict
        :return: The results from the plugin
        :rtype: dict
        """
        super().run(tmp, task_vars)

        self._check_argspec(DOCUMENTATION)
        if self._result.get("failed"):
            return self._result

        self._result.update({"elapsed": {"total": 0}})

        # pre set get
        # Note: although we are doing a get, the netsnmp varbind _can_ have values
        # they are disregarded when doing a get
        self._connection.configure(self._task.args)
        pre_set_response = self._connection.get()
        self._result["elapsed"]["pre_set_get"] = pre_set_response.elapsed
        self._result["elapsed"]["total"] += pre_set_response.elapsed

        if pre_set_response.error:
            final_error = f"SNMP get (pre-set)failed. The error was: '{pre_set_response.error}'"
            self._result.update({"failed": True, "msg": final_error})
            return self._result

        self._result.update(
            {
                "before": {
                    "result": pre_set_response.result,
                    "raw": pre_set_response.raw,
                },
            },
        )
        # close the connection, because the netsnmp session cannot be reused
        self._connection.close()

        # set
        self._connection.configure(self._task.args)
        set_response = self._connection.set()
        self._result["elapsed"]["set"] = set_response.elapsed
        self._result["elapsed"]["total"] += set_response.elapsed

        if set_response.error:
            final_error = f"SNMP set failed. The error was: '{set_response.error}'"
            self._result.update({"failed": True, "msg": final_error})
            return self._result
        # close the connection, because the netsnmp session cannot be reused
        self._connection.close()

        # post set get
        # Note: although we are doing a get, the netsnmp varbind _can_ have values
        # they are disregarded when doing a get
        self._connection.configure(self._task.args)
        post_set_response = self._connection.get()
        self._result["elapsed"]["post_set_get"] = post_set_response.elapsed
        self._result["elapsed"]["total"] += post_set_response.elapsed

        if post_set_response.error:
            final_error = f"SNMP get (post-set)failed. The error was: '{post_set_response.error}'"
            self._result.update({"failed": True, "msg": final_error})
            return self._result

        self._result.update(
            {
                "after": {
                    "result": post_set_response.result,
                    "raw": post_set_response.raw,
                },
            },
        )

        if pre_set_response.raw != post_set_response.raw:
            self._result.update({"changed": True})

        return self._result
