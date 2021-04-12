Title: Blocking bad extensions and extortion with iRedMail
Author: Eric Light
Tags: Tech, Security, Linux, Mail
Date: 2021-04-12

Turns out this is my third Amavis article.  I guess it's just one of those systems.

_Heads up, if you're trying to do this, make sure you also read [my other article]({filename}/Tech/amavis2.md) about the "banned\_files\_lover" thing._

Today I'm on a mission to:
1. Drop all incoming Office '97 files (they're predominantly malicious these days)
1. Drop all incoming Macro-enabled Office 2007+ files (there aren't legitimate reasons to receive these _in my scenario_)
1. Drop any emails containing a .onion address
1. Drop any emails containing a bitcoin wallet

Dropping Attachments
---

The attachment block is easily handled by Amavis.  In iRedMail on Debian, the configuration file is found at `/etc/amavis/conf.d/50-user`.  Open your config file, and scroll down to the section where the `$banned_filename_re` variable is set.  Insert the following line:

``` text
 qr'.\.(doc|dot|docm|docb|xls|xlm|xlt|xlsm|xlsb|
        xla|xlam|ppt|pps|pptm|potm|ppam|ppsm|sldm)$'i,           # Office '97-2003 and Macro-enabled files
 qr'.\.(adn|accdb|accdr|accdt|accda|mdw|accde|mam|maq|mar|mat|
        maf|laccdb|ade|adp|mdb|cdb|mda|mdn|mdt|mdf|mde|ldb)$'i,  # Microsoft Access files
 qr'^\.pub$',                                                    # Microsoft Publisher files


```

That will block all core Office '97-2003 files, as well as all Macro-enabled Office 2007-365 files.

By default, this will **silently** reject mails containing these attachments.  If you want senders to receive a bounce message, search for the `$final_banned_destiny` variable and make sure it's set to `D_BOUNCE`.

Dropping .onion and BTC
---

This part happens in Postfix, and it's more-super-easy than the last bit.  To configure Postfix's body checks, edit `/etc/postfix/body_checks.pcre`.  I simply added the following:

``` text
/(\w+\.onion)/ REJECT This mail server does not accept references to .onion addresses (${1})
/(\b(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39})/ DISCARD Bitcoin wallet detected (${1})

```

I used the REJECT directive for testing, but to be honest I don't want to send bounces back to these people, so I changed to DISCARD after it was working.  You can see the difference above.

The text after the REJECT directive is returned to the sender, and the text after the DISCARD directive is logged.  The variable `${1}` contains the detected string, and is appended to the response message.

That's the end!  Safety.  Yes.

Acknowledgements
===

Thanks to Brad and Hamish for this post - Brad for the regex, Hamish for the idea, and both of them for the review!
