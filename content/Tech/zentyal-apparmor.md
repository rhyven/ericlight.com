Title: When AppArmor eats your breakfast
Author: Eric Light
Tags: Security, Tech, Linux
Date: 2018-03-19

I've knocked heads with AppArmor a few times now.  To be quite honest with myself, I think it's primarily because I install it, enable all the plugins, and then forget it's there until there's a problem.

**TL;DR:**

On a fully-updated Zentyal 5.0 system running DHCP, the AppArmor profile in /etc/apparmor.d/usr.sbin.dhcpd **will prevent isc-dhcp-server from restarting itself after an upgrade**.

More search-type words:  Zentyal dhcp server doesn't start again after upgrade.  isc-dhcp-server graceful shutdown, but no restart.

This frustration-laden, Google-friendly equivalent of speaking slowly and clearly should illustrate how impossible it was for me to find guidance on this.

To fix:
```
# aa-complain /etc/apparmor.d/usr.sbin.dhcpd 
```

---

Okay, now that the TL;DR is finished, here's the rest of the story:

Unfortunately there's **always** a problem with AppArmor eventually.

Even worse, _the problem is often silent_.  I'll just find that, for example, NONE of my man pages work.  Or logrotate will fail.  For example, here's what happens when you enable aa-enforce mode on your friendly resident user manual:

```
 $ man
 What manual page do you want?
 $ sudo aa-enforce /etc/apparmor.d/usr.bin.man
 Setting /etc/apparmor.d/usr.bin.man to enforce mode.
 $ man
 $man: can't open the manpath configuration file /etc/manpath.config
```

If I hadn't enabled `aa-enforce` immediately before that, what would *you* have done?  You would have gone ahead, made sure that manpath.config existed, made sure it wasn't corrupted, maybe tried running `man` as root... maybe even copied a manpath.config file from a known-working computer.  But, hidden within `dmesg` is our old friend:

`[149929.763064] type=1400 audit(1521449052.257:111): apparmor="DENIED" operation="open" profile="/usr/bin/man" name="/etc/manpath.config" pid=22633 comm="man" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0`

And that example is actually better than it used to be - quite a few times in the past four years, I've received this:

    $ man
    $

... from a fully-updated Debian system.

<br/><br/>
_This makes me sad._
<br/><br/>

Or, in one particular case, _ISC-DHCP-SERVER_ of all things will launch perfectly well, but will fail to restart after a package update, and the first thing I'll notice is "o hai all the things is broken halp plz".  Something like that.

When you're troubleshooting DHCP, you'll probably check systemctl, leases table, maybe /var/log ... But when you get around to checking `dmesg`, you may notice the root of the problem:

From dmesg -T:

```
[Sat Mar 17 03:44:28 2016] audit_printk_skb: 18 callbacks suppressed
```

Considering the update occurred at 03:44am, this is probably our problem.  I can't see *for sure*, but I'm pretty certain those 18 suppressed callbacks are filled with "DENIED" log lines.

The fix is simple:

```
# aa-complain /etc/apparmor.d/usr.sbin.dhcpd 
Setting /etc/apparmor.d/usr.sbin.dhcpd to complain mode.
```

And your isc-dhcp-server should now restart gracefully after it's scheduled upgrades!

