# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
""" The base class for SNMP action plugins
"""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from typing import Dict, Union

from ansible.plugins.action import ActionBase

# pylint: disable=import-error
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)


# pylint: enable=import-error


class SnmpActionBase(ActionBase):
    """action module"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._result: Dict
        self._task_vars: Union[Dict, None]

    def _check_argspec(self, documentation):
        aav = AnsibleArgSpecValidator(
            data=self._task.args,
            schema=documentation,
            schema_format="doc",
            name=self._task.action,
        )
        valid, errors, self._task.args = aav.validate()
        if not valid:
            self._result["failed"] = True
            self._result["msg"] = errors

    def run(self, tmp=None, task_vars=None):
        """The std execution entry pt for an action plugin

        :param tmp: no longer used
        :type tmp: none
        :param task_vars: The vars provided when the task is run
        :type task_vars: dict
        :return: The results from the plugin
        :rtype: dict
        """
        self._result = super().run(tmp, task_vars)
        self._task_vars = task_vars
