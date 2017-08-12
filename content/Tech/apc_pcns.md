Title: Broken log times in APC's PCNS Appliance 4.1
Author: Eric Light
Tags: UPS
Date: 2016-10-27

Schneider Electric's [PowerChute Network Shutdown](http://www.schneider-electric.com/en/product-range/61933-powerchute-network-shutdown/) is a piece of software which communicates with your local UPS, and initiates system shutdown if the UPS battery is unable to continue providing power.  This helps to preserve file integrity in the event of a prolonged power failure.

Previously, you had to install the PCNS client separately on each virtual machine.  Since then though, APC have released a [PCNS VMware Appliance](https://solutionexchange.vmware.com/store/products/apc-powerchute-network-shutdown-v4-1-for-vmware) which is installed directly into vCenter, and initiates shutdown on all the VMware guests through a single Virtual Machine.  This is a much tidier model, so we've recently embarked on migrating to the PCNS Appliance.

After installing the PCNS 4.1 appliance and getting everything working, I discovered that the time on all the log files was wrong by a significant margin.  I can't remember exactly what the margin was, it could have been say 8 hours or something.

I did a bit of research and eventually I discovered a spectaularly old question on the APC forums, dating all the way back to 2011:

_"I have installed PCNS 2.2.4 into the vMA of an ESXi 4.1 server. It properly communicates with the associated NMC and performs correctly. However, it reports all the activities in Eastern Standard Time. I don't know where it's picking up that time zone and can't find anywhere to change it. In the vSphere client the time shows up correctly. Checking date inside the vMA from the CLI also shows the correct time and timezone. The date and time setting in the NMC is correct and is set to synch with NTP with correct time zone."_  
From: <http://forums.apc.com/spaces/7/ups-management-devices-powerchute-software/forums/general/6809/pcns-2-2-4-esxi-annoyance>

The answers include a broken link to an APC web page about it, but fortunately the poster copied the original post detail, which showed me where to look:

_"PCNS uses a standard java function to retrieve the current date from the system when writing events to the log. The Problem on the VIMA is that this function always returns the US date format (PDT).  
This is an issue with Java http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=6456628  
You can correct the time issue on VIMA by modifying /etc/sysconfig/clock file.  
+/etc/sysconfig/clock contains a line ZONE="America/Los_Angeles"+  
You need to edit the ZONE= to match your region such as ZONE="America/New_York"_

Sounds great!  But when I looked in /etc/sysconfig/clock, I discovered my time zone was already set to "Pacific/Auckland".

However, it also contained the value "UTC = False".  I changed this to "UTC = True", and et voilà!  The problem is fixed!
