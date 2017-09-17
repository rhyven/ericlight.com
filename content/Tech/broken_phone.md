Title: When Encryption Attacks!
Author: Eric Light
Tags: Android, Tech
Date: 2017-09-12

So... I wrecked my phone last night.  :-(

Android's phone encryption feature has been around for aaaages, so I was confident when I started the encryption process last night.  Unfortunately, something went wrong, and last night I discovered that everything was toast.

After a bit of digging, I found someone else with [**exactly** the same problem](https://forum.xda-developers.com/galaxy-s4-sprint/help/phone-encrypted-access-twrp-t3587534)!  

> "unable to boot into my phone as it sits at the boot screen. When I try to boot into TWRP, it asks for my password. [...] it appears to decrypt the partition and mount, but then while loading, TWRP shows a continuous stream of:
>
> <span style="color:red">E:Error parsing XML file</span>
>
> errors until it just restarts."

Unfortunately, nobody responded to my own personal [denvercoder9](https://xkcd.com/979/).

Long story short, I lost everything.  But for a while, I thought my *entire phone* was bricked.  The phone wasn't accessible in either Recovery mode (due to the XML parsing catastrophe) **or** Download mode - it wasn't accessible either via adb or via fastboot.

Eventually my mate [@rendition](https://keybase.io/rendition) pointed out that I could just boot into Recovery, then cancel the decryption step and wipe my phone from there.  That allowed me to start again from a clean slate.

And I encrypted my phone right away, with no trouble at all!
