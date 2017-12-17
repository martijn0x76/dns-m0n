dns-m0n
=======

Summary
-------

Simple Python script to alert on DNS changes.

Install
-------

* $ git clone https://github.com/martijn0x76/dns-m0n.git
* $ cd dns-m0n
* $ pip install -r requirements.txt
* $ ./dns-m0n.py

Usage
-----

```
Usage: ./dns-m0n.py
```

Output example
--------------
```
dns-m0n by @martijn0x76 - Keeps an eye on DNS records

Checking: www.security.nl      | Current: 82.94.191.109, Before: 82.94.191.109
```

```
dns-m0n by @martijn0x76 - Keeps an eye on DNS records

Checking: www.security.nl      | Current: 82.94.191.109, Before: 1.1.1.1 >>modified<<

Number of detected changes: 1
```

TODO
----

* Support for names that resolve to multiple IP's and round-robin DNS
* Support for NS,MX and TXT records
* Save the complete config in the SQLite database
