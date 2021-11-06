Title: Acronis Cyber Protect and Microsoft Defender on the same Linux system
Author: Eric Light
Tags: Tech, Linux
Date: 2021-11-07

A few months ago, I [published what I learned]({filename}mdfe_linux.md) from playing with the Linux version of [Microsoft Defender for Endpoint](https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/microsoft-defender-endpoint-linux?view=o365-worldwide) a few months back. If you're here, you'll have possibly already read my original post. There was a bit of tuning required to get it to behave nicely; just adding some sensible audit logging exclusions. 

Well the Acronis Cyber Protect backup platform has recently been added to the bundle, and it had a few specific requirements, so I've documented them here.

There are four Acronis processes which MDATP will spend a lot of time scanning and rescanning. Exclude those from the scanning engine by executing the following commands as root:

``` bash
mdatp exclusion process add --path /usr/lib/Acronis/Schedule/schedul2-bin
mdatp exclusion process add --path /usr/lib/Acronis/APL/active-protection
mdatp exclusion process add --path /opt/acronis/aakore
mdatp exclusion process add --path /usr/lib/Acronis/BackupAndRecovery/mms
```

There are also five processes which need to be excluded from auditctl, unless you want your audit logs rotated every ten minutes. Again, these must all be run as root.

``` bash
echo -a never,exit -S 41 -S 42 -F comm="mms" -k exclude_acronis >> /etc/audit/rules.d/01-exclusion.rules
echo -a never,exit -S 41 -S 42 -S 43 -F comm="adp-agent" -k exclude_acronis >> /etc/audit/rules.d/01-exclusion.rules
echo -a never,exit -S 41 -S 42 -S 43 -S 288 -F exe=/usr/lib/Acronis/APL/active-protection -k exclude_acronis >> /etc/audit/rules.d/01-exclusion.rules
echo -a never,exit -S 41 -S 42 -S 43 -F exe=/opt/acronis/bin/updater -k exclude_acronis >> /etc/audit/rules.d/01-exclusion.rules
echo -a never,exit -S 41 -S 42 -S 288 -F exe=/opt/acronis/aakore -k exclude_acronis >> /etc/audit/rules.d/01-exclusion.rules
```

Once you've created the exclusions, you can either reboot or run `service auditd restart`. Either way, make sure you run `service auditd status` to ensure nothing went wrong with the exclusions.


