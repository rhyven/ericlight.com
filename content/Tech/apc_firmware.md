Title: Firmware update on an APC AP9630 NMC2
Author: Eric Light
Tags: Tech
Date: 2017-09-02

I've spent a little while working with the [APC Network Management Cards](http://www.apc.com/shop/us/en/products/UPS-Network-Management-Card-2/P-AP9630) now, and firmware updates are a total pain.

The biggest issue is that the UPS power outlets need to be **powered off** in order to flash the firmware, otherwise there's a terrifyingly-high chance that the NMC (a ~$700 card) will completely shit itself, and die permanently.  Aside from that, I've never managed to get updates working properly from the web interface.

Fortunately, the card is hot-pluggable, so if you have a spare UPS hanging around, you can unplug the NMC from each UPS in your fleet, throw it into your spare, and flash the firmware from there. Fast, easy, and simple... as long as you have that all-important spare.

Download the Firmware
---------------------

First, download the appropriate firmware for your device. At time of writing, the link for the SmartUPS 6.5.0 NMC firmware [can be found here](http://www.apc.com/us/en/tools/download/download.cfm?sw_sku=SFSUMX650&software_id=MFOI-APKQJS&family=98&part_num=AP9630&swfam=&tsk=), but if it's been a while you should find a new version at <http://www.apc.com/us/en/tools/download/>.

It comes down as an EXE file, but use 7-zip to extract the archive somewhere convenient. You only need the three .bin files:

* apc_hw05_bootmon_108.bin
* apc_hw05_aos_650.bin
* apc_hw05_sumx_650.bin

Flashing the Firmware
---------------------
Flashing the actual firmware is easy, but you do need to be careful of the order. The bootmon package goes first, then the AOS package, and then the sumx package.

**Be aware: the NMC will reboot immediately after each file is uploaded.  As a result, you need to reconnect after each upload, and reissue the BIN command.**

Make sure you know the username and password (default credentials are apc/apc), and that the FTP server is enabled. Then, go ahead and ftp to the NMC on it's IP address.

    $ ftp
    ftp> open x.x.x.x
    Connected to x.x.x.x.
    Name (eric): apc
    Password: apc
    230 Login successful.
    Remote system type is UNIX.
    Using text mode to transfer files.
    ftp> bin
    Using binary mode to transfer files.

Make sure you send the 'bin' command. I also use the hash command so I can watch the transfer status, but it's unnecessary.

Once you've connected, go ahead and upload the bootmon file:

    ftp> put apc_hw05_bootmon_108.bin
    ftp> close

It'll only take a few seconds to upload the file, and you won't see any notification from the FTP server.  But if you're paying attention to the card itself, you'll see the NMC network connection go down, and then start flashing.  This is the NMC installing the new firmware package.

Once the connection is up again, your FTP session will be broken.  Go ahead and reconnect; remember to reissue the BIN command:

    ftp> put apc_hw05_bootmon_108.bin
    ftp> close
    <...snip...>
    ftp> open x.x.x.x
    <...snip...>
    ftp> bin
    Using binary mode to transfer files.

Now upload the AOS file.  When the NMC reboots again, go ahead and repeat the cycle to upload the sumx file.

Once the NMC reboots for the third time, you should be done!

Thanks
------

Thanks to Angela from APC - she's been around for years, and as far as I can see she's _THE_ leading customer support person for the entire NMC firmware suite.  You can find her post on this process  [here at the APC forums](http://forums.apc.com/spaces/7/ups-management-devices-powerchute-software/forums/general/3183/firmware-upgrade-for-ap9631-which-order).
