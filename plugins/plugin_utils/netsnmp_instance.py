# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""An instance of netsnmp
"""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import time

from typing import List, Union


# Note: HAS_SNMP is checked in snmp_connection_base
try:
    import netsnmp

    HAS_NETSNMP = True
except ImportError:
    HAS_NETSNMP = False


from .netsnmp_defs import (
    SnmpConfiguration,
    SnmpConfigurationParamMap,
    SnmpConnectionParamMap,
    SnmpResponse,
    Snmpv1Connection,
    Snmpv2cConnection,
    Snmpv3UsmConnection,
)


class SnmpInstance:
    """An instance of netsnmp"""

    SNMP_INT_TYPES = [
        "INTEGER32",
        "INTEGER",
        "COUNTER32",
        "GAUGE32",
        "TIMETICKS",
        "COUNTER64",
        "UNSIGNED32",
        "COUNTER",
        "GAUGE",
    ]

    def __init__(
        self,
        connection: Union[Snmpv1Connection, Snmpv2cConnection, Snmpv3UsmConnection],
        configuration: SnmpConfiguration,
    ):

        args = {}
        for attribute in SnmpConnectionParamMap:
            if hasattr(connection, attribute.name):
                args[attribute.value] = getattr(connection, attribute.name)
        self.session = netsnmp.Session(**args)

        # Special case for a V1 only setter
        if hasattr(connection, "retry_no_such"):
            self.session.RetryNoSuch = getattr(connection, "retry_no_such")

        for attribute in SnmpConfigurationParamMap:
            if hasattr(configuration, attribute.name):
                setattr(
                    self.session,
                    attribute.value,
                    int(getattr(configuration, attribute.name)),
                )

        self._oids: List

    def set_oids(self, oid_list: List) -> None:
        """Transform the list of oid dicts into a VarList

        :param oid_list: The list of oid dicts
        :type oid_list: list
        """
        self._oids = netsnmp.VarList()
        for oid in oid_list:
            self._oids.append(netsnmp.Varbind(**oid))
        return vars

    def _varbinds_to_dicts(self) -> List:
        """Convert the varbind into a list of dicts
        use the iid as the key to group attributes

        In the case of an int type, convert it
        """
        results = {}

        for entry in self._oids.varbinds:
            if entry.iid not in results:
                results[entry.iid] = {}
            value = entry.val
            if entry.type in self.SNMP_INT_TYPES:
                try:
                    value = int(value)
                except ValueError:
                    pass
            # This does not handle OCTETSTR correctly
            # but at least it will be a string
            # OCTETSTR is best handled with "use_sprint_value"
            if isinstance(entry.val, bytes):
                value = str(value)
            results[entry.iid][entry.tag] = value
        return list(results.values())

    def get(self) -> SnmpResponse:
        """Perform the SNMP get"""
        error = None
        start = time.time()
        try:
            _res = self.session.get(self._oids)
        except Exception as exc:  # pylint: disable=broad-except
            error = str(exc)
        end = time.time()
        if self.session.ErrorStr:
            error = self.session.ErrorStr
        return SnmpResponse(
            error=error,
            elapsed=end - start,
            result=self._varbinds_to_dicts(),
            raw=[vb.__dict__ for vb in self._oids.varbinds],
        )

    def set(self) -> SnmpResponse:
        """Perform the SNMP set"""
        error = None
        start = time.time()
        try:
            _res = self.session.set(self._oids)
        except Exception as exc:  # pylint: disable=broad-except
            error = str(exc)
        end = time.time()
        if self.session.ErrorStr:
            error = self.session.ErrorStr
        return SnmpResponse(error=error, elapsed=end - start)

    def walk(self) -> SnmpResponse:
        """Perform the SNMP walk"""
        error = None
        start = time.time()
        try:
            _res = self.session.walk(self._oids)
        except Exception as exc:  # pylint: disable=broad-except
            error = str(exc)
        end = time.time()
        if self.session.ErrorStr:
            error = self.session.ErrorStr
        return SnmpResponse(
            error=error,
            elapsed=end - start,
            result=self._varbinds_to_dicts(),
            raw=[vb.__dict__ for vb in self._oids.varbinds],
        )
