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
                        <div>The dotted-decimal, instance identifier, for scalar MIB objects use &#x27;0&#x27;</div>
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
                        <div style="font-size: small; color: darkgreen"><br/>aliases: tag</div>
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
                                    <li>NULL</li>
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
                        <div style="font-size: small; color: darkgreen"><br/>aliases: val</div>
                </td>
            </tr>

    </table>
    <br/>


Notes
-----

.. note::
   - The SNMP set task will always return 'changed'
   - Tested against ubuntu 18.04 using net-snmp.
   - This module works with connection ``v1``, ``v2c``, ``v3_usm``.



Examples
--------

.. code-block:: yaml

    ---
    # Update 2 individual entries
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

    # Update the description of all interfaces matching a regex
    - name: Retrieve the index and name from the interface table
      ansible.snmp.walk:
        oids:
        - oid: IF-MIB::ifIndex
        - oid: IF-MIB::ifDescr
      register: if_indicies

    - name: Set a timestamp and the regex to use for matching interface names
      set_fact:
        ts: "{{ lookup('pipe', 'date -u +\"%Y-%m-%dT%H:%M:%SZ\"') }}"
        regex: "(Ethernet|Gigabit|Intel).*"

    - name: Update all matching interfaces
      ansible.snmp.set:
        oids:
        - oid: IF-MIB::ifAlias
          iid: "{{ iid }}"
          value: "Configured by ansible @ {{ ts }}"
      vars:
        matching_interfaces: "{{ lookup('ansible.utils.index_of', if_indicies.result, 'match', regex, 'ifDescr', wantlist=True) }}"
        iid: "{{ if_indicies['result'][int_id]['ifIndex'] }}"
      loop: "{{ matching_interfaces }}"
      loop_control:
        loop_var: int_id
      register: changes

    - name: Review all changes
      ansible.utils.fact_diff:
        before: "{{ interface.before.result|ansible.utils.to_paths }}"
        after: "{{ interface.after.result|ansible.utils.to_paths }}"
      loop: "{{ changes.results }}"
      loop_control:
        loop_var: interface
        index_var: idx
        label: "{{ idx }}"



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>after</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The result of an SNMP get for the OIDs after the set</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;raw&#x27;: {&#x27;description&#x27;: &#x27;The raw result from the snmp walk&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;list&#x27;, &#x27;elements&#x27;: &#x27;dict&#x27;, &#x27;entries&#x27;: {&#x27;iid&#x27;: {&#x27;description&#x27;: &#x27;The instance id&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;str&#x27;}, &#x27;tag&#x27;: {&#x27;description&#x27;: &#x27;The OID&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;str&#x27;}, &#x27;type&#x27;: {&#x27;description&#x27;: &#x27;The type of the value&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;str&#x27;}, &#x27;value&#x27;: {&#x27;description&#x27;: &#x27;The currently set value for the oid&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;raw&#x27;}}}, &#x27;result&#x27;: {&#x27;description&#x27;: &#x27;The transformed result from the snmp walk&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;list&#x27;, &#x27;elements&#x27;: &#x27;dict&#x27;, &#x27;entries&#x27;: {&#x27;_raw&#x27;: {&#x27;description&#x27;: &#x27;The individual oid entry and the currently set value&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;}}}}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>before</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The result of an SNMP get for the OIDs prior to set</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;raw&#x27;: {&#x27;description&#x27;: &#x27;The raw result from the snmp walk&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;list&#x27;, &#x27;elements&#x27;: &#x27;dict&#x27;, &#x27;entries&#x27;: {&#x27;iid&#x27;: {&#x27;description&#x27;: &#x27;The instance id&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;str&#x27;}, &#x27;tag&#x27;: {&#x27;description&#x27;: &#x27;The OID&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;str&#x27;}, &#x27;type&#x27;: {&#x27;description&#x27;: &#x27;The type of the value&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;str&#x27;}, &#x27;value&#x27;: {&#x27;description&#x27;: &#x27;The currently set value for the oid&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;raw&#x27;}}}, &#x27;result&#x27;: {&#x27;description&#x27;: &#x27;The transformed result from the snmp walk&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;, &#x27;type&#x27;: &#x27;list&#x27;, &#x27;elements&#x27;: &#x27;dict&#x27;, &#x27;entries&#x27;: {&#x27;_raw&#x27;: {&#x27;description&#x27;: &#x27;The individual oid entry and the currently set value&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;}}}}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>elapsed</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The amount of time in seconds spent for the snmp calls</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;post_set_get&#x27;: {&#x27;description&#x27;: &#x27;The amount of time spent in seconds for the get after the set&#x27;, &#x27;type&#x27;: &#x27;float&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;}, &#x27;pre_set_get&#x27;: {&#x27;description&#x27;: &#x27;The amount of time spent in seconds for the get prior to the set&#x27;, &#x27;type&#x27;: &#x27;float&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;}, &#x27;set&#x27;: {&#x27;description&#x27;: &#x27;The amount of time spent in seconds for the set&#x27;, &#x27;type&#x27;: &#x27;float&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;}, &#x27;total&#x27;: {&#x27;description&#x27;: &#x27;the amount of time spent on all snmp calls&#x27;, &#x27;type&#x27;: &#x27;float&#x27;, &#x27;returned&#x27;: &#x27;always&#x27;}}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)
