Title: Making Amavis work with ESET Antivirus
Author: Eric Light
Tags: Tech, Security, Linux, Mail
Date: 2017-08-12

I've been dabbling a little bit with [iRedMail](http://www.iredmail.org), mostly just to have a play with a mail server, but also to see what's involved in mail security.  iRedMail is a package that [pulls together](http://www.iredmail.org/docs/used.components.html) Postfix as an MTA, Dovecot as a POP3 & IMAP server, SOGo for ActiveSync, Roundcube for Webmail, SpamAssassin for spam protection, and ClamAV for virus scanning.

But of course, ClamAV has [shown disappointing performance](https://www.av-test.org/en/news/news-single-view/linux-16-security-packages-against-windows-and-linux-malware-put-to-the-test/), and it would be really nice to use something more... commercially suitable.

To tie together mail receipt and scanning, iRedMail uses [Amavis](https://www.ijs.si/software/amavisd/) (strictly speaking, 'amavisd-new').  Amavis uses ClamAV by default, but it comes with a bunch of [configuration blocks](https://www.apt-browse.org/browse/ubuntu/trusty/main/all/amavisd-new/1:2.7.1-2ubuntu3/file/etc/amavis/conf.d/15-av_scanners) to bring together other antivirus applications.

But although amavisd-new is stable and still maintained, some parts of it are really old.  In particular, many of these av-scanner config blocks are... uhh... "deprecated".  There's one particular entry for ESET that is dated 2002 - things have changed a lot in the last fifteen years.  \*shudder\*

So, with the help of [some documentation](https://www.akadia.com/download/documents/amavisd.conf.txt), I managed to piece together a code block that works:

    ['ESET File Security for Linux',
      ['/opt/eset/esets/sbin/esets_scan','esets_scan'],
      '--subdir --unsafe --unwanted --clean-mode=strict {}',
      [0,10,100],[1,50],
      qr/threat="([^"]+)"/m
    ],

That would be the end of the story, except I also had to hunt around to find out the right place to put my beautiful codeblock into.  It turns out that Debian's Amavis config structure is quite different to the CentOS config that is most-frequently mentioned in the iRedMail forums.  I spent a lot of time playing with `/etc/amavis/conf.d/15-av_scanners`, and nothing seemed to work.  Eventually I found out that Debian features a `/etc/amavis/conf.d/50-users` file that overwrites the settings from `15-av_scanners`.  Finally I had progress!

Somewhere around line 154 in `/etc/amavis/conf.d/50-users`, you'll find an `@av_scanners` codeblock.  I deleted the ClamAV section in there, and replaced it with the ESET codeblock above.  I left the ClamAV settings in the `@av_scanners_backup` section, because Amavis will fall back to that if ESET fails.

That seems to be all!  At least, it works with the [EICAR anti-malware test file](http://www.eicar.org/85-0-Download.html).
