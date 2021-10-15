## SNMP poc work

### Installing net-snmp

#### Using dnf

```
sudo dnf uninstall net-snmp net-snmp-libs net-snmp-utils net-snmp-python
```

or 

#### Using source
- download https://sourceforge.net/projects/net-snmp/files/net-snmp/5.9.1/net-snmp-5.9.1.tar.gz/download
- extract `tar -xvf net-snmp-5.9.1.tar.gz`
- cd `cd net-snmp-5.9.1`
- configure `./configure`
- make `make`
- install `sudo make install`
- add the install path to ld

```
more /etc/ld.so.conf.d/netsnmp.conf 
/usr/local/lib
```

- cd `python`
- build `python setup.py build`
- install `python setup.py install --user`
- confirm `python -c 'import netsnmp'`
- It's installed in system python

### Get some mibs

- `mkdir ~/cisco_mibs`
- `cd ~/cisco_mibs`
- `ftp -nv ftp.cisco.com`
- `user anonymous`
- `password email@company.com`
- ` cd pub/mibs/v2`
- `prompt`
- `mget *`

### Configure netsnmp

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



### Using net-snmp with venv

- `python3 -m venv venv --system-site-packages`

or install again after sourcing venv

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install net-snmp-5.9.1/python` 
