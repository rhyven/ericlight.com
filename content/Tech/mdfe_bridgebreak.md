Title: task pve-bridge blocked for more than 120 seconds - on Proxmox with MDATP
Author: Eric Light
Tags: Tech, Linux
Date: 2022-03-13

Today I updated and rebooted a bunch of servers - all in a day's work. Everything went fine, until one of the hosts (the big one) didn't boot up again properly.

I've got two hosts, both running ProxmoxVE (version 7.1) and Microsoft Defender for Endpoint (version 101.61.69-insiderfast). On reboot, one of the hosts came up fine; the other didn't.

Long story short, uninstalling mdatp fixed the problem - wild hypothesis, but I suspect it was interfering with either network bridge or interprocess communication.

The rest of this post is technical info for people who might be able to fix it, and so that this blog post will come up for the other people who inevitably bump into this!

---

Symptoms - upon boot, the host came up, was apparently able to launch one VM, and recieved a timeout for all subsequent VM's:

<figure align="center">
  <img src="{static}/images/Tech/mdatp-bridge1.jpg" alt="A screenshot of the failed VM start actions."/>
</figure>

The lines are truncated, but all those pink lines are showing `TASK ERROR: start failed: command '/usr/bin/kvm -id 153 [...]' failed: got timeout`.

I say 'apparently' launched one VM, because I was unable to interact with it - in fact **all** the launch-on-boot VM's appeared to have booted, except everything about them was non-responsive, including Proxmox stats windows and console.

Trying to manually interact with the VM's using `qm` failed entirely - the console froze, completely unresponsive to either ^C or ^X, until I forcefully disconnected from SSH.

Checking dmesg revealed a horror story:

```console
Mar 13 16:54:36 buckwheat kernel: [  159.853700] vmbr1: port 1(eth3) entered blocking state
Mar 13 16:54:36 buckwheat kernel: [  159.853703] vmbr1: port 1(eth3) entered forwarding state
Mar 13 16:54:43 buckwheat kernel: [  166.700586] ixgbe 0000:81:00.1 eth3: NIC Link is Down
Mar 13 16:54:43 buckwheat kernel: [  166.701135] vmbr1: port 1(eth3) entered disabled state
Mar 13 16:54:45 buckwheat kernel: [  168.294208] ixgbe 0000:81:00.1 eth3: NIC Link is Up 10 Gbps, Flow Control: RX/TX
Mar 13 16:54:45 buckwheat kernel: [  168.294343] vmbr1: port 1(eth3) entered blocking state
Mar 13 16:54:45 buckwheat kernel: [  168.294349] vmbr1: port 1(eth3) entered forwarding state
Mar 13 16:54:47 buckwheat pvestatd[5040]: VM 112 qmp command failed - VM 112 qmp command 'query-proxmox-support' failed - unable to connect to VM 112 qmp socket - timeout a>
Mar 13 16:54:50 buckwheat pvestatd[5040]: VM 105 qmp command failed - VM 105 qmp command 'query-proxmox-support' failed - unable to connect to VM 105 qmp socket - timeout a>
Mar 13 16:54:53 buckwheat pvestatd[5040]: VM 115 qmp command failed - VM 115 qmp command 'query-proxmox-support' failed - unable to connect to VM 115 qmp socket - timeout a>
Mar 13 16:54:55 buckwheat pve-guests[11257]: start failed: command '/usr/bin/kvm -id 153 -name Eden -no-shutdown -chardev 'socket,id=qmp,path=/var/run/qemu-server/153.qmp,s>
Mar 13 16:54:56 buckwheat pvesh[5530]: Starting VM 153 failed: start failed: command '/usr/bin/kvm -id 153 -name Eden -no-shutdown -chardev 'socket,id=qmp,path=/var/run/qem>
Mar 13 16:54:56 buckwheat pve-guests[5530]: <root@pam> end task UPID:buckwheat:000015C7:00000710:622D6A6F:startall::root@pam: OK
Mar 13 16:54:56 buckwheat systemd[1]: Finished PVE guests.
Mar 13 16:54:56 buckwheat systemd[1]: Reached target Multi-User System.
Mar 13 16:54:56 buckwheat systemd[1]: Reached target Graphical Interface.
Mar 13 16:54:56 buckwheat systemd[1]: Starting Update UTMP about System Runlevel Changes...
Mar 13 16:54:56 buckwheat systemd[1]: systemd-update-utmp-runlevel.service: Succeeded.
Mar 13 16:54:56 buckwheat systemd[1]: Finished Update UTMP about System Runlevel Changes.
Mar 13 16:54:56 buckwheat systemd[1]: Startup finished in 4.603s (kernel) + 2min 54.823s (userspace) = 2min 59.427s.
Mar 13 16:54:56 buckwheat pvestatd[5040]: VM 104 qmp command failed - VM 104 qmp command 'query-proxmox-support' failed - unable to connect to VM 104 qmp socket - timeout a>
Mar 13 16:54:59 buckwheat pvestatd[5040]: VM 153 qmp command failed - VM 153 qmp command 'query-proxmox-support' failed - got timeout
Mar 13 16:54:59 buckwheat pvestatd[5040]: status update time (30.177 seconds)
Mar 13 16:55:18 buckwheat pvestatd[5040]: VM 104 qmp command failed - VM 104 qmp command 'query-proxmox-support' failed - unable to connect to VM 104 qmp socket - timeout a>
Mar 13 16:55:21 buckwheat pvestatd[5040]: VM 153 qmp command failed - VM 153 qmp command 'query-proxmox-support' failed - unable to connect to VM 153 qmp socket - timeout a>
Mar 13 16:55:24 buckwheat pvestatd[5040]: VM 112 qmp command failed - VM 112 qmp command 'query-proxmox-support' failed - unable to connect to VM 112 qmp socket - timeout a>
Mar 13 16:55:27 buckwheat pvestatd[5040]: VM 105 qmp command failed - VM 105 qmp command 'query-proxmox-support' failed - unable to connect to VM 105 qmp socket - timeout a>
Mar 13 16:55:30 buckwheat pvestatd[5040]: VM 115 qmp command failed - VM 115 qmp command 'query-proxmox-support' failed - unable to connect to VM 115 qmp socket - timeout a>
Mar 13 16:55:30 buckwheat pvestatd[5040]: status update time (30.186 seconds)
Mar 13 16:55:48 buckwheat pvestatd[5040]: VM 153 qmp command failed - VM 153 qmp command 'query-proxmox-support' failed - unable to connect to VM 153 qmp socket - timeout a>
Mar 13 16:55:51 buckwheat pvestatd[5040]: VM 104 qmp command failed - VM 104 qmp command 'query-proxmox-support' failed - unable to connect to VM 104 qmp socket - timeout a>
Mar 13 16:55:54 buckwheat pvestatd[5040]: VM 115 qmp command failed - VM 115 qmp command 'query-proxmox-support' failed - unable to connect to VM 115 qmp socket - timeout a>
Mar 13 16:55:57 buckwheat pvestatd[5040]: VM 105 qmp command failed - VM 105 qmp command 'query-proxmox-support' failed - unable to connect to VM 105 qmp socket - timeout a>
Mar 13 16:56:00 buckwheat pvestatd[5040]: VM 112 qmp command failed - VM 112 qmp command 'query-proxmox-support' failed - unable to connect to VM 112 qmp socket - timeout a>
Mar 13 16:56:00 buckwheat pvestatd[5040]: status update time (30.191 seconds)
Mar 13 16:56:00 buckwheat kernel: [  243.301563] INFO: task wdavdaemon:5583 blocked for more than 120 seconds.
```

