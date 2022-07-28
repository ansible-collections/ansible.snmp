#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-module-docstring

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

DOCUMENTATION = r"""
---
module: walk
author: Bradley Thornton (@cidrblock)
short_description: Perform an SNMP walk against a remote device for one or more OIDs
version_added: "1.0.0"
description:
  - Perform an SNMP walk against a remote device for one or more OIDs
options:
  best_guess:
    description:
    - This setting controls how return value oids are parsed.
    - Setting to 0 causes a regular lookup.
    - Setting to 1 causes a regular expression match (defined as -Ib in snmpcmd).
    - Setting to 2 causes a random access lookup (defined as -IR in snmpcmd).
    type: int
    choices:
    - 0
    - 1
    - 2
    default: 0
  enums:
    description:
      - Set to `True` to have integer return values converted to enumeration identifiers if possible.
    type: bool
    default: True
  long_names:
    description:
      - Set to `True` to have OIDS generated preferring longer Mib name convention.
    type: bool
    default: False
  oids:
    description:
      - A dictionary of entries to walk on the remote device
    type: list
    elements: dict
    required: True
    suboptions:
      oid:
        description:
        - The OID to retrieve.
        type: str
        required: True
      iid:
        description:
        - the dotted-decimal, instance identifier, for scalar MIB objects use '0'
        type: str
  numeric:
    description:
      - Set to `True to have `oids` returned untranslated (i.e. dotted-decimal).
    type: bool
    default: False
  sprint_value:
    description:
      - Set to `True` to have return values formatted with netsnmp's sprint_value function.
      - This will result in certain data types being returned in non-canonical format.
      - Values returned with this option set may not be appropriate for 'set' operations.

    type: bool
    default: True

notes:
- Tested against ubuntu 18.04 using net-snmp.
- This module works with connection C(v1), C(v2c), C(v3_usm).
"""

EXAMPLES = r"""
---
"""

RETURN = """
---
elapsed:
  description: The amount of time in seconds spent for the snmp calls
  returned: always
  type: dict
  sample:
    walk:
      description: The amount of time spent in seconds for the walk
      type: float
      returned: always
    total:
      description: the amount of time spent on all snmp calls
      type: float
      returned: always
raw:
  description: The raw result from the snmp walk
  returned: always
  type: list
  elements: dict
  sample:
    iid:
      description: The instance id
      returned: always
      type: str
    tag:
      description: The OID
      returned: always
      type: str
    type:
      description: The type of the value
      returned: always
      type: str
    value:
      description: The currently set value for the oid
      returned: always
      type: raw
result:
  description: The transformed result from the snmp walk
  returned: always
  type: list
  elements: dict
  sample:
    _raw:
      description: The individual oid entry and the currently set value
      returned: always
"""
