=====================================
Ansible Snmp Collection Release Notes
=====================================

.. contents:: Topics


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