The wdavdaemon is shown blocking here, but pve-bridge turned up just as frequently in the logs:

```console
root@buckwheat:/var/log# grep blocked syslog
Mar 13 18:34:14 buckwheat kernel: [  242.802463] INFO: task wdavdaemon:5740 blocked for more than 120 seconds.
Mar 13 18:34:14 buckwheat kernel: [  242.802658] INFO: task wdavdaemon:4899 blocked for more than 120 seconds.
Mar 13 18:34:14 buckwheat kernel: [  242.802840] INFO: task pve-bridge:6117 blocked for more than 120 seconds.
Mar 13 18:34:14 buckwheat kernel: [  242.802945] INFO: task pve-bridge:7734 blocked for more than 120 seconds.
Mar 13 18:34:14 buckwheat kernel: [  242.803057] INFO: task pve-bridge:9120 blocked for more than 120 seconds.
Mar 13 18:34:14 buckwheat kernel: [  242.803170] INFO: task pve-bridge:10283 blocked for more than 120 seconds.
Mar 13 18:36:15 buckwheat kernel: [  363.631430] INFO: task wdavdaemon:5740 blocked for more than 241 seconds.
Mar 13 18:36:15 buckwheat kernel: [  363.631610] INFO: task wdavdaemon:4899 blocked for more than 241 seconds.
Mar 13 18:36:15 buckwheat kernel: [  363.631776] INFO: task pve-bridge:6117 blocked for more than 241 seconds.
Mar 13 18:36:15 buckwheat kernel: [  363.631872] INFO: task pve-bridge:7734 blocked for more than 241 seconds.
```

So the interesting thing is that another node - foxtail - was also updated to the same version of both Proxmox and mdatp. The only obvious difference I can see are the numbers of VLANs each of them are bridging to:

This is a list of the bridges now, when they're both working (sorry, Markdown hates tabs; the below should be four tidy columns):

```console
root@foxtail:/var/log# brctl show
bridge name	bridge id		STP enabled	interfaces
fwbr101i0	8000.9e7164f22bab	no		fwln101i0
							tap101i0
vmbr0		8000.c2602668d5f4	no		eno1
							fwpr101p0
							tap100i0
							tap109i0
```
versus
```console
root@buckwheat:/var/log# brctl show
bridge name	bridge id		STP enabled	interfaces
fwbr102i0	8000.6	abd66965438	no		fwln102i0
							tap102i0
fwbr104i0	8000.f60b3f1a3118	no		fwln104i0
							tap104i0
fwbr105i0	8000.961281d6d5dc	no		fwln105i0
							tap105i0
vmbr0		8000.90e2bad572a8	no		eth2
							tap112i0
							tap115i0
							tap153i0
vmbr0v5		8000.0ea35ee013ba	no		eth2.5
							fwpr104p0
vmbr0v666	8000.1a23193ccf17	no		eth2.666
							fwpr102p0
							fwpr105p0
vmbr1		8000.90e2bad572a9	no		eth3

```

But when buckwheat was broken, the majority of the bridges were not visible:

<figure align="center">
  <img src="{static}/images/Tech/mdatp-bridge2.jpg" alt="A screenshot of the active bridges on each VM host. Buckwheat is missing a lot."/>
</figure>

At some point during troubleshooting, I restarted pvedaemon - although the service had started correctly, the restart failed with error: `timeout waiting on systemd`.

