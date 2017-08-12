Title: HP Procurve's warn-and-disable
Author: Eric Light
Tags: Tech, Networking
Date: 2017-04-30

Since mid-2016, I've been working as a Network and Security Administrator.  While I'd done a fair amount of networking previously, most of my experience had been with either unmanaged switches, or in a pre-built Cisco environment.  Stepping into the world of managed networking was new for me, as was stepping into the world of HP Switches.

We were having recurring issues with a certain business unit looping ports on a switch.  We had loop-protect running, but it was only set to disable the port after 5 seconds, and only for 300 seconds.  This wasn't long enough (we've since set it to something more resilient).

During our attempts to minimise the impact of a network loop, we enabled this setting on our HP Procurve switches:

    fault-finder broadcast-storm action warn-and-disable

This seems simple enough.  The fault-finder module will look for broadcast storms, and when found, will throw a syslog, an SNMP trap, and will disable the offending switch port.

Don't be fooled.  **This will absolutely wreck your breakfast.**

The fault-finder module is a *system-wide* setting, which means it applies to uplink ports as well.  When a broadcast storm happens, all your distribution switches will see the broadcasts coming from... their uplink port.  So of course, the switches disable their uplink to the rest of the network, neatly segregating themselves away from any services or central management.

Suffice to say, the next time we had a network loop there was a lot of walking and console cable madness, while we visited each of the distribution switches and manually re-enabled the disabled ports.

Lesson learned, loop-protect it is.  (Until we get STP up campus-wide, of course)
