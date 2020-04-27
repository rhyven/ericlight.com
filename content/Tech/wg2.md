Title: WireGuard - Part Three (Troubleshooting)
Author: Eric Light
Tags: Tech, Security, WireGuard, Networking, Linux
Date: 2017-06-12

This is part of my [brief]({filename}wg0.md) [series]({filename}wg1.md) on [WireGuard](https://wireguard.com/).  I'm pretty enamoured with WireGuard and the way it works, but there were a couple slightly curly bits that I needed to get my head around.  This troubleshooting guide is a rough dump of the issues I had, and how I fixed them.


Gotten Stuck?
-------------

At this stage, there are actually a few ways that this can go wrong, even though we haven't done much.  Think through all the bits:

* Installed WireGuard at both ends
* Set up your NAT rule on the remote side
* Created a private and public key on each side
* Put each public key in the opposite side's [Peer] config
* Put a suitable IP address on each side


Troubleshooting
---------------

There are, actually, a myriad of ways this can fail:

* Broken routing on the client PC
* Broken NAT on the remote router
* Broken routing on the remote PC
* Broken wg0 configuration on one side
* Lack of TCP forwarding on the remote computer
* Lack of Proxy ARP on the remote computer

If you can't ping the remote server yet, don't panic.  Run tcpdump to find out what you're missing.

* On the remote server:  `tcpdump -i wg0`
* On your local machine: `ping -c1 10.20.40.1`

That will tell you whether your packets are reaching the remote server, or if they're not getting through the tunnel.

If they're not making it through the tunnel at all, you'll probably be seeing error messages in the ping.  For example:

    PING 10.20.10.1 (10.20.10.1) 56(84) bytes of data.
    From 10.20.40.2 icmp_seq=1 Destination Host Unreachable
    ping: sendmsg: Required key not available

That's the error message I got when I set AllowedIPs too strictly.  Because I was trying to ping something that was **routable**, but wasn't within the AllowedIPs range, there was no applicable key for the packet.


Thanks
------

Huge gratitude to [Jason Donenfeld](https://www.zx2c4.com/) (aka zx2c4) for spending his time not only reading this post, but also for sending me some fantastic feedback!  I'd made some bungles in my original post on this topic, and he vastly helped my understanding.

Also, huge gratitude to another Jason ([@rendition](https://keybase.io/rendition)) who has helped me develop from a junior network admin into a ... 'moderate' network admin.  I've learned more in the last year than I ever thought possible.  He's taught me nearly everything I know about managed networking, reviewed this post for me, and is actually the guy who introduced me to WireGuard originally!
