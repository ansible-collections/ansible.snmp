import json
from enum import Enum

import netsnmp
import yaml

from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.web import JsonLexer
from types import SimpleNamespace
from typing import List
from typing import Union


class SnmpConfiguration(SimpleNamespace):
    # Note: these will all get cast as an int later
    # here as a bool for convenience
    use_long_names: bool = False
    use_sprint_value: bool = False
    use_enums: bool = False
    use_numeric: bool = False
    best_guess: int = 0


class SnmpConnectionBase(SimpleNamespace):
    dest_host: str = "localhost"
    remote_port: int = 161
    timeout: int = 500000
    retries: int = 3


class Snmpv1Connection(SnmpConnectionBase):
    version: int = 1
    retry_no_such: int = 0


class Snmpv2cConnection(SnmpConnectionBase):
    community: str = "public"
    version: int = 2


class SnmpConfigurationParamMap(Enum):
    use_long_names = "UseLongNames"
    use_sprint_value = "UseSprintValue"
    use_enums = "UseEnums"
    use_numeric = "UseNumeric"
    best_guess = "BestGuess"


class SnmpConnectionParamMap(Enum):
    # base session
    dest_host = "DestHost"
    version = "Version"
    remote_port = "RemotePort"
    timeout = "Timeout"
    retries = "Retries"
    retry_no_such = "RetryNoSuch"
    # v1/v2c session
    community = "Community"
    # v3 session
    sec_name = "SecName"
    sec_level = "SecLevel"
    context_engine_id = "ContextEngineId"
    context = "Context"
    # v3 over TLS/DTLS
    our_identity = "OurIdentity"
    their_identity = "TheirIdentity"
    trust_cert = "TrustCert"
    their_hostname = "TheirHostname"
    # v3 with USM
    sec_engine_id = "SecEngineId"
    auth_proto = "AuthProto"
    auth_pass = "AuthPass"
    priv_proto = "PrivProto"
    priv_pass = "PrivPass"


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
        connection: Union[Snmpv1Connection, Snmpv2cConnection],
        configuration: SnmpConfiguration,
    ):

        args = {}
        for attribute in SnmpConnectionParamMap:
            if hasattr(connection, attribute.name):
                args[attribute.value] = getattr(connection, attribute.name)
        self.session = netsnmp.Session(**args)

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
            self._oids.append(netsnmp.Varbind(oid))
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
        _res = self.session.get(self._oids)
        if self.session.ErrorStr:
            print(self.session.ErrorStr)
        return self.varbinds_to_dict()

    def walk(self):
        _res = self.session.walk(self._oids)
        if self.session.ErrorStr:
            print(self.session.ErrorStr)
        return self._varbinds_to_dicts()

def color_dump(obj):
    output = json.dumps(obj, indent=4)
    colorful = highlight(
        output,
        lexer=JsonLexer(),
        formatter=Terminal256Formatter(style='monokai'),
    )
    print(colorful)

def main():
    configuration = SnmpConfiguration(use_enums=True, use_sprint_value=True)
    connection = Snmpv2cConnection(
        dest_host="nxos101", community="public", timeout=50000000
    )
    instance = SnmpInstance(connection=connection, configuration=configuration)

    input("Walk a table cell by cell. Press Enter to continue...")
    instance.set_oids(["IF-MIB::ifTable"])
    result = instance.walk()
    color_dump(result)

    input("Walk a table using cisco mibs. Press Enter to continue...")
    instance.set_oids(['ENTITY-MIB::entPhysicalTable'])
    result = instance.walk()
    color_dump(result)

    input("Walk a table row by row. Press Enter to continue...")
    columns = [
        "ifIndex",
        "ifDescr",
        "ifType",
        "ifMtu",
        "ifSpeed",
        "ifPhysAddress",
        "ifAdminStatus",
        "ifOperStatus",
        "ifLastChange",
        "ifInOctets",
        "ifInUcastPkts",
        "ifInDiscards",
        "ifInErrors",
        "ifInUnknownProtos",
        "ifOutOctets",
        "ifOutUcastPkts",
        "ifOutDiscards",
        "ifOutErrors",
        "ifSpecific",
    ]
    mib = "IF-MIB"
    instance.set_oids([f"{mib}::{column}" for column in columns])
    result = instance.walk()
    color_dump(result)

    input("Get a single. Press Enter to continue...")
    instance.set_oids(["SNMPv2-MIB::sysDescr.0"])
    result = instance.get()
    color_dump(result)

    input("Get several. Press Enter to continue...")
    instance.set_oids(
        ["SNMPv2-MIB::sysDescr.0", "SNMPv2-MIB::sysContact.0", "SNMPv2-MIB::sysLocation.0"]
    )
    result = instance.get()
    color_dump(result)

    input("Get a OID. Press Enter to continue...")
    instance.set_oids([".1.3.6.1.2.1.1.1.0"])
    result = instance.get()
    color_dump(result)

if __name__ == "__main__":
    main()