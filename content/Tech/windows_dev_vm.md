Title: Setting up a Windows Dev VM under ProxmoxVE
Author: Eric Light
Tags: Tech
Date: 2020-04-26

Righto, I've been using WireGuard for quite a long time now, but I just had my first foray into WireGuard on Windows.  I'm trying to roll it into a low-touch VPN deployment sort of thing.  

There will be a post about that soon, but this particular post is about _setting up the environment_ for me to play with this stuff... I need a system where I can take snapshots and roll back the drive to a known state.  (So I can be sure I'm not missing anything that the installer would do).  

I don't have a Windows machine, so I started off by downloading a [Win10 Dev VM from Microsoft](https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/).  Since I'm running ProxmoxVE, I chose the VMware image, which will come down as a .zip file.

Download the zip file, and extract it to wherever your VM disk images live (mine is `/VM_Local_zpool/`)... this will save some time when you're importing the disk.  

Next, you simply use the [importovf](https://pve.proxmox.com/pve-docs/qm.1.html) function of `qm` to import the OVF manifest as a new KVM-based VM in Proxmox!

`~ # qm importovf 103 WinDev2004Eval.ovf VM_Images --format qcow2`
`Formatting '/VM_Local_zpool/images/103/vm-103-disk-0.qcow2', fmt=qcow2 size=136365211648 cluster_size=65536 preallocation=metadata lazy_refcounts=off refcount_bits=16`
`  (100.00/100%)`  
`~ #`

That was suspiciously easy...

After importing I couldn't launch the VM, but I've seen this error a dozen times and know who to handle it:

`kvm: -drive file=/VM_Local_zpool/images/103/vm-103-disk-0.qcow2,if=none,id=drive-sata0,format=qcow2,cache=none,aio=native,detect-zeroes=on: file system may not support O_DIRECT`
`kvm: -drive file=/VM_Local_zpool/images/103/vm-103-disk-0.qcow2,if=none,id=drive-sata0,format=qcow2,cache=none,aio=native,detect-zeroes=on: Could not open '/VM_Local_zpool/images/103/vm-103-disk-0.qcow2': Invalid argument`
`TASK ERROR: start failed: command '/usr/bin/kvm <-- snip --> -machine 'type=pc'' failed: exit code 1`

If you're here because you googled the above error, your problem is rooted in this particular bit: `file system may not support O_DIRECT`.  Your problem is that Cache setting on your Hard Disk entry (under VM -> Hardware) is set to "Default (No cache)".  Set it to Write Back or Write Through and it'll launch fine.

Okay, so the VM starts with no network card - I went ahead and just added the VMware vmxnet one that Proxmox offers, since that'll already have drivers set up on this VMware image.  After that it was a few seconds to join the domain, pop the Computer object into the correct OU, run a gpupdate, and fire up my RDP connection using [Remmina](https://www.remmina.org)... and just like that, I've got a Windows machine set up to start playing!

Now that I've shaved that particular set of yaks, I'm ready to start trying to do what I wanted to do earlier this morning.  Let's see how tomorrow goes...
