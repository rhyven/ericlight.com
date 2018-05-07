Title: Fix Dell Keyboard Backlight under Debian
Author: Eric Light
Tags: Tech, Linux
Date: 2018-01-11

My personal laptop is an old Dell Latitude E6410.  One of the things I actually love about it, is the fact that the keyboard has a backlight.

However, because Linux, sometimes that backlight just stops working.  When this happens, you'll see error messages in dmesg, such as:

    dell_wmi: Unknown key with type 0x0011 and code 0x01e2 pressed

If this happens to you, just run this command:

    $ sudo echo 7 > /sys/devices/platform/dell-laptop/leds/dell\:\:kbd_backlight/brightness

You can echo a higher number if you want your keyboard brighter, but I found 7 to be more than bright enough.
