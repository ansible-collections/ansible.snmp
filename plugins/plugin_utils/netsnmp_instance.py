""" An instance of netsnmp"""

import netsnmp
import time


from typing import List
from typing import Union

from .netsnmp_defs import SnmpConfiguration
from .netsnmp_defs import SnmpConfigurationParamMap
from .netsnmp_defs import SnmpConnectionParamMap
from .netsnmp_defs import SnmpResponse
from .netsnmp_defs import Snmpv1Connection
from .netsnmp_defs import Snmpv2cConnection
from .netsnmp_defs import Snmpv3UsmConnection


class SnmpInstance:

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
        connection: Union[
            Snmpv1Connection, Snmpv2cConnection, Snmpv3UsmConnection
        ],
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

    def set_oids(self, oid_list) -> None:
        self._oids = netsnmp.VarList()
        for oid in oid_list:
            self._oids.append(netsnmp.Varbind(**oid))
        return vars

    def _varbinds_to_dicts(self) -> List:
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
            # but al leat it will be a string
            # OCTETSTR is best handled with "use_sprint_value"
            if isinstance(entry.val, bytes):
                value = str(value)
            results[entry.iid][entry.tag] = value
        return list(results.values())

    def get(self):
        error = None
        start = time.time()
        try:
            _res = self.session.get(self._oids)
        except Exception as exc:
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

    def set(self):
        error = None
        start = time.time()
        try:
            res = self.session.set(self._oids)
        except Exception as exc:
            error = str(exc)
        end = time.time()
        if self.session.ErrorStr:
            error = self.session.ErrorStr
        return SnmpResponse(error=error, elapsed=end - start)

    def walk(self):
        error = None
        start = time.time()
        try:
            _res = self.session.walk(self._oids)
        except Exception as exc:
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
