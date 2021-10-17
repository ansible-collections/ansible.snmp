# (c) 2021 Red Hat Inc.
# (c) 2021 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author: Ansible Networking Team
connection: v2
short_description: Make SNMP v2 connections to a device
description:
- Make SNMP v2 connections to a device.
version_added: 1.0.0
requirements:
- python bindings for netsnmp

options:
  host:
    description:
    - Specifies the remote device FQDN or IP address for the SNMP connection
      to.
    default: inventory_hostname
    vars:
    - name: ansible_host
  port:
    type: int
    description:
    - Specifies the port on the remote device that listens for SNMP connections.
    default: 161
    ini:
    - section: defaults
      key: remote_port
    env:
    - name: ANSIBLE_REMOTE_PORT
    vars:
    - name: ansible_port
  community:
    description:
    - Specifc the community string for SNMP v2 connections.
    default: public
    ini:
    - section: ansible.snmp
      key: community
    env:
    - name: ANSIBLE_SNMP_COMMUNITY
    vars:
    - name: ansible_snmp_community
"""

from ansible.plugins.connection import ConnectionBase


class Connection(ConnectionBase):
    """Local based connections"""

    transport = "v2"
    has_pipelining = False

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)

    def _connect(self):
        if not self._connected:
            self._connected = True
        return self

    def exec_command(self, cmd, in_data=None, sudoable=True):
        pass

    def put_file(self, in_path, out_path):
        pass

    def fetch_file(self, in_path, out_path):
        pass

    def close(self):
        self._connected = False
