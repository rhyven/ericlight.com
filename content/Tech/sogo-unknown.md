Title: iRedMail: Daily user unknown entries from backup_sogo.sh 
Author: Eric Light
Tags: Tech, Linux, Mail
Date: 2020-11-01

If you've been running iRedMail for a while, eventually you'll probably start seeing 'user unknown' events in your daily logs:

    :::text
    * Backup all users' data under /var/vmail/backup/sogo/2020/11/01
    <0x0x5574a64c36b0[SOGoCache]> Cache cleanup interval set every 300.000000 seconds
    <0x0x5574a64c36b0[SOGoCache]> Using host(s) '127.0.0.1' as server(s)
    2020-11-01 09:29:12.784 sogo-tool[29749:29749] user 'abdulm' unknown
    2020-11-01 09:29:12.786 sogo-tool[29749:29749] user 'bent' unknown
    2020-11-01 09:29:12.786 sogo-tool[29749:29749] user 'brettr' unknown
    2020-11-01 09:29:12.786 sogo-tool[29749:29749] user 'catalinar' unknown
    2020-11-01 09:29:12.787 sogo-tool[29749:29749] user 'clinth' unknown
    2020-11-01 09:29:12.787 sogo-tool[29749:29749] user 'danield' unknown
    2020-11-01 09:29:12.787 sogo-tool[29749:29749] user 'dannyn' unknown
    2020-11-01 09:29:12.788 sogo-tool[29749:29749] user 'darcyk' unknown
    2020-11-01 09:29:12.788 sogo-tool[29749:29749] user 'davidl' unknown
    * Compress backup files.

This is because removal of an iRedMail user doesn't remove the corresponding SOGo user data.  You can take care of this with `sogo-tool`:

    :::bash
    root@server:/# sogo-tool remove abdulm@<domain.xyz> bent@<domain.xyz> brettr@<domain.xyz>

... etc.  Once you're done, run the backup again to make sure you've got them all:

    :::bash
    root@server:/# /bin/bash /var/vmail/backup/backup_sogo.sh
    * Backup all users data under /var/vmail/backup/sogo/2020/11/01
    <0x0x563fd0e2b6b0[SOGoCache]> Cache cleanup interval set every 300.000000 seconds
    <0x0x563fd0e2b6b0[SOGoCache]> Using host(s) '127.0.0.1' as server(s)
    * Compress backup files.

