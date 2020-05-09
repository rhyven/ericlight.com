Title: Renaming a computer object in Active Directory
Author: Eric Light
Tags: Tech
Date: 2020-05-09

Quick post tonight.

You can't rename a computer object in Active Directory Users and Computers.  Even if you change the hostname, the domain object will still have the original distinguishedName from the old device.

However... you can do it in ADSIEdit!  Just open `ADSIEdit`, navigate to the AD container that holds your misnamed object, right click on it, and Rename.

I've just done it with a couple test computers on a domain and both worked completely smoothly.  I don't know if this would be safe if the renamed computer were off-site.
