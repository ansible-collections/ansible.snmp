.. _ansible.snmp.set_module:


****************
ansible.snmp.set
****************

**Perform an SNMP set against a remote device for one or more OIDs**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Perform an SNMP get against a remote device for one or more OIDs




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>oids</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A dictionary of OID, value to set on the remote device</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>iid</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The dotted-decimal, instance idenfier, for scalar MIB objects use &#x27;0&#x27;</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>oid</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The OID to update.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>OBJECTID</li>
                                    <li>OCTETSTR</li>
                                    <li>INTEGER</li>
                                    <li>NETADDR</li>
                                    <li>IPADDR</li>
                                    <li>COUNTER</li>
                                    <li>COUNTER64</li>
                                    <li>GAUGE</li>
                                    <li>UINTEGER</li>
                                    <li>TICKS</li>
                                    <li>OPAQUE</li>
                                    <li>None</li>
                        </ul>
                </td>
                <td>
                        <div>The type of value</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The value to be set for the OID.</div>
                </td>
            </tr>

    </table>
    <br/>


Notes
-----

.. note::
   - The SNMP set task will always return 'changed'



Examples
--------

.. code-block:: yaml

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




Status
------


Authors
~~~~~~~

- Ansible Networking Team
