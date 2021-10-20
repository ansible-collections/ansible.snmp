# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: set
short_description: Perform an SNMP set against a remote device for one or more OIDs
version_added: "1.0.0"
description:
  - Perform an SNMP get against a remote device for one or more OIDs
options:
  oids:
    description:
      - A dictionary of OID, value to set on the remote device
    type: list
    elements: dict
    required: True
    suboptions:
      oid:
        description:
        - The OID to update.
        type: str
        required: True
      iid:
        description:
        - The dotted-decimal, instance idenfier, for scalar MIB objects use '0'
        type: str
        required: True
      type:
        description:
        - The type of value
        type: str
        choices:
        - OBJECTID
        - OCTETSTR 
        - INTEGER
        - NETADDR
        - IPADDR
        - COUNTER
        - COUNTER64
        - GAUGE
        - UINTEGER
        - TICKS
        - OPAQUE
        - NULL
      value:
        description:
        - The value to be set for the OID.
        type: raw
        required: True

 

notes:
- The SNMP set task will always return 'changed'

author: Ansible Networking Team

"""

EXAMPLES = r"""
- name: Set several individual OIDs
  ansible.snmp.set:
    oids:
    - oid: "SNMPv2-MIB::sysContact"
      iid: '0'
      value: "cidrblock @ {{ ts }}"
    - oid: "SNMPv2-MIB::sysLocation"
      iid: '0'
      value: "Office @ {{ ts }}"
  vars:
    ts: "{{ lookup('pipe', 'date -u +\"%Y-%m-%dT%H:%M:%SZ\"') }}"
"""


RETURN = """
before:
  description: The result of an SNMP get for the OIDs prior to set
  returned: always
  type: dict
  keys:
    raw:
      description: The raw result from the snmp walk
      returned: always
      type: list
      elements: dict
      entries:
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
      entries:
        _raw: 
          description: The individual oid entry and the currently set value
          returned: always
after:
  description: The result of an SNMP get for the OIDs after the set
  returned: always
  type: dict
  keys:
    raw:
      description: The raw result from the snmp walk
      returned: always
      type: list
      elements: dict
      entries:
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
      entries:
        _raw: 
          description: The individual oid entry and the currently set value
          returned: always
elapsed:
  description: The amount of time in seconds spent for the snmp calls
  returned: always
  type: dict
  entries:
    post_set_get:
      description: The amount of time spent in seconds for the get after the set
      type: float
      returned: always
    pre_set_get:
      description: The amount of time spent in seconds for the get prior to the set
      type: float
      returned: always
    set:
      description: The amount of time spent in seconds for the set
      type: float
      returned: always
    total:
      description: the amount of time spent on all snmp calls
      type: float
      returned: always

"""
