Title: Wireguard - Making a smooth installer on Windows
Author: Eric Light
Tags: Tech, Security, Wireguard
Date: 2020-04-26
Status: draft

Righto, I've been using Wireguard for quite a long time now, but I just had my first foray into Wireguard on Windows.  I'm trying to roll it into a low-touch VPN deployment sort of thing.

I don't have a Windows machine, so I've started off by downloading a Win10 Dev VM from Microsoft.  It came down as a VMware .zip file, so after extracting the zip file I [used qm to import the ovf](https://pve.proxmox.com/pve-docs/qm.1.html) manifest as a new KVM-based VM in Proxmox.

```~ # qm importovf 103 WinDev2004Eval.ovf VM_Images --format qcow2
Formatting '/VM_Local_zpool/images/103/vm-103-disk-0.qcow2', fmt=qcow2 size=136365211648 cluster_size=65536 preallocation=metadata lazy_refcounts=off refcount_bits=16
    (100.00/100%)
~ #``` 

That was suspiciously easy!  After importing I couldn't launch the VM, but I've seen this error a dozen times and know who to handle it:

```kvm: -drive file=/VM_Local_zpool/images/103/vm-103-disk-0.qcow2,if=none,id=drive-sata0,format=qcow2,cache=none,aio=native,detect-zeroes=on: file system may not support O_DIRECT
kvm: -drive file=/VM_Local_zpool/images/103/vm-103-disk-0.qcow2,if=none,id=drive-sata0,format=qcow2,cache=none,aio=native,detect-zeroes=on: Could not open '/VM_Local_zpool/images/103/vm-103-disk-0.qcow2': Invalid argument
TASK ERROR: start failed: command '/usr/bin/kvm -id 103 -name WinDevEval -chardev 'socket,id=qmp,path=/var/run/qemu-server/103.qmp,server,nowait' -mon 'chardev=qmp,mode=control' -chardev 'socket,id=qmp-event,path=/var/run/qmeventd.sock,reconnect=5' -mon 'chardev=qmp-event,mode=control' -pidfile /var/run/qemu-server/103.pid -daemonize -smbios 'type=1,uuid=1a0d83cb-68fa-4509-aa0c-75ffb16ef4f2' -smp '1,sockets=1,cores=1,maxcpus=1' -nodefaults -boot 'menu=on,strict=on,reboot-timeout=1000,splash=/usr/share/qemu-server/bootsplash.jpg' -vnc unix:/var/run/qemu-server/103.vnc,x509,password -cpu kvm64,+lahf_lm,+sep,+kvm_pv_unhalt,+kvm_pv_eoi,enforce -m 2048 -device 'pci-bridge,id=pci.1,chassis_nr=1,bus=pci.0,addr=0x1e' -device 'pci-bridge,id=pci.2,chassis_nr=2,bus=pci.0,addr=0x1f' -device 'vmgenid,guid=ef1bb4f2-7fbf-4f08-80b3-1811220c501f' -device 'piix3-usb-uhci,id=uhci,bus=pci.0,addr=0x1.0x2' -device 'usb-tablet,id=tablet,bus=uhci.0,port=1' -device 'VGA,id=vga,bus=pci.0,addr=0x2' -device 'virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x3' -iscsi 'initiator-name=iqn.1993-08.org.debian:01:66d6ecb3ba9' -device 'ahci,id=ahci0,multifunction=on,bus=pci.0,addr=0x7' -drive 'file=/VM_Local_zpool/images/103/vm-103-disk-0.qcow2,if=none,id=drive-sata0,format=qcow2,cache=none,aio=native,detect-zeroes=on' -device 'ide-hd,bus=ahci0.0,drive=drive-sata0,id=sata0,bootindex=100' -machine 'type=pc'' failed: exit code 1```

If you're here because you googled the above error, your problem is rooted in this particular bit `file system may not support O_DIRECT`.  Your problem is that Cache setting on your Hard Disk entry (under VM -> Hardware) is set to "Default (No cache)".  Set it to Write Back or Write Through and it'll launch fine.

Okay, so the VM starts with no network card - I went ahead and just added the VMware vmxnet one that Proxmox offers, since that'll already have drivers set up on this VMware image.  After that it was a few seconds to join the domain, pop the Computer object into the correct OU, run a gpupdate, and fire up my RDP connection using [Remmina](https://www.remmina.org)... and just like that, I've got a Windows machine set up to start playing with the Wireguard experience on Windows.
