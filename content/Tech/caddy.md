Title: Moving to the Caddy web server
Author: Eric Light
Tags: Tech, Security, Linux
Date: 2020-04-05
Modified: 2022-01-05


For the last couple of years I've been running this site, as well as my friend's site ([Under The Umbrella](https://www.undertheumbrella.co.nz)) on [Nginx](https://www.nginx.org).  Recently my VPS host decided to do away with their cheapest tier, so instead of doubling my annual cost, I hopped onto <https://www.lowendbox.com> and found myself a replacement Cheaps McGee VPS to host this.

Well, a major change like that is a great time to learn about something new, so I took the opportunity to get started with [Caddy](https://www.caddyserver.com).  If you don't already know about Caddy, it's a fast, simple, _clean_ web server.  It's written in Go, so it's both fast and memory safe.  And hey, it's super simple.

I'm not going to go into a whole lot of detail about setting up Caddy - there are enough tutorials out there already, and really I got all the info I needed from the website.  But here are some particularly notable bits:

The Caddyfile
========

This lives in `/etc/caddy/Caddyfile`:

```ini
ericlight.com, www.ericlight.com {

    file_server
    root * /var/www/ericlight.com

    import /etc/caddy/caddy_security.conf

    log {
       output file /var/log/caddy/access.log
       format single_field common_log
    }
}

undertheumbrella.co.nz, www.undertheumbrella.co.nz {

    file_server
    root * /var/www/undertheumbrella.co.nz

    import /etc/caddy/caddy_security.conf

    log {
        output file /var/log/caddy/utu_access.log
        format single_field common_log
    }
}
```

And, `/etc/caddy/caddy_security.conf` contains:
```ini
header {
    Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Xss-Protection "1; mode=block"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Content-Security-Policy "upgrade-insecure-requests"
        Referrer-Policy "strict-origin-when-cross-origin"
        Cache-Control "public, max-age=15, must-revalidate"
        Feature-Policy "accelerometer 'none'; ambient-light-sensor 'none'; autoplay 'self'; camera 'none'; encrypted-media 'none'; fullscreen 'self'; geolocation 'none'; gyroscope 'none';       magnetometer 'none'; microphone 'none'; midi 'none'; payment 'none'; picture-in-picture *; speaker 'none'; sync-xhr 'none'; usb 'none'; vr 'none'"
}

```
** Update 2022-01-05:** Previously I'd used `header / {` above; that should have been simply `header {`. Thanks [@JoHoffmann8](https://twitter.com/JoHoffmann8) for pointing this out! It's also worth mentioning that Caddy are deprecating the `common_log` log format, which makes me sad in one way, but I do get it - the Caddy json log file format is far richer, but I liked the easily-ingested syslog format. ¯\\\_(ツ)\_/¯

---

Ok so here's the thing.  Caddy really seems to implement Python's ethos of "Batteries Included".  The above contents are enough on their own to:

1. Host two separate static websites
1. Offer two subdomains for each of these websites 
1. Manage the entire certificate creation and renewal process from [Let's Encrypt](https://www.letsencrypt.org) for two sites, plus subdomains.
1. Get an A+ rating on both [SSL Labs](https://www.ssllabs.com/ssltest/) and [SecurityHeaders.io](https://www.securityheaders.io)(!!)
1. And, of course, zoink all the logs into separate files under /var/log/caddy


Creating a Caddy Service file
=========

**UPDATE 2020-05-07:  With the release of Caddy 2.0, it appears a regular `dpkg -i caddy.deb` will take care of creating the caddy.service file**

---

If you're running Debian, you'll need to create yourself a service file for systemd, so you can get your server to launch Caddy on boot.  I got mine from <https://github.com/caddyserver/dist/tree/master/init>:

`/etc/systemd/system/caddy.service`:

```ini
# This service file requires the following:
#
# 1) Group named caddy:
#      $ groupadd --system caddy
#
# 2) User named caddy, with a writeable home folder:
#      $ useradd --system \
#           --gid caddy \
#           --create-home \
#           --home-dir /var/lib/caddy \
#           --shell /usr/sbin/nologin \
#           --comment "Caddy web server" \
#           caddy
#
# 3) Caddyfile at /etc/caddy/Caddyfile that is
#    readable by the caddy user
#

[Unit]
Description=Caddy Web Server
Documentation=https://caddyserver.com/docs/
After=network.target

[Service]
User=caddy
Group=caddy
ExecStart=/usr/bin/caddy run --config /etc/caddy/Caddyfile --environ
ExecReload=/usr/bin/caddy reload --config /etc/caddy/Caddyfile
TimeoutStopSec=5s
LimitNOFILE=1048576
LimitNPROC=512
PrivateTmp=true
ProtectSystem=full
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
```

Preventing scans
======

Everything above is already pretty secure - Caddy is really good at making security super easy.  On top of that, Caddy is the only service hosted on this box, there's no dynamic code (all raw HTML and CSS, thanks to [Pelican](https://getpelican.com)), and the only things listening to the internet are SSH and Caddy itself.  But even then, I get tired of seeing hundreds of scan reports every day.  [Fail2Ban](https://www.fail2ban.org/) to the rescue.

`/etc/fail2ban/filter.d/caddy-4xx.conf`:
```
[Definition]
failregex = ^<HOST>.*"(GET|POST).*" (404|444|403|400) .*$
ignoreregex =
```

`/etc/fail2ban/jail.local`:
```
[caddy-4xx]
port    = http,https
logpath = /var/log/caddy/access.log
          /var/log/caddy/utu_access.log
enabled = true
banTime = 3600
findTime = 600
maxretry = 5
```

Fin!
====

And that's all!  I had another tweak or two to my Pelican Makefile, to point rsync to the right server, but overall that was an incredibly simple process.  The Caddy team have done a spectacular job.
