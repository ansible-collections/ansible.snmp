.. _ansible.snmp.v1_connection:


***************
ansible.snmp.v1
***************

**Make SNMP v1 connections to a device**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Make SNMP v1 connections to a device.



Requirements
------------
The below requirements are needed on the local Ansible controller node that executes this connection.

- python bindings for netsnmp


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>community</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"public"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>community = public</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_COMMUNITY</div>
                                <div>var: ansible_snmp_community</div>
                    </td>
                <td>
                        <div>Specific the community string for SNMP v1 connections.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"inventory_hostname"</div>
                </td>
                    <td>
                                <div>var: ansible_host</div>
                    </td>
                <td>
                        <div>Specifies the remote device FQDN or IP address for the SNMP connection to.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">161</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[defaults]<br>remote_port = 161</p>
                            </div>
                                <div>env:ANSIBLE_REMOTE_PORT</div>
                                <div>var: ansible_port</div>
                    </td>
                <td>
                        <div>Specifies the port on the remote device that listens for SNMP connections.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>retries</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">3</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>retries = 3</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_RETRIES</div>
                                <div>var: ansible_snmp_retries</div>
                    </td>
                <td>
                        <div>Specify the number retries before failure</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>retry_no_such</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>retry_no_such = no</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_RETRY_NO_SUCH</div>
                                <div>var: ansible_snmp_retry_no_such</div>
                    </td>
                <td>
                        <div>If enabled NOSUCH errors in &#x27;get&#x27; pdus will be repaired, removing the entry in error, and resent, undef will be returned for all NOSUCH varbinds, when set to `False` this feature is disabled and the entire get request will fail on any NOSUCH error.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">500000</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>timeout = 500000</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_TIMEOUT</div>
                                <div>var: ansible_snmp_timeout</div>
                    </td>
                <td>
                        <div>Specify the number of micro-seconds before a retry</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>version</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>1</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify the SNMP version</div>
                </td>
            </tr>
    </table>
    <br/>








Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
