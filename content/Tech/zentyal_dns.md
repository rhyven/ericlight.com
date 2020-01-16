Title: Zentyal 6.0 to 6.1 upgrade getting stuck
Author: Eric Light
Tags: Tech, Security, Linux, Mail
Date: 2019-12-17

So I faced a little challenge with a [Zentyal](https://www.zentyal.com) server the other day.  I was upgrading from ye olde 6.0 to 6.1, when everything just stopped.  I let it sit in the corner for about an hour or so, but it never picked up the thread.  All the services were still live, so I logged in to have a look.

Running `ps aux`, I discovered this line:

    :::bash
    sh -c /usr/bin/sudo -p sudo: /var/lib/zentyal/tmp/x2M7gkZVvm.cmd 2> /var/lib/zentyal/tmp/stderr

So, I had a quick look at the contents of that stderr file:

    :::bash
    # cat /var/lib/zentyal/tmp/stderr 
    Password has expired
    dns-RIMU@ad.ericlight.com's Password: 

And what does that temp .cmd file contain?

    :::bash
    # cat /var/lib/zentyal/tmp/x2M7gkZVvm.cmd 
    kinit -k -t /var/lib/samba/private/dns.keytab dns-RIMU

Running that kinit command indeed prompts for a password reset, but the interesting thing is that samba-tool shows me this password shouldn't expire:

    :::bash
    # pdbedit -u dns-RIMU -v | grep change
    Password can change:  Wed, 31 Oct 2018 21:47:30 NZDT
    Password must change: never

... _riiiiiiight_, that's a bit interesting.  And yet I'm still being prompted to set a new password.  I used samba-tool to remind samba that this password shouldn't expire:

    :::bash
    # samba-tool user setexpiry dns-RIMU --noexpiry
    Expiry for user 'dns-RIMU' disabled.

And now...

    :::bash
    # pdbedit -u dns-RIMU -v | grep -i change
    Password can change:  Wed, 31 Oct 2018 21:47:30 NZDT
    Password must change: Tue, 19 Jan 2038 16:14:07 NZDT

Now I can run kinit against dns-RIMU perfectly fine, and indeed the Zentyal upgrade succeeded!

