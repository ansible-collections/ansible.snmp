# Ansible SNMP Collection

[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/ansible.snmp)](https://codecov.io/gh/ansible-collections/ansible.snmp)

The Ansible `ansible.snmp` collection includes a variety of plugins for using SNMP on the control node to make SNMP connections to a device.

<!--start requires_ansible-->

## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.

<!--end requires_ansible-->

## Included content

<!--start collection content-->
### Connection plugins
Name | Description
--- | ---
[ansible.snmp.v1](https://github.com/ansible-collections/ansible.snmp/blob/main/docs/ansible.snmp.v1_connection.rst)|Make SNMP v1 connections to a device
[ansible.snmp.v2c](https://github.com/ansible-collections/ansible.snmp/blob/main/docs/ansible.snmp.v2c_connection.rst)|Make SNMP v2c connections to a device
[ansible.snmp.v3_usm](https://github.com/ansible-collections/ansible.snmp/blob/main/docs/ansible.snmp.v3_usm_connection.rst)|Make SNMP v3 user-based security model (USM) connections to a device.

### Modules
Name | Description
--- | ---
[ansible.snmp.get](https://github.com/ansible-collections/ansible.snmp/blob/main/docs/ansible.snmp.get_module.rst)|Perform an SNMP get against a remote device for one or more OIDs
[ansible.snmp.set](https://github.com/ansible-collections/ansible.snmp/blob/main/docs/ansible.snmp.set_module.rst)|Perform an SNMP set against a remote device for one or more OIDs
[ansible.snmp.walk](https://github.com/ansible-collections/ansible.snmp/blob/main/docs/ansible.snmp.walk_module.rst)|Perform an SNMP walk against a remote device for one or more OIDs

<!--end collection content-->

## Installing this collection

You can install the `ansible.snmp` collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install ansible.snmp

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: ansible.snmp
```

## Using this collection

The most common use case for this collection is to retrieve operation state information from a device using `SNMP get` or `SNMP walk`

**NOTE**: For Ansible 2.9, you may not see deprecation warnings when you run your playbooks with this collection. Use this documentation to track when a module is deprecated.

### See Also:

- [Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) in the Ansible documentation for more details.

## Contributing to this collection

This collection is intended for plugins that are not platform or discipline specific. Simple plugin examples should be generic in nature. More complex examples can include real world platform modules to demonstrate the utility of the plugin in a playbook.

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [ansible.utils collection repository](https://github.com/ansible-collections/ansible.utils). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for complete details.

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

### Developer notes

- 100% code coverage is the goal, although it's not always possible. Please include unit and integration tests with all PRs. PRs should not cause a decrease in code coverage.
- Filter plugins should be 1 per file, with an included DOCUMENTATION string, or reference a lookup plugin with the same name.
- Action, filter, and lookup plugins should use argspec validation. See [AnsibleArgSpecValidator](https://github.com/ansible-collections/ansible.utils/blob/main/plugins/module_utils/common/argspec_validate.py).
- Use of the latest version of black is required for formatting (black -l79)
- The README contains a table of plugins. Use the [collection_prep](https://github.com/ansible-network/collection_prep) utilities to maintain this.

### Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Release notes

<!--Add a link to a changelog.md file or an external docsite to cover this information. -->

Release notes are available [here](https://github.com/ansible-collections/ansible.utils/blob/main/changelogs/CHANGELOG.rst)
For automated release announcements refer [here](https://twitter.com/AnsibleContent).

## Roadmap

For information on releasing, versioning and deprecation see the [stratergy document](https://access.redhat.com/articles/4993781).

In general, major versions can contain breaking changes, while minor versions only contain new features (like new plugin addition) and bugfixes.
The releases will be done on an as-needed basis when new features and/or bugfixes are done.

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Installing the python binding for net-snmp

#### Using dnf

```
sudo dnf install net-snmp net-snmp-libs net-snmp-utils net-snmp-python
```

or

#### Using source (fedora)

- download https://sourceforge.net/projects/net-snmp/files/net-snmp/5.9.1/net-snmp-5.9.1.tar.gz/download
- extract `tar -xvf net-snmp-5.9.1.tar.gz`
- as root `sudo su -`
- cd `cd net-snmp-5.9.1`
- set the path to system python
- configure `./configure --with-python-modules --libdir=/usr/lib64 --enable-shared`
- make `make`
- install `sudo make install`
- add the install path to ld

```
more /etc/ld.so.conf.d/netsnmp.conf
/usr/local/lib
```

- cd `python`
- build `python setup.py build`
- install `python setup.py install` or `python setup.py install --user`
- confirm `python -c 'import netsnmp'`
- It's installed in system python

#### Configuring netsnmp

- `sudo dnf install perl-Term-ReadLine-Gnu`
- `snmpconf -p`
  - 1: snmp.conf
  - 4: Textual mib parsing
  - 1: Specifies directory to be searched for mibs
  - Enter the list of directories to search through for mibs: +/home/bthornto/cisco_mibs
  - finished
  - finished
  - quit
- review `~/.snmp/snmp.conf`

#### Using the net-snmp python bindings with a python virtual environment

- `python3 -m venv venv --system-site-packages`

or install again after sourcing venv

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install net-snmp-5.9.1/python`

#### Good stuff to read

- [net-snmp bindings](https://github.com/net-snmp/net-snmp/blob/master/python/README)
- dump MIBs into other formats, including python classes [libsmi](https://www.ibr.cs.tu-bs.de/projects/libsmi/smidump.html?lang=de)
- Cisco MIB ftp details [here](https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/9226-mibs-9226.html#q2)
- SNMP table traversal [here](https://datatracker.ietf.org/doc/html/rfc1187#page-2)
