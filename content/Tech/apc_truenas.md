Title: Getting TrueNAS (FreeNAS 12) to work with an APC NMC2 UPS (AP9631)
Author: Eric Light
Tags: Tech, Linux
Date: 2021-01-14

TrueNAS, and FreeNAS before it, has supported UPS via the NUT software package since forever.  But most people using it seem to be using USB-connected UPS devices.  I don't have one of these.  I'm dealing with an IPv4-based APC ups, specifically the Smart-UPS X 1500 (SMX1500RMI2UNC), with an AP9631 NMC2 card.

You're probably here because you're in the same boat:  trying to set up a non-USB or Ethernet-based UPS under FreeNAS/TrueNAS, and you can't.  You've noticed the TrueNAS console _will not shut up_ about errors which read something like: 

`nut plugin: nut_connect: upscli_connect (localhost, 3493) failed: Connection failure: Connection refused`.  (Or perhaps port 161)

_"But why?"_, you say.  _"I've given TrueNAS my UPS hostname, why is it always trying to talk to localhost?  And what is this port 3493, when SNMP is 161?"_

What's happening is that `upscli` is trying to talk to the `upsd` damon _on your TrueNAS server_, which is expected to listen on port 3493 - it's **upsd** which then does the talky with the SNMP driver, which in turn does the talky with the UPS.  This is why the TrueNAS console logs look like it's just shouting at itself.

Okay, let's get into it:

## UPS Configuration

First, you need to enable SNMP on your AP9631.  This was pretty straightforward, but remember that you need to go:

1. Configuration -> Network -> SNMPv1 -> Access -> **Enable**
1. Configuration -> Netowrk -> SNMPv1 -> Access Control, and make sure the `public` community is set to be accessible from 0.0.0.0
1. Reboot your NMC2 card.

This configuration should work with the defaults that the NUT SNMP driver expects - I suggest you get it working like this for now, then tweak to SNMPv3 once you have a confirmed-working connection.

## TrueNAS Configuration

Your UPS configuration menu is under TrueNAS -> Services -> UPS.  Configure your TrueNAS UPS section like so:

### General Options section:

* **Identifier:**  Up to you, but do yourself a favour and make it `ups`.
* **UPS Mode:**  Master
* **Driver:**  "Various ups 3 (various) SNMP - RFC 1628 (snmp-ups, experimental)"  -- once you save, this will simply display as `snmp-ups$(various)`
* **Port or Hostname:**  The hostname of the ups, hopefully something simple like `ups.mydomain.local`

### Monitor section:

Leave the Monitor User, Monitor Password, Extra users, and Remote Monitor all blank/default for now - you can change them once the UPS is talking to you.  Note I don't believe it's important to change the Monitor Password under this configuration, as `upsd` only listens on the loopback address.

### Shutdown and Email sections

I shall leave in your capable hands.

### Other Options:

* **Auxiliary Parameters (ups.conf):**  This is where you override the SNMP defaults, if desired.  By default, NUT will use SNMPv1 and the 'public' community.  [See here for all config options](https://networkupstools.org/docs/man/snmp-ups.htm) availble for the SNMP driver.  You could do something like this, if you want:

```ini
community=yaysecurity
snmp_version=3
privProtocol=AES
```

* **Auxiliary Parameters (upsd.conf):**  `LISTEN 127.0.0.1 3493`

That last line was the magic - this is the bit that makes upsd _not only_ listen on port 161 (whyyyy), but _also_ listen on 3493, which is where the rest of the UPS subsystem expects to find UPS data!

# Other interesting tidbits:

* Running `upsc -l` should list all UPS instances configured on your server.  Since I've got one, called 'ups', I see:

```text
# upsc -l
ups
```

* If `upsc -l` gives you a Connection Refused error, check `/usr/local/etc/nut/upsd.conf` to make sure it's listening on 3493.  If not, add your auxiliary parameter in TrueNAS and restart the service.

```text
# upsc ups
Error: Connection failure: Connection refused

# cat /usr/local/etc/nut/upsd.conf
LISTEN 127.0.0.1 161
LISTEN ::1 161

# sockstat -4 -l | grep upsd
uucp     upsd       99934 6  tcp4   127.0.0.1:161         *:*
```

_Above: upsd is definitely not listening on the expected port_

* **NUT Config files**:  These live under `/usr/local/etc/nut/`.  The folder is deleted and recreated every time you edit something in the TrueNAS gui, so if you're in that folder and change something in the GUI, you'll need to do the whole `cd /usr/local/etc/nut` again. No you can't do `cd ../nut`, because the whole inode is gone, so the OS doesn't know where you are anymore.

* **Testing your UPS**:  Once `upsd` is listening on 3493, you should be able to run `upsc ups`, and it will query your UPS for data.  Note that "ups" is your UPS identifier from the "General Options" section, also found as the first line of `/usr/local/etc/nut/ups.conf`:

```text
# cat /usr/local/etc/nut/ups.conf
[ups]
    driver = snmp-ups
    port = ups.mydomain.local
    desc = 
    pollfreq = 15

# upsc ups
ambient.humidity: 0.00
ambient.temperature: 23.0
battery.charge: 100.00
battery.date: 05/15/2017
battery.packs: 0.00
battery.runtime: 1221.00
battery.runtime.low: 600
battery.voltage: 54.50
device.mfr: APC
device.model: Smart-UPS X 1500
[...]
```

I think that pretty much covers it.  I hope this has been helpful to someone - at very least, I hope it's helpful to future-me!

It's been a little while since I've worked with UPS management software.  I like to think it's because my day job isn't in infrastructure anymore, but also to be honest the whole UPS scene is fairly ugly.  I recall speaking with an electrical engineer from Schneider a while ago, who jokingly said something like "creating a new UPS or CNC communications protocol is almost a rite of passage for any new engineer".  I can see why... when you're new, and see something _superbly awful_, it's quite compelling to try and fix it!  But decades now of dependencies really do add up to be a burden.

