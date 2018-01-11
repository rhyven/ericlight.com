Title: RingZer0team CTF - Linux Sysadmin challenges
Author: Eric Light
Tags: Security, Tech, RingZer0Team
Date: 2017-05-28

There are a bunch of fantastic Capture The Flag security challenges on [RingZer0Team.com](https://www.ringzer0team.com).  I've been working through some of these for a wee while now, and with the [New Zealand Cyber Security Challenge](https://www.cybersecuritychallenge.org.nz/) coming up again soon, I thought I'd get back into some of them.

The Sysadmin Linux series of challenges is where you're trying to breach the security of a Linux system.  I actually finished most of these last year, but I wanted to finish my last two.  Of course, to get to the last two stages, you need to use the flags from the _previous_ stages.  So I'm revisiting them.

Level 1 - Morpheus -> Trinity
-----------------------------

We start by SSH'ing into a particular user account on the ringzer0team server:

    You have mail.
    Last login: Thu Apr 27 02:52:40 2017 from <somewhere>
    morpheus@forensics:~$ 

There's only one file in the home folder, and I can't read it.  There's a /home/trinity folder with full read access, but also nothing legible.

The flag for level 1 is found by running ps aux, which reveals what appears to be Trinity's password:

    root      3241  0.0  0.0   4188   572 ?        S    Jan14   1:44 /bin/sh /root/backup.sh -u trinity -p Flag-<redacted>

Level 2 - Morpheus -> Architect
-------------------------------

Aha, and the flag for level two is in /etc/fstab, which contains what appears to be The Architect's password, in base64:

    /dev/sr0        /media/cdrom0   udf,iso9660 user,noauto     0       0
    /dev/fd0        /media/floppy0  auto    rw,user,noauto  0       0
    #//TheMAtrix/phone  /media/Matrix  cifs  username=architect,password=$(base64 -d "<redacted>"),iocharset=utf8,sec=ntlm  0  0

Level 3 - The Architect
-----------------------

Level 3 requires you to log on as architect, using the password we discovered earlier.  The only clue is "dig for password".

This bit got a bit harder.  There are a couple possible hints in architect's mail file, including a bunch of attempts to mount a cifs volume, and reference to a file in /backup/.

Digging through the files in /backup left me at a loss.  There are references to /tmp/Gathering.py, but that's a challenge for later (cypher's challenge).  After some digging I located /var/tmp/.swl, which contained some MySQL credentials!

    mysql> show tables;
    +----------------+
    | Tables_in_arch |
    +----------------+
    | arch           |
    | flag           |
    +----------------+
    2 rows in set (0.00 sec)
    
    mysql> select * from arch;
    +------+-----------------------+
    | id   | arch                  |
    +------+-----------------------+
    |    1 | The one               |
    |    1 | The null one          |
    |    1 | The mother of the one |
    |    1 | The father of the one |
    |    1 | The flag of the one   |
    |    1 | The null one          |
    +------+-----------------------+
    6 rows in set (0.00 sec)  
    
    mysql> select * from flag;
    +---------------------------------+
    | flag                            |
    +---------------------------------+
    | FLAG-<redacted>                 |
    +---------------------------------+
    1 row in set (0.00 sec)


Yasss after a solid hour of digging, I've found the flag for the third level!

Level Four - Morpheus -> Oracle
-------------------------------

Again we're logging on as morpheus, but this time the goal is to access the oracle account.

Lots of tasty stuff under /var/tmp/.viminfo, now that I've found it.  References to files in /backup/, to /tmp/Gathering.py, /tmp/mail_cypher

Don't make the mistake of trying to cat .swo; it'll eat your console session.

Found this interesting thing in mail, but it's not helpful:  `forensics.localdomain : Apr 14 21:14:33 : morpheus : user NOT in sudoers ; TTY=pts/4 ; PWD=/home/trinity ; USER=root ; COMMAND=/usr/sbin/usermod -aG neo morpheus`

In one of the /backup files, I found the remains of an SSH key, and it worked!  Access to the oracle account achieved.  In the home folder, we've got a handy-dandy Base64-encoded flag in flag.txt.

Level Five - Oracle Encrypted File
----------------------------------

There's a file in the oracle home folder named encflag.txt.enc:

    U2FsdGVkX1+dCl4WEHNJKBqA8a4fQeheOgA7oiNmjwlJQvGaQAgqcIsGRIcbdHKF
    heSs51JRSEmOLqVyGvoxDA--

Decoding the base64 returns a binary blob, prefixed with the string "Salted".  This is one of the levels that I never completed originally, so maybe it's time to give it another crack.

