Title: iRedMail, SpamAssassin, and Lynis
Author: Eric Light
Tags: Tech, Linux, Mail, Security
Date: 2020-11-02

I really like iRedMail, and I also really like Lynis.

However, they don't exactly like _each other_... or, more accurately, some of Lynis' recommendations can cause a couple iRedMail components to fail.  Today we're talking about SpamAsassin.

One of the suggestions from Lynis is to turn off the 'execute' bit on compilers for users who aren't either the owner or in the owner group (the 'other' execute bit).  For example:

    :::bash
    root@server:/# chmod o-x /usr/bin/as
    root@server:/# chmod o-x /usr/bin/gcc

Easy peasy!  But once you do this, you might start getting the following in your daily iRedMail Cron reports:

    :::text
    /etc/cron.daily/spamassassin:
    /bin/sh: 1: x86_64-linux-gnu-gcc: Permission denied
    make: *** [Makefile:346: body_0.o] Error 126
    command 'make PREFIX=/tmp/.spamassassin23046Zmmrr9tmp/ignored INSTALLSITEARCH=/var/lib/spamassassin/compiled/5.028/3.004002 >>/tmp/.spamassassin23046Zmmrr9tmp/log' failed: exit 2

There are probably a bunch of ways to fix this.  My way, I'm sure, is not the best way... however it was quick and easy, and it worked.

    :::bash
    root@server:/# chgrp debian-spamd /usr/bin/as
    root@server:/# chgrp debian-spamd /usr/bin/gcc
    root@server:/# runuser -l debian-spamd -c sa-compile

Look ma, no more errors!

This solution really *only* works for me because debian-spamd is the only non-root user that calls these compilers.  If I had another user which needed to call them, I'd have to come up with a better fix.  But for a standalone iRedMail server, this does the trick!
