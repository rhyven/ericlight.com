Title: Compiling Heimdall without installing Qt
Author: Eric Light
Tags: Android, Tech
Date: 2017-09-13
Modified: 2017-12-19

During my recent [Wrecked-phone Saga]({filename}broken_phone.md), I had some trouble flashing my firmware.  My phone was broken at the time, so I couldn't enable ADB Debugging - therefore adb wasn't an option.  OEM Bootlock was on, so fastboot wasn't an option.  My Recovery bootloader was also broken.  I thought my phone was bricked.

That's until I remembered Heimdall.

[Heimdall](http://glassechidna.com.au/heimdall/) is specifically a tool for working with the partitions on Samsung phones - other visitors need not apply.  It works a treat for my Samsung Galaxy S5 (kltedv) though.

Heimdall, however, is **old**.  The version in the Debian Sid repository is 1.4.1, which [dates back to 2015](http://metadata.ftp-master.debian.org/changelogs/main/h/heimdall-flash/heimdall-flash_1.4.1-2_changelog).  And when we have old versions, we also have incompatibilites!  Such as Heimdall 1.4.1's [incompatibility with newer versions of Samsung devices](https://github.com/Benjamin-Dobell/Heimdall/issues/209) ... such as my precious SGS5.

Happily, Heimdall is open source, so I was able to download and compile a new version that overcomes the problem.  And that's how I found myself staring at the screen and looking at this:

![Do I really need to install 55 packages to build this?]({filename}/images/yuck.png)

**That is Yuck.bat**

I really didn't want to install 55 packages just to build this.  The majority of missing packages were required to build the GUI section of the tool, which I didn't want to use anyway.  What if I could ... _build Heimdall without building the GUI??_

And of course, that's the title of this article, so here's how to do it!

**EDIT 2017-12-19:  The stuff below is no longer necessary.  For better instructions, have a look at my article about [flashing a Samsung G900I back to stock]({filename}new_heimdall.md).**

1. Clone the git repository, with `git clone https://github.com/Benjamin-Dobell/Heimdall.git`

2. Edit the CMakeLists.txt file: `nano Heimdall/CMakeLists.txt`

3. Delete the last four lines of CMakeLists.txt:

        cmake_minimum_required(VERSION 2.8.4)

        set(CMAKE_MODULE_PATH
            ${CMAKE_SOURCE_DIR}/cmake
            ${CMAKE_MODULE_PATH})

        project(Heimdall)

        set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

        option(DISABLE_FRONTEND "Disable GUI frontend" OFF)

        add_subdirectory(libpit)
        add_subdirectory(heimdall)

4. You're done!  Go ahead and build according to the instructions.
