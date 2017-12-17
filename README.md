dns-m0n
=======

Inspired by [this](https://blog.fox-it.com/2017/12/14/lessons-learned-from-a-man-in-the-middle-attack/) nice blogpost about a MitM attack on [Fox-IT](https://www.fox-it.com/en/) last September.

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
echo customerportal.mydomain.com >> ./names.txt
```

```
Usage: ./dns-m0n.py
```

Run as a cronjob every minute
```
* * * * * /usr/bin/python /path/dns-m0n.py
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
