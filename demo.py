import json
import time

from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.web import JsonLexer

from snmp_wrapper import SnmpConfiguration, Snmpv2cConnection, SnmpInstance


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
    error, elapsed, result = instance.walk()
    if error:
        raise Exception(error)
    color_dump(result)
    print("SNMP time: " + str(elapsed))


    input("Walk a table using cisco mibs. Press Enter to continue...")
    instance.set_oids(['ENTITY-MIB::entPhysicalTable'])
    error, elapsed, result = instance.walk()
    if error:
        raise Exception(error)
    color_dump(result)
    print("SNMP time: " + str(elapsed))


    input("Walk a table row by row. Press Enter to continue...")
    start = time.time()
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
    error, elapsed, result = instance.walk()
    if error:
        raise Exception(error)
    color_dump(result)
    print("SNMP time: " + str(elapsed))


    input("Get a single. Press Enter to continue...")
    start = time.time()
    instance.set_oids(["SNMPv2-MIB::sysDescr.0"])
    error, elapsed, result = instance.get()
    if error:
        raise Exception(error)
    color_dump(result)
    print("SNMP time: " + str(elapsed))


    input("Get several. Press Enter to continue...")
    start = time.time()
    instance.set_oids(
        ["SNMPv2-MIB::sysDescr.0", "SNMPv2-MIB::sysContact.0", "SNMPv2-MIB::sysLocation.0"]
    )
    error, elapsed, result = instance.get()
    if error:
        raise Exception(error)
    color_dump(result)
    print("SNMP time: " + str(elapsed))


    input("Get a OID. Press Enter to continue...")
    start = time.time()
    instance.set_oids([".1.3.6.1.2.1.1.1.0"])
    error, elapsed, result = instance.get()
    if error:
        raise Exception(error)
    color_dump(result)
    print("SNMP time: " + str(elapsed))

if __name__ == "__main__":
    main()