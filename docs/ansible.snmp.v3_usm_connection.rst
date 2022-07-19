.. _ansible.snmp.v3_usm_connection:


*******************
ansible.snmp.v3_usm
*******************

**Make SNMP v3 user-based security model (USM) connections to a device.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Make SNMP v3 user-based security model (USM) connections to a device.



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
                    <b>auth_pass</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>context = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_AUTH_PASS</div>
                                <div>var: ansible_snmp_auth_pass</div>
                    </td>
                <td>
                        <div>Specify the SNMP v3 authentication passphrase.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>auth_proto</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>MD5</b>&nbsp;&larr;</div></li>
                                    <li>SHA1</li>
                                    <li>SHA-192</li>
                                    <li>SHA-256</li>
                                    <li>SHA-284</li>
                                    <li>SHA-512</li>
                        </ul>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>context = MD5</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_AUTH_PROTO</div>
                                <div>var: ansible_snmp_auth_proto</div>
                    </td>
                <td>
                        <div>Specify the SNMP v3 authentication protocol.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>context</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>context = </p>
                            </div>
                                <div>env:ANSIBLE_SNMP_CONTEXT</div>
                                <div>var: ansible_snmp_context</div>
                    </td>
                <td>
                        <div>Specify the SNMP v3 context name.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>context_engine_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>sec_level = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_CONTEXT_ENGINE_ID</div>
                                <div>var: ansible_snmp_context_engine_id</div>
                    </td>
                <td>
                        <div>Specify the SNMP v3 context engine ID.</div>
                        <div>Will be probed if not supplied.</div>
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
                    <b>priv_pass</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>priv_proto = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_PRIV_PASS</div>
                                <div>var: ansible_snmp_priv_pass</div>
                    </td>
                <td>
                        <div>Specify the SNMP v3 privacy passphrase.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>priv_proto</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>DES</b>&nbsp;&larr;</div></li>
                                    <li>AES128</li>
                                    <li>AES256</li>
                        </ul>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>priv_proto = DES</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_PRIV_PROTO</div>
                                <div>var: ansible_snmp_priv_proto</div>
                    </td>
                <td>
                        <div>Specify the SNMP v3 privacy protocol.</div>
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
                                <div>var: ansible_snmp_RETRIES</div>
                    </td>
                <td>
                        <div>Specify the number retries before failure</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sec_engine_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>sec_name = VALUE</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_SEC_ENGINE_ID</div>
                                <div>var: ansible_snmp_sec_engine_id</div>
                    </td>
                <td>
                        <div>Specify the SNMP v3 security engine ID.</div>
                        <div>Will be probed if not supplied.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sec_level</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>noAuthNoPriv</b>&nbsp;&larr;</div></li>
                                    <li>authNoPriv</li>
                                    <li>authPriv</li>
                        </ul>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>sec_level = noAuthNoPriv</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_SEC_LEVEL</div>
                                <div>var: ansible_snmp_sec_level</div>
                    </td>
                <td>
                        <div>Specify the SNMP v3 secutiry level.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sec_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"initial"</div>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[ansible.snmp]<br>sec_name = initial</p>
                            </div>
                                <div>env:ANSIBLE_SNMP_SEC_NAME</div>
                                <div>var: ansible_snmp_sec_name</div>
                    </td>
                <td>
                        <div>Specify the SNMP v3 security name.</div>
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
                                    <li><div style="color: blue"><b>3</b>&nbsp;&larr;</div></li>
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