A quick google of "salted base64" reveals an [interesting comment on StackExchange](https://security.stackexchange.com/a/124333).  Apparently I'm looking at a file encrypted with the OpenSSL 'enc' command, so I first copy the file to my own computer to work.

I discover that the command `openssl enc -in testfile -d -a` will un-base64 it, then load the file in.  I need to pass it a password to decrypt with though, so now I need to find that.

Oh my god I just did `cat .*` in the oracle home folder and literally found an alias that reads and decrypts the file.  I can't believe that took me almost an hour.

There are no words.

Level Six - Trinity -> Neo
--------------------------

Okay getting serious now.  Using Trinity's account, I need to find the password for the neo account.

It's a bit noisy on login:

    You have mail.
    Last login: Tue Apr 25 16:29:29 2017 from <le blah>
    -bash: hello: command not found
    Sup Neo!
    ls: cannot open directory /home/neo: Permission denied
    cat: phonebook: Permission denied

A vague tickle in my memory prompted me to run sudo -l right off the bat.  Rewarded with:

    User trinity may run the following commands on this host:
        (neo) /bin/cat /home/trinity/*

So of course I immediately run `sudo -u neo /bin/cat /home/trinity/*`

This gives us a 'phone book' containing:

	The Oracle        1800-133-7133
	Persephone        345-555-1244
	
	
	
	
	
	copy made by Cypher copy utility on /home/neo/phonebook

Trinity's .bashrc contains a bit of kruft:


	hello neo
	echo "Sup Neo!"
	$(ls -lart /home/neo)
	cat phonebook

Really not useful.  I remember finding Trinity's password with `ps aux`:

    root      3241  0.0  0.0   4188   572 ?        S    Jan14   1:47 /bin/sh /root/backup.sh -u trinity -p Flag-08grILsn3ekqhDK7cKBV6ka8B

It looks a little bit like a MySQL connection string, so I try that but no dice.  Nothing under /var/tmp this time, and grep doesn't find anything useful under the /backup goldmine.

There's some weirdness under /etc/passwd.  I don't know what this means, but saving it for later:

    trinity:x:1002:1002:trinity,%,lsdf(940998+(n.~,3):/home/trinity:/bin/bash

I looked through the mail file, but nothing jumped out at me there.  Also trawled again through /backup, as well as /var/backups.  Then /etc and /var.  Argh.

Finally I start looking for Persephone.  Nothing helpful, but it reminds me of the last line in the phonebook.

copy made by Cypher copy utility on /home/neo/phonebook

And then I remember that the sudo command allows a * at the end of the cat command, which might allow me to do path traversal...

    sudo -u neo /bin/cat /home/trinity/../neo/phonebook

Finally, after a whole hour of digging, I'm awarded Neo's password!


Level 7 - Neo is Not Alone
--------------------------

I don't know what this clue means, but I bet it has something to do with Persephone.  Persephone comes from Greek mythology as one of Zeus' daughters, and the goddess of the underworld.  Does that help me here?  I don't know, it's getting late...

I run `cat .*` in Neo's home directory to see if there's anything hiding there, but no luck this time.  Also nothing for `sudo -l`.

There's an unreadable file (owned by root) called 'result.stat', that's probably related to something.  I browse the mail history and see:

    forensics.localdomain : Dec  7 14:08:08 : neo : user NOT in sudoers ; TTY=pts/2 ; PWD=/home/neo ; USER=morpheus ; COMMAND=/home/morpheus/egrep /home/morpheus/../neo/result.stat

That could be handy.  I do remember an egrep in /home/neo, will have a look.  Lots of reference to /bin/monitor, too. 

I'm only in the neo group, so nothing to see there.

Running `ps aux | grep neo` shows a heap of /bin/monitor processes started by root, but running under neo.  There's also a "SCREEN" instance there, but running `screen -D -RR` doesn't reclaim it, so something's up there.  I'm pretty sure there's something there in /bin/monitor.

In all honesty this one had me beat.  It was half-past midnight and I was exhausted.  I knew that there was something special about /bin/monitor, and I knew there was something special about the fact that it was running as neo.  But I took the expedient route and had a quick google.  I found the answer at [http://blog.dornea.nu/2016/10/30/ringzer0-ctf-sysadmin-linux/](http://blog.dornea.nu/2016/10/30/ringzer0-ctf-sysadmin-linux/) - without this I could have been looking for years.  However, as is so often the case, this tutorial was the basis of some great learning for me.

Because the process is owned by neo, and because /bin/monitor could be _read_ by neo, it meant I could run a stack trace.  *I have never done this before* - no false impressions here, I totally relied on that dornea.ru page to tip me off to the usage of strace.  But once I knew that, I had the flag.

I was very well misled by this one, actually.  The Persephone comment in the phonebook totally led me down the wrong path, and I spent quite a long time searching for her details on the system.  It was the reddest herring possible.

Level 8 - Morpheus -> Cypher
----------------------------

Okay it's late now so I'm going to try to thrash this one quick.  Nothing in `ps aux` for cypher.  Grepping /backup found a python file and a dump showing a cron job runs this file every minute.  The contents of the python file are:

    import os
    os.system('ps aux > /tmp/28JNvE05KBltE8S7o2xu')

I can't read the output file, but I can edit the python script!  This is gonna be easy.

After a little bit of trial and error, I edited the python script to first list the contents of the /home/cypher folder, and after that, to output the contents of /home/cypher/flag.txt

It's important to note that the python file is recreated every three minutes when it's run, so you need to redo your changes for every iteration.

Fin
===

That's the end!  I'm quite pleased I've managed to finish all of the Sysadmin Linux section.  Of course that's also scary, because it means I need to break into the other sections.  That's OK though... it's a good time to do it!

