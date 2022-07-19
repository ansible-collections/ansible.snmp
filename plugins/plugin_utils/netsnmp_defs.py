# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The SNMP v1 connection

Note:
  It is importtant that these class defintions stay in sync with
  their respective module and connection docstrings
  These classes are introspected for defautl and non-default values
  and the attributes are subsequently pulled from the
  connection options and task args
  The default values here are not used, but serve as an indication
  of whether or not the argspec value of None should be used
  as ansible provides None for an optional value in the argspec
  because the netsnmp Session cannot be updated with a None value
"""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from enum import Enum
from types import SimpleNamespace
from typing import Dict, List, NamedTuple, Union


class IntrospectableSimpleNamespace(SimpleNamespace):
    """A modified SimpleNamespace that allows for introspection
    for attributes that have a value or not. Used immediately
    after instantiation, indicates attributes that had a default value set"""

    @classmethod
    def _describe(cls) -> Dict:
        """Produce a dict of all annotations, including parent classes

        :return: A dict of attr:type
        :rtype: dict
        """
        dyct = {}
        for c in cls.mro():
            try:
                dyct.update(**c.__annotations__)
            except AttributeError:
                pass
        return dyct

    @property
    def set(self) -> List[str]:
        """Produce a list of attributes that have a value

        :return: A list of attr w/ a value set
        :rtype: List
        """
        return [k for k in self._describe() if hasattr(self, k)]

    @property
    def not_set(self) -> List[str]:
        """Produce a list of attributes that do not have a value

        :return: A list of attr w/o a value set
        :rtype: List
        """
        return [k for k in self._describe() if not hasattr(self, k)]


class SnmpConfiguration(IntrospectableSimpleNamespace):
    """The netsnmp configuration attributes

    Note: these will all get cast as an int later
    here as a bool for convenience
    """

    best_guess: int = 0
    enums: bool = False
    long_names: bool = False
    numeric: bool = False
    sprint_value: bool = False


class SnmpConnectionBase(IntrospectableSimpleNamespace):
    """The SNMP base class

    This contains attributes common to all SNMP connection types
    """

    host: str = "localhost"
    port: int = 161
    timeout: int = 500000
    retries: int = 3


class Snmpv1Connection(SnmpConnectionBase):
    """The SNMP v1 connection class

    This contains attributes unique to the SNMP v1 connection
    """

    version: int = 1
    retry_no_such: int = 0


class Snmpv2cConnection(SnmpConnectionBase):
    """The SNMP v2 connection class

    This contains attributes unique to the SNMP v2c connection
    """

    community: str = "public"
    version: int = 2


class Snmpv3Connection(SnmpConnectionBase):
    """The SNMP v3 connection base class

    This contains attributes common to all SNMP v3 connections
    """

    context_engine_id: str
    sec_name: str = "initial"
    sec_level: str = "noAuthPriv"
    context: str = ""


class Snmpv3UsmConnection(Snmpv3Connection):
    """The SNMP v3 user security model class

    This contains attributes for the SNMP v3 USM connection"""

    sec_engine_id: str
    auth_pass: str
    priv_pass: str
    auth_proto: str = "MD5"
    priv_proto: str = "DES"


# Note: If there is a better implementation here
#       that doesn't violate the UPPER_CASE convention for enum
#       it wasn't obvious
class SnmpConfigurationParamMap(Enum):
    """Map the configuration attributes to their netsnmp counterparts

    attributes should map to docstring/argspec attributes
    values should correspond to netsnmp attributes
    """

    # pylint: disable=invalid-name

    long_names = "UseLongNames"
    sprint_value = "UseSprintValue"
    enums = "UseEnums"
    numeric = "UseNumeric"
    best_guess = "BestGuess"


class SnmpConnectionParamMap(Enum):
    """Map the connection attributes to their netsnmp counterparts

    attributes should map to connection options
    values should correspond to netsnmp attributes
    """

    # pylint: disable=invalid-name

    # base session
    host = "DestHost"
    version = "Version"
    port = "RemotePort"
    timeout = "Timeout"
    retries = "Retries"

    # v1 only
    # handled separately because it's a setter not a arg/kwarg v1 only
    # retry_no_such = "RetryNoSuch"

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


class SnmpResponse(NamedTuple):  # pylint:disable=inherit-non-class
    """Simple structure for the response from an snmp call"""

    elapsed: Dict
    error: str
    result: Union[List, Dict] = {}
    raw: List = []
