Title: Mikrotik RouterOS - incorrect SNMP status for idle WLAN interfaces
Author: Eric Light
Tags: Tech
Date: 2018-01-07

While trying to monitor the status of one of our wireless access points, I discovered that RouterOS returns an incorrect SNMP status code for the wlan interfaces when there are no clients connected to the interface.  This is at least present in RouterOS v6.40.3, on a Mikrotik cAPlite (RBcAPL-2nD). 

Specifically, when the wifi interface is **up**, but has zero connected clients, the OID returns an SNMP value of 2 ("down").  This status is incorrect - the interface isn't down, it's merely waiting for an external connection. 

The specific OID is 1.3.6.1.2.1.2.2.1.8.2 (iso.org.dod.internet.mgmt.mib-2.interfaces.ifTable.ifEntry.ifOperStatus - interface #2 in my case) 

The applicable RFC says, "_When ifAdminStatus changes to the up state, the related ifOperStatus should do one of the following: [...] Change to the dormant state if and only if the interface is found to be operable, but the interface is waiting for other, external, events to occur before it can transmit or receive packets_"  (<https://www.ietf.org/rfc/rfc2863.txt>, section 3.1.13) 

I notice this issue was logged on the forums about 6 years ago, at <https://forum.mikrotik.com/viewtopic.php?t=51332>.  

I've raised this issue with Mikrotik support, and apparently it's been added to their to-do list, but I'm not sure it'll ever be done.  In the meantime, we've just had to disable up/down monitoring of that specific interface, because it's so misleading.
