Title: Wireguard - Part One (Installation)
Author: Eric Light
Tags: Tech, Security, Wireguard, Networking, Linux
Date: 2017-06-03
Modified: 2017-06-11

[Wireguard](https://wireguard.io/) is the most excellent VPN stack around.  It's _really_ fast, the concept of Cryptokey Routing is awesome, and I love the speed and simplicity benefits that come from opionionated cryptography.  The protocol is so simple - expressed in a mere 4k lines of code - that it's auditable by anyone.

**But.**

With my initial naive approach, I found myself using HTTPS, over ports forwarded over SSH tunnels, connected over Wireguard.  Although it was straightforward to get Wireguard working between two endpoints, I ended up in nested-crypto hell.

So, this brief series is about making Wireguard work as a VPN onto a different site.  We'll start by making it work between two endpoints, and [we'll go forward from there]({filename}wg1.md).  My end goal is to have access to all the resources on a remote site, just by running `wg-quick up wg0`. 

The endpoints I'm going to set up are at:

* **Remote machine:** wg0: 10.20.40.1 (behind public IP 163.172.161.0)
* **Local machine:** wg0: 10.20.40.2


NAT Setup
---------

Chances are, your remote endpoint is behind a firewall of some sort.  Pick a high port, and configure your firewall to forward UDP packets on that port through to your remote Wireguard endpoint.  You don't need to do this on your local side, because reply traffic from the remote side will generally be handled by the stateful session part of your firewall.

Many routers and firewalls offer port address translation (also known as PAT) as part of port forwarding or NAT.  This is when a packet hits the firewall on (say) port 57432, and the firewall puts it on the LAN to port 22, for example.  You don't want this.  I think it's possible with Wireguard, but it adds complexity without benefit.


Config - Remote Site
--------------------

* [Install Wireguard](https://www.wireguard.io/install/)
* Generate your keys.  The following will create a public key and a stub config in /etc/wireguard/:

        cd /etc/wireguard
        umask 077
        printf "[Interface]\nPrivateKey = " > wg0.conf
        wg genkey | tee -a wg0.conf | wg pubkey > publickey

* Edit your config to match:

        [Interface]
        PrivateKey = WhAt3v3R=      (this is the private key generated on this machine)
        ListenPort = 12345          (this is the UDP port you've forwarded from your firewall)
        Address = 10.20.40.1/24     (this will be the IP given to the wg0 interface)
        
        [Peer]
        PublicKey = (leave this blank for now; you'll paste in your local public key here soon)
        AllowedIPs = 10.20.40.0/24  (this is the range of Wireguard IP addresses that this Peer's key can be used from)

* That should be all you need to configure on the remote side for now.  Save your wg0.conf file, and bring the interface up:

        wg-quick up wg0
        ping -c1 10.20.40.1

* You should see a bunch of actions performed by wg-quick, and a reply packet from your ping.  Now onto the local side.


Config - Local Machine
----------------------

* Install Wireguard and generate your keys, as per the first two steps above.
* Edit your configuration again:

        [Interface]
        PrivateKey = WhAt3v3R+PaRt-tw0=    (this is the private key generated on this machine)
        ListenPort = 12345                 (this is the UDP port again; I don't think they have to be the same)
        Address = 10.20.40.2/24            (note - different IP address, but in the same range)
        
        [Peer]
        PublicKey = ??????????             (copy the public key from the REMOTE server here)
        Endpoint = 163.172.161.0:12345     (enter the PUBLIC IP address of the remote site, plus the forwarded port)
        AllowedIPs = 10.20.40.0/24         (specifying that packets using this key must come from within 10.20.40.x)

* Now that you've got a local public key, take a second to paste it into the Peer public key section on the remote server.
* Once you're finished you should be able to bring the interface up and ping it:

        wg-quick up wg0
        ping -c1 10.20.40.2

* ... and you should even be able to ping the remote server as well:

        ping -c1 10.20.40.1


Gotten Stuck?
-------------

At this stage, there are actually a few ways that this can go wrong, even though we haven't done much.  Here's a quick summary of everything we've done:

* Installed Wireguard at both ends
* Set up your NAT rule on the remote side 
* Created a private and public key on each side
* Put each public key in the opposite side's [Peer] config
* Put a suitable IP address on each side

If you've nailed each of those and you're still having trouble, you can have a quick look at the brief Troubleshooting guide I've put together as [Part Three]({filename}wg2.md).


Onto Part Two
-------------

That should be all you need to get Wireguard working between two machines on two different sites.  So far we haven't done anything either interesting or uncommon - this is all the basic stuff you'll find on the [Wireguard Quick Start](https://www.wireguard.io/quickstart/) page, although expressed slightly differently.  [The next article]({filename}wg1.md) will be a bit more about intra-site routing.


Thanks
------

Huge gratitude to [Jason Donenfeld](https://www.zx2c4.com/) (aka zx2c4) for spending his time not only reading this post, but also for sending me some fantastic feedback!  I'd made some bungles in my original post on this topic, and he vastly helped my understanding.

If you do end up using Wireguard, _go forth and [donate](https://www.wireguard.io/#donations)_! Seriously, **at very least**, send Jason the cost of a local cup of coffee or a beer for his efforts.

Also, huge gratitude to another Jason ([@rendition](https://keybase.io/rendition)) who has helped me develop from a junior network admin into a ... 'moderate' network admin.  I've learned more in the last year than I ever thought possible.  He's taught me nearly everything I know about managed networking, reviewed this post for me, and is actually the guy who introduced me to Wireguard originally!

