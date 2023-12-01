=====================================
Ansible Snmp Collection Release Notes
=====================================

.. contents:: Topics


v2.0.0
======

Release Summary
---------------

Starting from this release, the minimum `ansible-core` version this collection requires is `2.14.0`. The last known version compatible with ansible-core<2.14 is `v1.2.0`.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.14.0`, since previous ansible-core versions are EoL now.

v1.2.0
======

Minor Changes
-------------

- Update the supported net-snmp version from 5.9.1 to 5.9.4 for the collection.

v1.0.1
======

Bugfixes
--------

- Re-release post migration from https://github.com/ansible-network/ansible.snmp to https://github.com/ansible-collections/ansible.snmp

v1.0.0
======

New Plugins
-----------

Connection
~~~~~~~~~~

- v1 - Make SNMP v1 connections to a device
- v2c - Make SNMP v2c connections to a device
- v3_usm - Make SNMP v3 user-based security model (USM) connections to a device.

New Modules
-----------

- get - Perform an SNMP get against a remote device for one or more OIDs
- set - Perform an SNMP set against a remote device for one or more OIDs
- walk - Perform an SNMP walk against a remote device for one or more OIDs
