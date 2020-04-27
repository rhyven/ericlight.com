Title: Getting WireGuard on Windows - quietly
Author: Eric Light
Tags: Tech, WireGuard
Date: 2020-04-27

So, I mentioned in my post [yesterday]({filename}windows_dev_vm.md) that I'm trying to get a bit of a quiet installer for WireGuard on Windows.  Not that the current one is _noisy_, but I have a really simple use-case that I want to meet.

I spent some time seeing if I could just extract `WireGuard.exe` and run that.  Nope, of course - it requires [WinTun](https://www.wintun.net/) to be installed to facilitate the Layer 3 tunneling.

Next I played with the idea of just deploying WinTun directly, without installing the WireGuard package itself.  I can only assume that this would have been _super easy_ if I'd ever built a proper MSI installer before, but in the end it was just way easier to:

```text
WireGuard-amd64-0.1.0.msi /q
```
... It was still worth the tangential digging, but who would have ever guessed that [Jason Donenfeld](https://www.zx2c4.com/) would have already done things the best way.  ¯\\\_(ツ)\_/¯  </s\>

Note you've got to run the above in an elevated command prompt, since it's installing drivers.  However, the installation is still not quiet - after install, it pops up the WireGuard GUI window!

<figure align="center">
  <img src="{static}/images/Tech/WireGuard_launch.png" alt="After running the installer with the 'Quiet' parameter, the WireGuard GUI still opens"/>
</figure>

"That's annoying," I think to myself, "can I stop that?"  To the [installer source code](https://github.com/WireGuard/WireGuard-windows/blob/master/installer/WireGuard.wxs)!

OwO ... Hwat's this?  

```xml
    <!--
        Launch WireGuard.exe after setup complete
    -->
    <CustomAction Id="LaunchApplication" HideTarget="yes" Impersonate="no" Execute="deferred" FileKey="WireGuard.exe" ExeCommand="" Return="asyncNoWait" />
    <InstallExecuteSequence>
        <Custom Action="LaunchApplication" Before="InstallFinalize">(&amp;WireGuardFeature = 3) AND NOT DO_NOT_LAUNCH</Custom>
    </InstallExecuteSequence>
```

It appears that we can pass through an environment variable to stop the installer from launching the GUI after install!

```ps1
 .\WireGuard-amd64-0.1.0.msi /q DO_NOT_LAUNCH=True
```

Aaaand success... now I've got WireGuard and WinTun installed, no user interaction, so far completely silent.  Next I gotta create a keypair.  There aren't any relevant command-line arguments that I can pass to wireguard.exe, so I went on a hunt for a keypair generator.

<figure align="center">
  <img src="{static}/images/Tech/wireguard_exe_options.png" alt="A list of the few parameters for wireguard.exe - /installmanagerservice, /installtunnelservice, and similar uninstallers.  No keygen etc."/>
</figure>

I spent an hour or so scratching around various options to find a keypair generator that looked trustworthy.  I honestly couldn't find one... even the one posted on the [WireGuard GitHub](https://github.com/WireGuard/WireGuard-tools/tree/master/contrib/keygen-html) includes a caveat from Jason.

Until I decided to have a closer look at the installer source code... the very same code I was looking at when I discovered the DO_NOT_LAUNCH property above.

```xml
<Component Directory="System64Folder" Win64="yes" Id="Wg64Executable" Guid="d9b494ec-0959-442c-89ad-6aa175acfd03">
    <File Source="..\$(var.WIREGUARD_PLATFORM)\wg.exe" Id="Wg64Executable" />
</Component>
```

So `C:\Program Files\WireGuard\WireGuard.exe` appears to be just a shell that calls out to `C:\Windows\System32\wg.exe`.  Oh my god that knowledge would have saved me **hours**!!

So... here's how to generate a WireGuard keypair, in Windows, without the GUI.  Since system32 is in the path, you can run this from anywhere.  The below will create WireGuard.priv and WireGuard.pub in your AppData folder:

```text
PS C:\> wg genkey | tee $ENV:APPDATA\WireGuard.priv | wg pubkey > $ENV:APPDATA\WireGuard.pub
PS C:\> cat $ENV:APPDATA\WireGuard.*
uIGDK+LMDZANniFxrofIpu/hUyezuwCM7qSDVVO+1Gw=
85MxGcWutHJsjFggiZ+J4/vsNYDVEa8zYk53DQZCwyE=
```

**_AWESOME._**  Next step is to zoink that into a handy-dandy config file.  (More accurately, next step is to delete that private key that I've now posted to the internets)

Right, so it _looks_ like I can't just create a text-based wg0.conf file like I do in Linux.  When I do, I get this error:

```text
PS C:\Users> wg setconf wg0 .\wg0.conf
Line unrecognized: ` ■['
Configuration parsing error
```

I thought this might be the file encoding, so I tried it in ANSI etc, but then I learned that Wireguard for Windows stores it's config files in `C:\Windows\System32\config\systemprofile\AppData\Local\WireGuard\Configurations\` ... and they're not in plain text.  They're stored with the Windows Data Protection API (DPAPI), so perhaps that's what wireguard.exe is expecting?

Either way, I've been playing with this for quite a long time now, so I'm off to take a break for the night or so.  Once I figure out how to create a WireGuard config file for an interface I'll post a new article.  Hope you enjoyed reading so far!

