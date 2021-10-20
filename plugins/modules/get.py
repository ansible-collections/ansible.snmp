# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get
short_description: Perform an SNMP get against a remote device for one or more OIDs
version_added: "1.0.0"
description:
  - Perform an SNMP get against a remote device for one or more OIDs
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
      - A dictionary of entries to get from the remote device
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
        - the dotted-decimal, instance idenfier, for scalar MIB objects use '0'
        type: str
  numeric:
    description:
      - Set to `True to have `oids` returned untranslated (i.e. dotted-decimal).
    type: bool
    default: False
  sprint_value:
    description:
      - Set to `True` to have return values formatted with netsnmp's sprint_value function. 
      - This will result in certain data types being returned in non-canonical format 
    type: bool
    default: True

notes:

author: Ansible Networking Team

"""

EXAMPLES = r"""
"""


RETURN = """
"""
