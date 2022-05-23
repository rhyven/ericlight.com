Title: WireGuard - Part Two (VPN routing)
Author: Eric Light
Tags: Tech, Security, WireGuard, Networking, Linux
Date: 2017-06-11

This is a continuation of my brief series on the new [WireGuard](https://wireguard.com/) VPN.  [Part One]({filename}wg0.md) was about the simple building-blocks to get WireGuard working between two endpoints.  Now that we've got a couple machines able to ping each other by IP address, we can carry on a bit deeper into the inter-LAN routing stuff.

Extending on from the IP addresses in Part One, instead of JUST connecting to the remote machine, I want to actually have access to everything _on the whole 10.20.0.0/16 network_; even the non-WireGuard devices.  I want it to be like I'm there on-site.  The idea here is roughly:

* **Remote machine:** wg0: 10.20.40.1 (behind public IP 163.172.161.0)
* **Local machine:** wg0: 10.20.40.2 (with eth0 on 192.168.88.207)
* **Machines on remote LAN:** 10.20.0.0/16
* **Remote LAN WireGuard range:**  10.20.40.0/16 -- note this is within the remote 10.20.0.0/16 range

From my local machine, with minimal interaction, I want to be able to ping something like 10.20.**10.30**, and get a response.

Happily, now that the two endpoints are talking with each other, there's really not much that has to happen to get things working the way I want.

Remote Config
-------------

* Many Linux distros disable IPv4 packet forwarding by default.  But in this case, we very much want this enabled.  Edit your `/etc/sysctl.conf` file, and look for the line: `net.ipv4.ip_forward`, and set the value to 1.  You may need to add this line manually, or uncomment it.

* You'll also need to enable ProxyARP.  This is another kernel setting that's usually disabled, so edit `/etc/sysctl.conf`, and add the following line:  `net.ipv4.conf.all.proxy_arp = 1`.

* Reload your kernel settings.  A reboot will do the trick, or you could just run `sudo sysctl -p /etc/sysctl.conf`.


Starting WireGuard on Boot
--------------------------

There are a variety options to do this, and if you're a seasoned sysadmin you probably already have a favourite way.

One option is to add `post-up wg-quick up wg0` to the tail of your eth0 block (or appropriate interface) in /etc/network/interfaces.

A second option (for systemd users) is to simply run `systemctl enable wg-quick@wg0`.  This will tell systemd to bring the wg0 interface up once a network connection is established.

I only do this on the remote machine, because I don't want my local machine to be forever spinning up it's WireGuard connection; however I always want the remote machine listening for my packets.  That said, there's probably no reason to avoid this; I just haven't done it yet.


Local Config
------------

Here's the really cool bit.  Since your remote machine is now set up to perform IPv4 forwaring and ProxyARP, the only thing you need to change on the local side is a single number.  Or rather, a couple numbers.

* In your `/etc/WireGuard/wg0.conf` file, just expand the network range of your interface to include the entire remote LAN:

        [Interface]
        ...
        Address = 10.20.40.2/16
        
        [Peer]
        ...
        AllowedIPs = 10.20.0.0/16

* Now reload your WireGuard config, either by rebooting, or running `sudo wg-quick down wg0 && sudo wg-quick up wg0`.


That's all!  When you make the above changes, wg-quick will modify your routing table so that **any IP within 10.20.x.y** will be sent over the wg0 interface.  The remote host will dutifully forward the packet out into the rest of the network, and ProxyARP will take care of the rest:

    $ ping -c1 10.20.10.31
    PING 10.20.10.31 (10.20.10.31) 56(84) bytes of data.
    64 bytes from 10.20.10.31: icmp_seq=1 ttl=63 time=91.8 ms


Troubleshooting
---------------

Okay so by now there's a really good chance that you've bumped into trouble.  I've started on a basic [WireGuard troubleshooting guide]({filename}wg2.md), but it only covers the issues that I bumped into.  If you're still stuck after reading through that, ask a question on the WireGuard Mailing List, or reach out via IRC (#WireGuard on Freenode) - this is all on [the WireGuard website](https://www.wireguard.com/#contact-the-team).


Wrap-up
-------

That should be all!  When you reboot the remote server (I specify reboot, because you want to test that your solution can survive an outage at the remote site), you should be able to ping other things in the remote LAN without any additional interaction.  I still manually run `wg-quick up wg0` on my local laptop, because I don't want to be connected remotely _all_ the time.


Thanks
------

Huge gratitude to [Jason Donenfeld](https://www.zx2c4.com/) (aka zx2c4) for spending his time not only reading this post, but also for sending me some fantastic feedback!  I'd made some bungles in my original post on this topic, and he vastly helped my understanding.

If you do end up using WireGuard, _go forth and [donate](https://www.wireguard.com/#donations)_!  Seriously, **at very least**, send Jason the cost of a local cup of coffee or a beer for his efforts.

Also, huge gratitude to another Jason ([@rendition](https://keybase.io/rendition)) who has helped me develop from a junior network admin into a ... 'moderate' network admin.  I've learned more in the last year than I ever thought possible.  He's taught me nearly everything I know about managed networking, reviewed this post for me, and is actually the guy who introduced me to WireGuard originally!

