# (c) 2021 Red Hat Inc.
# (c) 2021 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author: Ansible Networking Team
connection: v3_usm
short_description: Make SNMP v3 user-based security model (USM) connections to a device.
description:
- Make SNMP v3 user-based security model (USM) connections to a device.
version_added: 1.0.0
requirements:
- python bindings for netsnmp

options:
  auth_pass:
    description:
    - Specify the SNMP v3 authentication passphrase.
    type: str
    ini:
    - section: ansible.snmp
      key: context
    env:
    - name: ANSIBLE_SNMP_AUTH_PASS
    vars:
    - name: ansible_snmp_auth_pass
  auth_proto:
    description:
    - Specify the SNMP v3 authentication protocol.
    default: MD5
    choices:
    - MD5
    - SHA1
    - SHA-192
    - SHA-256
    - SHA-284
    - SHA-512
    type: str
    ini:
    - section: ansible.snmp
      key: context
    env:
    - name: ANSIBLE_SNMP_AUTH_PROTO
    vars:
    - name: ansible_snmp_auth_proto
  context:
    description:
    - Specify the SNMP v3 context name.
    default: ''
    type: str
    ini:
    - section: ansible.snmp
      key: context
    env:
    - name: ANSIBLE_SNMP_CONTEXT
    vars:
    - name: ansible_snmp_context
  context_engine_id:
    description:
    - Specify the SNMP v3 context engine ID.
    - Will be probed if not supplied.
    type: str
    ini:
    - section: ansible.snmp
      key: sec_level
    env:
    - name: ANSIBLE_SNMP_CONTEXT_ENGINE_ID
    vars:
    - name: ansible_snmp_context_engine_id
  host:
    description:
    - Specifies the remote device FQDN or IP address for the SNMP connection
      to.
    default: inventory_hostname
    type: str
    vars:
    - name: ansible_host
  port:
    description:
    - Specifies the port on the remote device that listens for SNMP connections.
    type: int
    default: 161
    ini:
    - section: defaults
      key: remote_port
    env:
    - name: ANSIBLE_REMOTE_PORT
    vars:
    - name: ansible_port
  priv_pass:
    description:
    - Specify the SNMP v3 privacy passphrase.
    type: str
    ini:
    - section: ansible.snmp
      key: priv_proto
    env:
    - name: ANSIBLE_SNMP_PRIV_PASS
    vars:
    - name: ansible_snmp_priv_pass
  priv_proto:
    description:
    - Specify the SNMP v3 privacy protocol.
    default: DES
    choices:
    - DES
    - AES128
    - AES256
    type: str
    ini:
    - section: ansible.snmp
      key: priv_proto
    env:
    - name: ANSIBLE_SNMP_PRIV_PROTO
    vars:
    - name: ansible_snmp_priv_proto
  retries:
    description:
    - Specify the number retries before failure
    type: int
    default: 3
    ini:
    - section: ansible.snmp
      key: retries
    env:
    - name: ANSIBLE_SNMP_RETRIES
    vars:
    - name: ansible_snmp_RETRIES
  sec_engine_id:
    description:
    - Specify the SNMP v3 security engine ID.
    - Will be probed if not supplied.
    type: str
    ini:
    - section: ansible.snmp
      key: sec_name
    env:
    - name: ANSIBLE_SNMP_SEC_ENGINE_ID
    vars:
    - name: ansible_snmp_sec_engine_id
  sec_name:
    description:
    - Specify the SNMP v3 security name.
    default: initial
    type: str
    ini:
    - section: ansible.snmp
      key: sec_name
    env:
    - name: ANSIBLE_SNMP_SEC_NAME
    vars:
    - name: ansible_snmp_sec_name
  sec_level:
    description:
    - Specify the SNMP v3 secutiry level.
    default: noAuthNoPriv
    type: str
    choices:
    - noAuthNoPriv
    - authNoPriv
    - authPriv
    ini:
    - section: ansible.snmp
      key: sec_level
    env:
    - name: ANSIBLE_SNMP_SEC_LEVEL
    vars:
    - name: ansible_snmp_sec_level
  timeout:
    description:
    - Specify the number of micro-seconds before a retry
    type: int
    default: 500000
    ini:
    - section: ansible.snmp
      key: timeout
    env:
    - name: ANSIBLE_SNMP_TIMEOUT
    vars:
    - name: ansible_snmp_timeout


  
"""


from ansible_collections.ansible.snmp.plugins.plugin_utils.netsnmp_wrapper import (
    Snmpv3UsmConnection,
)
from ansible_collections.ansible.snmp.plugins.plugin_utils.snmp_connection_base import (
    SnmpConnectionBase,
)


class Connection(SnmpConnectionBase):
    """SNMP v3-usm based connections"""

    transport = "v3_usm"
    has_pipelining = False

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)

    def _connect(self):
        kwargs = {"dest_host": self.get_option("host")}

        params_with_defaults = [
            "auth_proto",
            "context",
            "host",
            "port",
            "priv_proto",
            "retries",
            "sec_name",
            "sec_level",
            "timeout",
        ]
        for param in params_with_defaults:
            kwargs[param] = self.get_option(param)

        params_no_defaults = [
            "auth_pass",
            "context_engine_id",
            "priv_pass",
            "sec_engine_id",
        ]
        for param in params_no_defaults:
            value = self.get_option(param)
            if value is not None:
                kwargs[param] = self.get_option(param)

        self._connection = Snmpv3UsmConnection(**kwargs)
        super()._connect()
