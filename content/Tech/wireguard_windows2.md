Title: WireGuard on Windows - Part 2
Author: Eric Light
Tags: Tech, WireGuard
Date: 2020-05-08

A few days ago I spun up a [Windows Dev VM]({filename}windows_dev_vm.md) to have a play with [WireGuard for Windows](https://www.wireguard.com/install/).

I didn't really have a clear goal in mind when I started playing with this - part of it was in trying to create and launch a tunnel without using the GUI.  Mostly I was just trying to learn more about a new implementation of a tool that I really like.

If you read my [previous article]({filename}wireguard_windows.md), you'll recall that I started off trying to do this with just `wireguard.exe`.  Here are some things I've discovered:

### wireguard.exe does a _whole lot_ of stuff

Wireguard.exe isn't just a GUI, which I originally thought it was.  It's also the piece of software that shouts out to [WinTun](https://www.wintun.net/) to create the interface, as well as the utility that reads the 'extended' attributes in your .conf file (e.g. the stuff that wg-quick takes care of), as well as the utility that [sets up your routes, DNS](https://github.com/WireGuard/wireguard-windows/blob/master/tunnel/addressconfig.go), etc, etc, etc.


### wireguard.exe doesn't create private/public keypairs

... To do this, you instead need to use wg.exe, which is installed under your System32 folder (so it's in your path, so it's accessible anywhere):

```text
PS C:\> wg genkey | tee $ENV:APPDATA\WireGuard.priv | wg pubkey > $ENV:APPDATA\WireGuard.pub
```

I did [figure this out the other day]({filename}wireguard_windows.md), but I'm reiterating here.


### wg.exe can read .conf files -- but you don't really want it to

Last time, I was having trouble reading a .conf file from wg.exe:

```text
PS C:\Users> wg setconf wg0 .\wg0.conf
Line unrecognized: ` ■['
Configuration parsing error
```

I'm not entirely sure what this was - I've since been able to read in a .conf file perfectly fine (for the record this is UTF-8 with Windows CRLF line-endings).  

However ... my breakthrough kinda sucks.

Wireguard for Windows stores it's config files in the Windows DPAPI-encrypted vault.  This is **_vastly_** better than just bunging a file in `C:\Users\Blah` and hoping for the best.  Maybe it's not perfect - I don't know much about DPAPI - but it's a far cry better than nothing.

When you use wireguard.exe to import a tunnel from a .conf file, it will read it in, sanity-check it (mine failed because I accidentally hit the keyboard during copy/pasta, so it rejected the Base64 encoding), and then safely store it away in the DPAPI storage.  You can then delete your original .conf file.  Just do this, it's better.


### You need __both__ wireguard.exe and wg.exe

OK so here's the bit that I only fully realised tonight:  wireguard.exe is like wg-quick, but it also provides the interface into the [Windows network stack](https://github.com/WireGuard/wireguard-windows/blob/master/tunnel/service.go) and the [Windows DPAPI storage](https://github.com/WireGuard/wireguard-windows/blob/master/conf/store.go) of your sensitive conf files.  You can't even run `wg set` without it, because wireguard.exe [is even responsible for creating the IPC Server](https://github.com/WireGuard/wireguard-windows/blob/master/manager/ipc_server.go) that interfaces with WinTun.

Honestly the Windows world is so much more complicated than the Linux world*.  🙄

(* some caveats apply)


## Conclusion

What's my plan now?

I'm going to make a thing that:

* Installs wireguard.msi silently
* Uses wg.exe to create a private/public keypair
* Uses that keypair to create a temporary .conf file
* Uses wireguard.exe to import that .conf file from some predetermined location
* Deletes the .conf file (probably using [cipher.exe](https://support.microsoft.com/en-nz/help/814599/how-to-use-cipher-exe-to-overwrite-deleted-data-in-windows-server-2003) to scrub it)
* Uses wireguard.exe to install the tunnel so it opens automatically on login

I'm hoping that this will create us something like an always-on-VPN connection that can be deployed easily by an IT support person, and require no end-user interaction.
