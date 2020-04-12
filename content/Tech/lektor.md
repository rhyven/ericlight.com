Title: Making Lektor work with grsecurity
Author: Eric Light
Tags: Security, Tech, Linux
Date: 2016-10-29

I started using [grsecurity](https://grsecurity.net/) on my servers in 2015, and there's always a bit of [tuning](https://wiki.archlinux.org/index.php/Grsecurity) [required](http://hardenedlinux.org/system-security/2016/01/10/hardening-your-desktop-linux-mint-with-grsec.html).

I was recently playing with [Lektor](https://www.getlektor.com) (before I swapped to [Pelican](https://www.getpelican.com)), and I had a bit of trouble with my grsec kernel.  In particular, Lektor and Pelican are both run within a virtualenv Python environment, and grsec eats it like popcorn in two different ways:

1) TPE (Trusted Path Execution) throws a wobbly:

`[253241.370019] grsec: From {ssh-origin-ip}: denied untrusted exec (due to file in world-writable directory) of /tmp/#50 by /usr/local/lib/lektor/bin/lektor[lektor:60593] uid/euid:1000/1000 gid/egid:1000/1000, parent /bin/bash[bash:60581] uid/euid:1000/1000 gid/egid:1000/1000`

This block occurs because the virtualenv violates grsecurity's Trusted Path Execution protection - the Python executable isn't under a trusted path, and the user isn't in the TPE-bypass group.

To resolve this one, add your user to the TPE group.  This will allow the user to execute binaries which aren't in trusted locations:

**`sudo usermod -aG grsec-tpe $USER`**


2) RWX protection.  This is a common problem with Python-based apps, even though Python has an exception (Edit 2020-04-12 - Issue 6 from <https://github.com/thestinger/paxd/> has been deleted) by default.

`[  207.534876] grsec: From {ssh-source-ip}: denied RWX mmap of <anonymous mapping> by /usr/local/lib/lektor/bin/lektor[lektor:534] uid/euid:1000/1000 gid/egid:1000/1000, parent /bin/bash[bash:477] uid/euid:1000/1000 gid/egid:1000/1000`

First, create your PaX ELF headers, and then disable grsec's MEMPROTECT extension on the included python2 binary, while you enable EMUTRAMP:

**`sudo paxctl /usr/local/lib/lektor/bin/python2 -c`  
`sudo paxctl /usr/local/lib/lektor/bin/python2 -Em`**

Result!
