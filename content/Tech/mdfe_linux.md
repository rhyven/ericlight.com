Title: Microsoft Defender for Endpoint (mdatp) on Debian Sid
Author: Eric Light
Tags: Tech, Linux
Date: 2021-07-07
Modified: 2021-08-01

** 2021-08-01 Update: ** 

This is a better string to find out what's hitting your audit log: `cat /var/log/audit/audit.log* | cut -d ' ' -f26 | sort | uniq -c | sort -n | tail -n 6 | head -n5`

---

Linux doesn't have many great antivirus options available. 

Don't get me wrong, there are actually a few options nowadays. We've got the ever-present [ClamAV](https://www.clamav.net/); [BitDefender](https://www.bitdefender.com) has a good reputation, but I haven't played with it yet; [Sophos AV](https://www.sophos.com/en-us/support/documentation/sophos-anti-virus-for-linux.aspx?) for Linux _seems_ to be in limbo. [ESET for Linux](https://www.eset.com/int/home/antivirus-linux/) exists, as does [Symantec Endpoint Protection](https://techdocs.broadcom.com/us/en/symantec-security-software/endpoint-security-and-management/endpoint-protection/all/getting-up-and-running-on-for-the-first-time-v45150512-d43e1033/installing-clients-with-save-package-v16194723-d21e1502/installing-the-client-for-linux-v95193124-d21e2986.html) for Linux. That's a pretty decent range - but they each have some real drawback. Assuming the price is right, you still see compatibility, usability, licensing dramas, or resource drain challenges.

Most recently, the Linux version of [Microsoft Defender for Endpoint](https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/microsoft-defender-endpoint-linux?view=o365-worldwide) entered the playing field. I finally got to play with this and I gotta say...

_Holy shit._

Look, I know we enjoy ragging on Microsoft. They've demonstrated some awful behaviour over the years, and every action still harkens back to the "Embrace, Extend, Extinguish" _modus operandi_. But they're doing really great work with the Defender/DATP/MDFE/whatever line. Even the basic Defender has been steading climbing the ranks, to the point where virtually _all_ guidance I've heard for the last two years is: "if you're not going full EDR, just use regulr Defender". It's no SentinelOne or CrowdStrike, but overall Defender just Gets The Job Done.

So, I was excited to try the Linux version. Long story short, it was a dream. The installation process was _streaks ahead_ of the competition. Resource usage is generally negligible, adding an average load of around 0.5% CPU, going up to about 16% CPU during a scan. There's a robust health and connectivity test built-in. Basically the whole thing just works, to the same level we've learned to expect from the Windows version. Oh and this one has **actual documentation** which seems to be considered optional by some of the competitors. 🙃

However.

You may find that mdatp is frantically scanning files that freqently Do Things. Bind9 (named) for example, might be handling hundreds of queries a minute. Each one of them triggers _not only_ an mdatp scan, but also auditd entries... which often logs more than once per query. I was finding logs being filled and rotated **every seven minutes** in some cases... and then punctuated by auditd yelling "my buffer is full, I can't log all these events!".

So as a result, I've spent quite a few hours learning how to wrangle auditd around exclusions.  Here's what I've learned:

# You need to lie to install MDFE on Sid

Edit `/etc/os-release` and change `VERSION_ID="11"` to `VERSION_ID="10"`. After that, you can install MDFE following the regular instructions. Don't forget to change it back later! 


# Troubleshooting performance issues:

_See also: <https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/linux-support-perf?view=o365-worldwide>_

First step - find the processes that mdatp is spending the most CPU time on:

``` bash
# Download Microsoft's parser (only do this once)
wget -c https://raw.githubusercontent.com/microsoft/mdatp-xplat/master/linux/diagnostic/high_cpu_parser.py

# Ask Defender to output the stats, and then parse it looking for high CPU:
$ mdatp diagnostic real-time-protection-statistics --output json | python high_cpu_parser.py
925 	mongodb		29184
37575	pulseaudio	47
21355	packagekitd	30
37588	dbus-daemon	26
37550	sshd		25
```

... Yikes, it's probably not necessary to scan MongoDB thirty thousand times! You can exclude a process from mdatp like this: `sudo mdatp exclusion process add --path /usr/bin/mongod`

But that's not all... even though mdatp is no longer **scanning** the application, you still have auditd frantically logging _every single thing it does_. That's also going to cause periodic slowdowns as the auditd buffer fills up, overflows, panicks, and then purges the stuff it couldn't write down.

## Syslog/audit logging issues

You can find out if anything is spewing a billion entries into your audit log, by just grepping for the rotation in syslog:

``` bash
# grep 'Audit daemon rotating' /var/log/syslog
Jul  6 01:00:08 spam auditd[28996]: Audit daemon rotating log files
Jul  6 04:00:05 spam auditd[28996]: Audit daemon rotating log files
Jul  6 06:57:01 spam auditd[28996]: Audit daemon rotating log files
Jul  6 09:57:18 spam auditd[28996]: Audit daemon rotating log files

```

... Filling up a log file every three hours is _weird_, but previously this server was doing it every few minutes. You can see what's causing all the log rotations with:

``` bash
# cat /var/log/audit/audit.log* | cut -d ' ' -f26 | sort | uniq -c
 138581 
      1 exe="/bin/bash"
      4 exe="/bin/hostname"
      2 exe="/bin/nano"
    684 exe="/lib/systemd/systemd"
   4754 exe="/lib/systemd/systemd-logind"
    209 exe="/lib/systemd/systemd-user-runtime-dir"
    119 exe="/opt/microsoft/mdatp/sbin/osqueryi"
      9 exe="/usr/bin/apt-get"
   2133 exe="/usr/bin/dbus-daemon"
  13212 exe="/usr/bin/perl"
  10784 exe="/usr/bin/pmxcfs"
     14 exe="/usr/bin/rrdcached"
      2 exe="/usr/bin/sort"
      4 exe="/usr/lib/postfix/sbin/cleanup"
    880 exe="/usr/lib/postfix/sbin/pickup"
    175 exe="/usr/lib/postfix/sbin/qmgr"
     27 exe="/usr/lib/postfix/sbin/smtp"
      4 exe="/usr/lib/postfix/sbin/trivial-rewrite"
     16 exe="/usr/sbin/cron"
  10326 exe="/usr/sbin/ebtables-legacy"
  10326 exe="/usr/sbin/ebtables-legacy-restore"
      3 exe="/usr/sbin/postdrop"
      5 exe="/usr/sbin/qmeventd"
      2 exe="/usr/sbin/sendmail"
     56 exe="/usr/sbin/smartd"
   3255 exe="/usr/sbin/sshd"
```

The number on the left shows the number of times that binary has had it's activity logged. This should clearly show the problem executables... today we're looking at `perl`, `pmxcfs`, and `ebtables-legacy`. Once you've got that, you need to determine which *syscalls* are part of regular noise:

```bash
# grep /usr/bin/pmxcfs /var/log/audit/audit.log* | cut -d ' ' -f 4 | sort | uniq -c
  10856 
   8142 syscall=263
   1357 syscall=43
   1357 syscall=84
```

Referring to [this document](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/), we can see these syscalls are sys_accept, sys_rmdir, and sys_unlinkat. Since pmxcfs is the ProxmoxVS Cluster File System, these are frankly all pretty normal syscalls for it to make.  Let's ignore them.

`echo -a never,exit -S 43 -S 84 -S 263 -F exe=/usr/bin/pmxcfs -k exclude_PVE_internals >> /etc/audit/rules.d/01-exclusion.rules`

^ Gotta do that as root, btw, or just append the line however you see fit. Once you've added exclusions for all of your high-noise entires, run `service auditd restart` and then `service auditd status` to make sure it worked properly.

On my Zentyal box I had to add a bunch of entries to exclude logging of certain high-noise things. For example, DNS query resolution (via named) and Samba activity:

``` text
cat /etc/audit/rules.d/01-exclusion.rules

-a never,exit -S 41 -S 42 -S 49 -S 82 -S 288 -F exe=/usr/sbin/named -k exclude_DNS_queries
-a never,exit -S 43 -F exe=/usr/sbin/winbindd -k exclude_Samba
-a never,exit -S 41 -S 42 -S 43 -S 87 -F exe=/usr/sbin/smbd -k exclude_Samba
-a never,exit -S 41 -S 43 -S 87 -F exe=/usr/sbin/samba -k exclude_Samba
```

**A word of warning:**  Don't just ignore everything willy-nilly. The audit logging system _exists_ so you can track activity on the system - blithely sending 100% of the log entries to the bin will undermine what the audit sytem exists for!


... That's all I've got so far. I'll keep updating this if I bump into anything new!
