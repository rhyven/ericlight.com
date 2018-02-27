Title: Respecting Amavis' "Banned Extensions" setting
Author: Eric Light
Tags: Tech, Security, Linux, Mail
Date: 2017-08-13

I've been dabbling a little bit with [iRedMail](http://www.iredmail.org), mostly just to have a play with a mail server, but also to see what's involved in mail security.  iRedMail is a package that [pulls together](http://www.iredmail.org/docs/used.components.html) Postfix as an MTA, Dovecot as a POP3 & IMAP server, SOGo for ActiveSync, Roundcube for Webmail, SpamAssassin for spam protection, and ClamAV for virus scanning.

Okay I have **no idea** why I have to write this, but apparently it's a thing.

Amavis has a list of banned file extensions.  In Debian, they live in `/etc/amavis/conf.d/20-debian_defaults`, and `/etc/amavis/conf.d/50-user`, and are set in the `$banned_filename_re` variable.  THIS MAKES PERFECT SENSE.

But of course, there's always something that doesn't make sense, and that is the fact that there is a SQL backend (at least in the environment created by iRedMail), and settings in here take precedence over the Amavis config files somehow.

And even more bizarrely, there exists in this SQL environment, a policy setting entitled "_**banned\_files\_lover**_", which was set to "Y".  I shit you not.  My only hope is that this only defaults to "Y" for postmaster.

To fix this, you need to hop into the database, and update the appropriate column in the `policy` table:

    $ mariadb
    MariaDB [none]> \u amavis
    MariaDB [amavisd]> update policy set banned_files_lover="N";

And now, Amavis will obey your file extension filters!

Thankfully, I found this information at <http://www.iredmail.org/forum/topic13147-iredmail-support-amavisd-passed-but-setup-at-ddiscard.html> -- I never would have found it otherwise!
