Title: Flashing a Samsung S5 G900I back to stock
Author: Eric Light
Tags: Android, Tech
Date: 2017-12-19

I got a second-hand Samsung Galaxy S5 for my mum yesterday (a G900I model, from Telstra), and I spent some time getting it ready.

Firstly, I [downloaded](https://www.sammobile.com/firmwares/galaxy-s5/SM-G900I/) the most-recent Telstra firmware image.  At time of writing, that's G900IDVU1CQJ2.  Telstra appears to be the only carrier still releasing stock firmware for this phone, so I downloaded the Telstra version even though we're connecting to Spark New Zealand.  This means the phone will at least be running the most up-to-date baseband and modem firmware.

Note - if you try this, and find that the recent (international) version doesn't work properly with your local carriers, download the older (local) package, and flash the modem.bin and the NON-HLOS.bin packages from the local one instead.

Flashing the new firmware required a little thinking.  I'm 99% sure that I did this the hard way, but basically:

 - Download the newest version of [Heimdall from Github](https://github.com/Benjamin-Dobell/Heimdall)
 - Back last year I had [a post]({filename}heimdall-nongui.md) that mentioned editing CMakeLists.txt - ignore that now.
 - Build the software (assuming you extracted the zip instead of using `git clone`), with:

        cd Heimdall-master
        mkdir build
        cd build
        cmake -DDISABLE_FRONTEND=ON -DCMAKE_BUILD_TYPE=Release .. 
        make

Once I'd built Heimdall, I unzipped the firmware into a convenient place, and I examined the PIT file from the phone:

    ./heimdall print-pit

This descripts the partition table on the phone.  In particular, it tells you which files in your firmware package should be uploaded to which partitions.  I ended up with the following Heimdall flash line:

    ./heimdall flash --APNHLOS NON-HLOS.bin --MODEM modem.bin --SBL1 sbl1.mbn --DBI sdi.mbn --ABOOT aboot.mbn --RPM rpm.mbn --TZ tz.mbn --BOOT boot.img --RECOVERY recovery.img --SYSTEM system.img.ext4 --CACHE cache.img.ext4 --HIDDEN hidden.img.ext4

I know I could have only flashed the modem.bin and NON-HLOS.bin files, but I'm not sure what I would have missed by skipping all the other partitions.

After the phone was flashed up to the current Stock firmware, I made sure it booted correctly, and then went ahead and converted the phone to my beloved [LineageOS](https://www.lineageos.org), happy in the knowledge that all the "other bits" of the firmware were all updated.
