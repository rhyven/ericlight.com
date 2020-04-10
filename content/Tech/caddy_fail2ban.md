Title: Using Fail2Ban to insta-block malicious hits
Author: Eric Light
Tags: Tech, Security, Linux
Date: 2020-04-07

Okay so a few days ago I [posted]({filename}caddy.md) about adopting [Caddy](https://www.caddyserver.com).  

Of course, anyone who hosts anything knows that accessible services on the internet will start getting hit by scanners within literal moments of being accessible.  On the very first night of having my site live on the new VPS, Logwatch informed me of a bunch of attempts to access wp-admin.php.  Sigh.

Well, this entire site is built with my favourite static site generator [Pelican](https://www.getpelican.com).  That means I don't have any PHP on my site whatsoever.  Why not just... block anyone that tries to open a PHP page at ericlight.com?  [Fail2Ban](https://www.fail2ban.org) to the rescue.

Two things we need:  A Fail2Ban filter, and a Fail2Ban jail.

The Filter
----

`nano /etc/fail2ban/filter.d/caddy-php.conf`  _(note, the name of this file must be the same as the identifier in your `jail.local` file)_

```ini
[Definition]
failregex = ^<HOST>.*\.php(\s|\?.*)HTTP.*$
ignoreregex =
```

... that will catch anything in your logs such as:

```
nn.nn.nn.nn - - [07/Apr/2020:23:20:39 +1200] "GET /wp-admin.php HTTP/2.0" 404 0
nn.nn.nn.nn - - [06/Apr/2020:10:12:24 +1200] "GET /index.php?s=index/%5Cthink%5Capp/invokefunction&function=call_user_func_array&vars%5B0%5D=phpinfo&vars%5B1%5D%5B%5D=1 HTTP/1.1" 404 0
nn.nn.nn.nn - - [06/Apr/2020:12:51:31 +1200] "GET /wp-login.php HTTP/1.1" 404 0
```

The Jail
----

`nano /etc/fail2ban/jail.local`

```ini
[caddy-php]
port    = http,https
logpath = /var/log/caddy/access.log
enabled = true
maxretry = 1
```

Note I used `maxretry = 1` there.  This means if an IP triggers that filter _a single time_, they'll be blocked **immediately**...  So you probably don't want to do this just willy-nilly. 

The Result
----

With those two parts done (and the obligatory `service fail2ban reload`, of course), you should find that your web server immediately bans any host that tries to load a .php file from your website!

```log
# tail -f /var/log/caddy/access.log /var/log/fail2ban.log
==> /var/log/caddy/access.log <==
1xx.1xx.1xx.11 - - [07/Apr/2020:23:25:55 +1200] "GET /arse.php HTTP/1.1" 404 0
1xx.1xx.1xx.6 - - [07/Apr/2020:23:25:57 +1200] "GET /arse.php?1234 HTTP/1.1" 404 0
1xx.2xx.6x.1xx - - [07/Apr/2020:23:26:03 +1200] "GET /blargh.php HTTP/2.0" 404 0

==> /var/log/fail2ban.log <==
2020-04-07 23:25:55,482 fail2ban.filter         [452]: INFO    [caddy-php] Found 1xx.1xx.1xx.11 - 2020-04-07 23:25:55
2020-04-07 23:25:55,551 fail2ban.actions        [452]: NOTICE  [caddy-php] Ban 1xx.1xx.1xx.11
2020-04-07 23:25:58,309 fail2ban.filter         [452]: INFO    [caddy-php] Found 1xx.1xx.1xx.6 - 2020-04-07 23:25:57
2020-04-07 23:25:58,782 fail2ban.actions        [452]: NOTICE  [caddy-php] Ban 1xx.1xx.1xx.6
2020-04-07 23:26:03,627 fail2ban.filter         [452]: INFO    [caddy-php] Found 1xx.2xx.6x.1xx - 2020-04-07 23:26:03
2020-04-07 23:26:04,010 fail2ban.actions        [452]: NOTICE  [caddy-php] Ban 1xx.2xx.6x.1xx
```

Great success!  You can use the `banTime` directive to adjust how long these blocks should last for - I've got mine set up to block for an hour.

Edit 2020-04-10:
---

Eh I realised that my RegEx missed these lovely things:

```log
[ip redacted] - - [08/Apr/2020:16:14:10 +1200] "GET /wp-config.php.new HTTP/1.1" 404 0
[ip redacted] - - [08/Apr/2020:16:14:14 +1200] "GET /wp-config.php.old HTTP/1.1" 404 0
[ip redacted] - - [08/Apr/2020:16:14:17 +1200] "GET /wp-config.php.bak HTTP/1.1" 404 0
[ip redacted] - - [08/Apr/2020:16:14:19 +1200] "GET /wp-config.php.backup HTTP/1.1" 404 0
[ip redacted] - - [08/Apr/2020:16:14:22 +1200] "GET /wp-config.php.save HTTP/1.1" 404 0
```

... so yeah I just changed it to drop anything with `.php` in the URL.  I'll try to remember not to post any articles with .php in the URL lol.


Credits
---

Thanks to Phage and Xyphoid for the help in fine-tuning my rusty RegEx!
