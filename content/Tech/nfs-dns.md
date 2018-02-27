Title: When the problem is DNS: FreeNAS and NFS
Author: Eric Light
Tags: Tech, Linux
Date: 2018-01-07

I discovered a while ago that NFS requires DNS to function correctly: <https://bugs.freenas.org/issues/4983>

That's somewhat annoying, because when your DNS server goes down (and your backups are stored on your FreeNAS server and accessed over NFS), is precisely the time when you really want your backups to be accessible.

However, turns out it doesn't _aaaaactuallyyyyy_ need DNS... it needs **name resolution**.  Specifically, FreeNAS just needs to be able to resolve it's own hostname.  Cue the handy-dandy hosts file.

Under Network -> Global Configuration -> Host name data base, add your details:

    192.168.88.5    backupserver backupserver.local backupserver.ad.mydomain.com

If you have a secondary IP address, duplicate the above line and replace the IP as appropriate.

Obviously, replace the hostname and your internal domain name with whatever you use.  However, be aware that the .local FQDN is **actually** required, even if you use a different domain name.
