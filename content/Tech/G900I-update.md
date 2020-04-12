Title: Updating the modem and radio firmware on a Samsung Galaxy 5 (G900I)
Author: Eric Light
Tags: Android, Security, Linux
Date: 2016-10-27
Modified: 2020-04-12

A couple months ago, [Check Point](http://www.checkpoint.com) revealed their discovery of the [Quadrooter vulnerability](http://blog.checkpoint.com/2016/08/07/quadrooter/) affecting the Qualcomm chipsets in oodles of Android phones.

I use --CyanogenMod-- [LineageOS](http://www.lineageos.org) on a Samsung Galaxy S5, so thankfully I [received patches](https://web.archive.org/web/20161223020015/http://www.cyanogenmod.org/blog/cm-13-0-release-znh5y) for three of the four vulnerabilities in only a few days.

However, that last vulnerability was part of a proprietary binary blob for controlling the Qualcomm LTE chipset, only patchable by Samsung themselves.  It took a while for the Samsung updates to roll out, and then I got distracted for a while, but I finally downloaded my firmware.  The package I've used is "G900IDVU1CPH3", which seems to be compatible at least with the three NZ-based carriers, as well as all the Australian carriers.

There are a couple little issues with the firmware upgrade, easily fixed if you know how.  I'm going to assume you know exactly how to do everything without help.  I'm sure you're pleased.

In particular, the version of Heimdall in the Debian Sid repositories (1.4.1-2) doesn't quite work with the SGS5.  It appears [other people](https://www.google.com/search?q=ERROR%3A+Failed+to+send+request+to+end+PIT+file+transfer%21+samsung) have had similar problems.

The beginning of fix for me came from [turboyz](https://github.com/turboyz) on Github, at the bottom of this post:  (Edit 2020-04-12: GitHub Issue 348 from <https://github.com/Benjamin-Dobell/Heimdall/> has been deleted); however, he's manually made a couple changes to BridgeManager.cpp, which appear to be no longer necessary.  We can simply build it from source:

    sudo apt-get install build-essential cmake zlib1g-dev libusb-1.0-0-dev git
    git clone https://github.com/Benjamin-Dobell/Heimdall.git
    cd Heimdall

    # OPTIONAL:  Remove the `if(NOT DISABLE_FRONTEND)` codeblock at the end of Heimdall/CMakeLists.txt
    # I believe this just saves time compiling the GUI
    
    mkdir build && cd build
    cmake -DCMAKE_BUILD_TYPE=Release ..
    make
    cd bin 

Now you've got a nice new Heimdall installation, with the approproate updates to allow it to talk nicely to the new Samsung bootloader.

I copied my new baseband files into the Heimdall/build/bin folder, just to get them all together.  The last step is to flash your NON-HLOS.bin and modem.bin files:

    ./heimdall flash --APNHLOS NON-HLOS.bin --MODEM modem.bin

I happen to have an issue on my phone currently where, even though the modem and LTE drivers have both been successfully installed, and even thought the Quadrooter tester is no longer showing any vulnerabilities, my Baseband version on my phone is still shown as the old one.  I haven't been able to figure out why yet, but I don't think I'll worry about it for now.  There have been reports that you should first do this with --no-reboot, wait for the update to complete, then pull your battery, then when you power back on, immediately go _back_ into download mode and re-flash.  Apparently this helps update the recognised Baseband version, but to be honest it didn't help me.

If you're completely 100% lucky and absolutely nothing goes wrong, you win!  You should now have the most recent Samsung modem and LTE chipset drivers available for your phone... without having to roll back to the stock Samsung firmware.

Incidentally, if you want to save gigabytes and time downloading said firmware, and if your phone is precisely a Samsung Galaxy S5 (G900I), and if you definitely want firmware G900IDVU1CPH3, I've extracted the important files (modem.bin and NON-HLOS.bin) and stored them here:

<https://www.ericlight.com/files/G900IDVU1CPH3_modem_LTE.zip>  
SHA256 hash = a2ab13063583f6e83a3c2d8b79521a59ba103dda30a24bddf9248dd5a25bff3c  

I promise I haven't intentionally backdoored them, but I make no warranties of any sort.  They might just be pictures of my foot.

Good luck!
