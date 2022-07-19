# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The get action plugin
"""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from typing import Dict, Union

# pylint: disable=import-error
from ansible_collections.ansible.snmp.plugins.modules.get import DOCUMENTATION
from ansible_collections.ansible.snmp.plugins.plugin_utils.snmp_action_base import SnmpActionBase


# pylint: enable=import-error


class ActionModule(SnmpActionBase):
    """action module"""

    # pylint: disable=too-few-public-methods
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._result: Dict
        self._task_vars: Dict

    def run(self, tmp: None = None, task_vars: Union[Dict, None] = None) -> Dict:
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
        self._result.update({"changed": False})

        self._connection.configure(self._task.args)

        response = self._connection.get()
        self._result["elapsed"]["get"] = response.elapsed
        self._result["elapsed"]["total"] += response.elapsed

        if response.error:
            self._result.update({"failed": True, "msg": response.error})
        else:
            self._result.update({"result": response.result, "raw": response.raw})

        return self._result
