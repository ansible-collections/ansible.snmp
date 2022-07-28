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
module: set
author: Bradley Thornton (@cidrblock)
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
        aliases:
        - tag
      iid:
        description:
        - The dotted-decimal, instance identifier, for scalar MIB objects use '0'
        type: str
        required: True
      type:
        description:
        - The type of value
        type: str
        choices:
        - "OBJECTID"
        - "OCTETSTR"
        - "INTEGER"
        - "NETADDR"
        - "IPADDR"
        - "COUNTER"
        - "COUNTER64"
        - "GAUGE"
        - "UINTEGER"
        - "TICKS"
        - "OPAQUE"
        - "NULL"
      value:
        description:
        - The value to be set for the OID.
        type: raw
        required: True
        aliases:
        - val



notes:
- The SNMP set task will always return 'changed'
- Tested against ubuntu 18.04 using net-snmp.
- This module works with connection C(v1), C(v2c), C(v3_usm).
"""

EXAMPLES = r"""
---
# Update 2 individual entries
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

# Update the description of all interfaces matching a regex
- name: Retrieve the index and name from the interface table
  ansible.snmp.walk:
    oids:
    - oid: IF-MIB::ifIndex
    - oid: IF-MIB::ifDescr
  register: if_indicies

- name: Set a timestamp and the regex to use for matching interface names
  set_fact:
    ts: "{{ lookup('pipe', 'date -u +\"%Y-%m-%dT%H:%M:%SZ\"') }}"
    regex: "(Ethernet|Gigabit|Intel).*"

- name: Update all matching interfaces
  ansible.snmp.set:
    oids:
    - oid: IF-MIB::ifAlias
      iid: "{{ iid }}"
      value: "Configured by ansible @ {{ ts }}"
  vars:
    matching_interfaces: "{{ lookup('ansible.utils.index_of', if_indicies.result, 'match', regex, 'ifDescr', wantlist=True) }}"
    iid: "{{ if_indicies['result'][int_id]['ifIndex'] }}"
  loop: "{{ matching_interfaces }}"
  loop_control:
    loop_var: int_id
  register: changes

- name: Review all changes
  ansible.utils.fact_diff:
    before: "{{ interface.before.result|ansible.utils.to_paths }}"
    after: "{{ interface.after.result|ansible.utils.to_paths }}"
  loop: "{{ changes.results }}"
  loop_control:
    loop_var: interface
    index_var: idx
    label: "{{ idx }}"

"""

RETURN = """
---
after:
  description: The result of an SNMP get for the OIDs after the set
  returned: always
  type: dict
  sample:
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
before:
  description: The result of an SNMP get for the OIDs prior to set
  returned: always
  type: dict
  sample:
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
  sample:
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
