Title: When a docking station wrecks your breakfast
Author: Eric Light
Tags: Tech
Date: 2019-02-23

It's been a while since I posted, but we bumped into something completely batshit crazy at work that I just had to share.

One of my colleagues was setting up a new computer, and was unable to RDP into the new build. He kept getting the error message "Your session ended because there was a data encryption error. If this keeps happening, ask your admin or tech support for help."

!["Your session ended because there was a data encryption error."]({static}/images/wd15.png)


We'd never experienced this error before, and - although the internet knew about it - there were not very many helpful hits on Google.  In fact, all of the reports we found were the result of a bug in Windows 7, and we were only using Windows 10.

In the end, completely weirdly, my colleague tried a different docking station, and it *worked*!  This is absolutely the weirdest thing I've ever seen.  Both the working and failing docking station had the most recent firmware applied, and they were both flashed from the same image, so it's not a corrupted download or anything.

Metadata about this issue:  Both machines were Windows 10, 1709 build, with all updates installed.  The originator machine was an HP Z240 workstation, and the target machine was a Dell 7390, connected to a Dell WD15 docking station.  All three items had received fresh firmware updates and all Windows Updates.




