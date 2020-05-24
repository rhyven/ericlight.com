Title: ZFS zpool vanishing after upgrading ProxmoxVE 5.4 to 6.2
Author: Eric Light
Tags: Tech, Linux
Date: 2020-05-23

Performing a major version upgrade is never pleasant.  I've been using ProxmoxVE for about ten years now though, and it's consistently done a fantastic job.  Since it's based on Debian, all the upgrades are done with a simple `apt update && apt upgrade`, with a variety of steps in the middle to point to new repositories, etc.  Nothing out of the ordinary, nothing scary.

So I've got two servers - one is an old one, with only a couple testing VM's residing on it.  I go ahead and work through the [5.x to 6.x upgrade guide](https://pve.proxmox.com/wiki/Upgrade_from_5.x_to_6.0), and everything Just Works.  No problem with that one.

When I moved onto the other server I had a couple different things I noticed.  For example, when trying to upgrade Corosync 2.x to 3.x (a prerequisite for the OS upgrade), I noticed it was trying to uninstall things like `corosync-pve`, which _really_ didn't seem right.

After comparing `dpkg -l` contents between the two servers, I learned that `corosync-pve` is actually just a transitional package - completely replaced by the new `corosync` package in version 3.  And although the server was trying to uninstall `corosync-pve`, it was then immediately installing `corosync`... so no problem.

Things continued to be mildly alarming during the upgrade itself, but not actually toooo bad, as all the removed packages were being replaced.  This one, for example:

```text
dpkg: pve-libspice-server1: dependency problems, but removing anyway as you requested:
 pve-qemu-kvm depends on pve-libspice-server1 (>= 0.12.5-1); however:
  Package pve-libspice-server1 is to be removed.
 spiceterm depends on libspice-server1 (>= 0.12.2); however:
  Package libspice-server1 is not installed.
  Package pve-libspice-server1 which provides libspice-server1 is to be removed.

(Reading database ... 65255 files and directories currently installed.)
Removing pve-libspice-server1 (0.14.1-2) ...
``` 

... was replaced with `spiceterm`.  No worries.

However things went _sharply downhill_ following reboot.  All of my VM images were missing!  I had a ZFS zpool that should have been at `/VM_Local_zpool` - that folder _existed_, and contained an `./images` folder, but that was completely empty.

I quickly checked the storage information in Proxmox, and the result was... **not good**:

<figure align="center">
  <img src="{static}/images/Tech/lost_zpool.png" alt="My storage usage - consistently at about 1.2 terabytes, and then suddenly... zero."/>
</figure>

... Really, not good.  :-|

So I SSH'ed into the server and had a quick look at my list of ZFS stores, and discovered that my dataset was entirely absent: 

```text
# zfs list
NAME               USED  AVAIL     REFER  MOUNTPOINT
rpool             83.8G  23.8G       96K  /rpool
rpool/ROOT        3.65G  23.8G       96K  /rpool/ROOT
rpool/ROOT/pve-1  3.65G  23.8G     3.65G  /
rpool/data        71.6G  23.8G     71.6G  /rpool/data
rpool/swap        8.50G  25.4G     6.85G  -

# zpool list
NAME    SIZE  ALLOC   FREE  CKPOINT  EXPANDSZ   FRAG    CAP  DEDUP    HEALTH  ALTROOT
rpool   111G  82.1G  28.9G        -         -    66%    73%  1.00x    ONLINE  -
```

A bit of Googling led me to the `zfs import` command, which resulted in the first piece of good news of the night:

```text
# zpool import

   pool: VM_Local_zpool
     id: 6614373363984244305
  state: ONLINE
 status: Some supported features are not enabled on the pool.
 action: The pool can be imported using its name or numeric identifier, though
	some features will not be available without an explicit 'zpool upgrade'.
 config:

	VM_Local_zpool              ONLINE
	  mirror-0                  ONLINE
	    wwn-0x50014ee0aeee96ef  ONLINE
	    wwn-0x50014ee05998ee25  ONLINE
```

It exists!  And it's ... online?  But where?  I don't get it.  I went ahead and tried importing it, but got a "directory not empty" error:

```text
# zpool import VM_Local_zpool 
cannot mount '/VM_Local_zpool': directory is not empty
```

Now, _**if** I'd been paying attention_ there, I would have realised that `zpool list` now contained my VM_Local_zpool:

```text 
# zfs list
NAME               USED  AVAIL     REFER  MOUNTPOINT
VM_Local_zpool    1.16T   611G     1.16T  /VM_Local_zpool
rpool             83.8G  23.8G       96K  /rpool
rpool/ROOT        3.65G  23.8G       96K  /rpool/ROOT
rpool/ROOT/pve-1  3.65G  23.8G     3.65G  /
rpool/data        71.6G  23.8G     71.6G  /rpool/data
rpool/swap        8.50G  25.4G     6.85G  -
```

From this point, all I had to do was empty /VM_Local_zpool, and try to remount the zpool.  But there's a second trick here.

ProxmoxVE has a pretty clear idea of How Storage Should Look, so every time it scans a storage device, is makes sure there's an `./images` folder in any storage enabled for VM Images.  It also makes sure there's a `./dump` folder on any storage enabled as a backup target, and a `./template` folder on any storage enabled for ISO images.  (Reference: <https://pve.proxmox.com/wiki/Storage:_Directory>)

So, when I removed that /VM_Local_zpool/images folder, Proxmox just... went ahead and recreated it almost immediately, so I still couldn't mount the zpool there.

In the end, I managed to get my zpool remounted by pairing the `rmdir` and `mount` commands together on the same line:

```text
# rmdir /VM_Local_zpool/images/
# zfs mount VM_Local_zpool
cannot mount '/VM_Local_zpool': directory is not empty
# rmdir /VM_Local_zpool/images/ && zfs mount VM_Local_zpool
# cd VM_Local_zpool/
/VM_Local_zpool# ls
backup	images
```

... and there we go!  My mount point, and all my VM images, are back unscathed!


And just for future reference - I saw a post on the FreeNAS forums that I should the status of the zfs-import-cache service, and enable it if it wasn't started by default... however it was fine:

```text
# systemctl status zfs-import-cache.service
● zfs-import-cache.service - Import ZFS pools by cache file
   Loaded: loaded (/lib/systemd/system/zfs-import-cache.service; enabled; vendor preset: enabled)
   Active: active (exited) since Sat 2020-05-23 20:46:54 NZST; 3min 26s ago
     Docs: man:zpool(8)
  Process: 1819 ExecStart=/sbin/zpool import -c /etc/zfs/zpool.cache -aN (code=exited, status=0/SUCCESS)
 Main PID: 1819 (code=exited, status=0/SUCCESS)

May 23 20:46:54 ~ systemd[1]: Starting Import ZFS pools by cache file...
May 23 20:46:54 ~ zpool[1819]: no pools available to import
May 23 20:46:54 ~ systemd[1]: Started Import ZFS pools by cache file.
```
