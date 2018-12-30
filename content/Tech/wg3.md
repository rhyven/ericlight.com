Title: New things I didn't know about Wireguard
Author: Eric Light
Tags: Tech, Security, Wireguard, Networking, Linux
Date: 2018-12-31

This is part of my [brief]({filename}wg0.md) [series]({filename}wg1.md) [on]({filename}wg2.md) [Wireguard](https://wireguard.io/).  I'm pretty enamoured with Wireguard and the way it works, and I've been using it pretty seamlessly for over a year now.  I've learned a couple things that weren't immediately obvious though, so I'm documenting them here.

Easy Provisioning 
-----------------

Samuel Holland mentioned an interesting trinket, in his post at <https://lists.zx2c4.com/pipermail/wireguard/2018-December/003703.html>:

*"[...] WireGuard will ignore a peer whose public key matches the interface's private key. So you can distribute a single list of peers everywhere."*

You can combine this with `wg addconf` like this:

 - Each peer has its own `/etc/wireguard/wg0.conf` file, which only contains it's `[Interface]` section
 - Each peer also has a shared `/etc/wireguard/peers.conf` file, which contains all the peers
 - The `wg0.conf` file also has a PostUp hook, calling `wg addconf /etc/wireguard/peers.conf`

It's up to you to decide how you want to share the peers.conf, be it via a proper orchestration platform, something much more pedestrian like Dropbox, or something kinda wild like Ceph.  I dunno, but it's pretty great that you can just wildly fling a peer section around, without worrying whether it's the same as the interface. 


Setting Private Key from a file
-------------------------------

Another piece of learning, courtesy of Samuel Holland, at <https://lists.zx2c4.com/pipermail/wireguard/2018-December/003702.html>.

You can read in a file as the Private Key by doing something like:

`PostUp = wg set %i private-key /etc/wireguard/wg0.key`

