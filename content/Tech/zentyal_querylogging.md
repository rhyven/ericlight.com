Title: Logging DNS queries, for both pfSense and Zentyal server
Author: Eric Light
Tags: Tech, Security, Linux
Date: 2020-12-06

Logs of your client DNS queries can be a really good tool for incident response.  I've finally got this implemented but it was much more of a struggle than I expected it to be, so here's my story!

We've got a pfSense firewall running as a DNS fowarder, and a [Zentyal](https://www.zentyal.com) server running BIND9 as the authoritative local server.  The firewall rules block all UDP/53, so all DNS queries go either directly to the firewall, or (more commonly) to the Zentyal server for resolution.  This means we have two places that resolve DNS queries which we want to forward off to our syslog server.

## pfSense

Unbound is a _super_ simple DNS forwarder, and the configuration is wonderfully straightforward.  It did take me quite a while to figure it out, but in the end it was a simple oversight on my part.

To get pfSense/Unbound to forward DNS queries to your syslog server, simply open the Services -> DNS Resolver page, click 'Display Custom options', and add these two lines:

    :::ini
    server:
    log-queries: yes

I spent hours fiddling before I realised I was missing the empty "server:" directive.  -__-

This will log all DNS queries that Unbound deals with.  These logs go to the standard internal pfSense log; if you want them to be replicated off to an external syslog server, go Status -> System Logs -> Settings.  Scroll down to the "Remote Log Servers" section and add your syslog server there.  (I'm not covering syslog listener config in this particualar post!)

## Zentyal

Yeah this one was harder to figure out.  Because Zentyal overwrites the config at _every damn opportunity_, you can't just edit `/etc/bind/named.conf.options`, like what you find in [most articles](https://www.thegeekdiary.com/how-to-enable-bind-query-logging-to-find-out-whos-querying-a-name-server/)... it may work for a moment, but it'll be overwritten.

The real answer to editing Zentyal's config files is outlined at <https://doc.zentyal.org/en/appendix-c.html#stubs>:

    :::bash
    cp /usr/share/zentyal/stubs/dns/named.conf.options.mas /etc/zentyal/stubs/dns/named.conf.options.mas

Once you've copied the stub into a place where it won't be clobbered, edit it and zoom right down to the bottom line, which looks like:

    :::ini
    logging { category lame-servers { null; }; };

This is the line you need to replace.  Now, you can go as ham as you want here.  I've actually used the sample provided by ISC themselves, which you can find at <https://kb.isc.org/docs/aa-01526>.  However, that's really robust and possibly more than you may need.  A bare minimum would probably look like:

    :::ini
    logging { 
        channel queries_log {
            syslog named;
            print-time yes;
            print-category yes;
            print-severity yes;
            severity info;
        };
    };

Note - when I tried to use the ISC sample wholesale, I needed to change a couple small things:

1.  Changed all `/var/named/log` output destinations to `/var/log/named`
1.  The lines for `category zoneload` and `category trust-anchor-telemetry` need to be removed for Zentyal 6.2's version of BIND9 
1.  I needed to create `/var/log/named`, and make sure it was writeable by the bind user

I think that covers it, I hope this helps someone!  I've actually even taken the time today to create a [Pull Request](https://github.com/zentyal/zentyal/pull/2005) in the Zentyal GitHub, we'll see if it ends up getting merged!
