Title: sa-compile failing during upgrade
Author: Eric Light
Tags: Tech, Linux
Date: 2020-03-15

I just spent an hour troubleshooting the most ridiculous thing.  I guess to help people search, I'd describe this as "dpkg failing at sa-compile in Debian 10" but that's really not a good picture of what's happening here...

```bash
Setting up sa-compile (3.4.2-1~deb9u3) ...
Running sa-compile (may take a long time)
/bin/sh: 1: x86_64-linux-gnu-gcc: Permission denied
make: *** [body_0.o] Error 126
command 'make PREFIX=/tmp/.spamassassin22062Ifq5yDtmp/ignored INSTALLSITEARCH=/var/lib/spamassassin/compiled/5.024/3.004002 >>/tmp/.spamassassin22062Ifq5yDtmp/log' failed: exit 2
dpkg: error processing package sa-compile (--configure):
subprocess installed post-installation script returned error exit status 25

<-- snip -->

Errors were encountered while processing:
  sa-compile
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

In my defence, it seemed similar to a recurring issue I've had on this server in the past, (which I now promise to address in a separate post).  That's why I ended up on a red herring hunt.

Anyway, I spent a bunch of time trying to troubleshoot dpkg and Python, before realising that a few months ago I'd installed [Lynis](https://cisofy.com/lynis) and worked through a bunch of the hardening recommendations.

... One of which is restricting the execute permissions on /usr/bin/gcc.  Which is a symlink to /usr/bin/gcc-6.  Which is a symlink to x86_64-linux-gnu-gcc-6.

```bash
root@x:/usr/bin# ls -l x86_64-linux-gnu-gcc-6
-rw-r--r-- 1 root root 949016 Feb 15  2018 x86_64-linux-gnu-gcc-6
```

Yes.  I was experiencing problems compiling things because I'd removed execute permissions for all users on the compiler I needed, and I'd spent an hour ignoring the "Permission denied" error that told me where to look.

Fixed with a simple `chmod 744 /usr/bin/x86_64-linux-gnu-gcc-6`.

