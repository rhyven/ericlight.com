Title: Installing PowerChute Network Shutdown on ProxmoxVE
Author: Eric Light
Tags: Tech, Linux
Date: 2018-02-27

This is going to be one of those posts where I just dump stuff.  Power failures are shite, and if your server isn't talking with your UPS, it won't shut down gracefully.  This is the story of my trying to get APC's PowerChute Network Shutdown working on a ProxmoxVE 5.1 environment.

Note I opted out of using either nut or apcupsd, because I had a nice fancy Network Management Card (NMC2 / Schneider AP9631) available.  Also, I wanted to shut down more than a single server, so a USB or Serial cable wouldn't do the trick.

1.  Install Java Runtime Environment: `apt install openjdk-8-jre`
1.  Download PCNS onto your Proxmox server - <http://www.apc.com/shop/us/en/categories/power/uninterruptible-power-supply-ups-/ups-management/powerchute-network-shutdown/N-auzzn7>
1.  Extract the download:  `tar -xvf pcns420Linux-x86-64.tar.gz`
1.  cd ./Linux_x64
1.  sudo su
1.  ./install.sh
1.  When prompted for your Java location, use `/usr/lib/jvm/java-8-openjdk-amd64/jre/bin`
1.  I didn't enable SMTP

Results in:

     root@ ~/Linux_x64# ./install.sh 
     ------------------------------------------------------------------
          PowerChute Network Shutdown 4.2.0 for Linux
          Copyright (c) 1999-2016 Schneider Electric.
          All Rights Reserved.
     ------------------------------------------------------------------

     OS=Linux

     Initializing ...

     Press any key to display End User License Agreement
     <--snip-->
     Do you agree to the above license terms? [yes or no]
     yes

     Please enter the installation directory or press enter to install to the default directory (/opt/APC/PowerChute):


     Are you sure you want to install PCNS to /opt/APC/PowerChute [Yes|No]? 
     yes
     PCNS will be installed to /opt/APC/PowerChute

     Please enter java directory if you want to use your system java (example:/usr/local/bin/jre/jre1.8.0_91) or press enter to install the bundled Java:
     /usr/lib/jvm/java-8-openjdk-amd64/jre/bin 

     Checking version of Java ...
     Detected Java Version: 1.8.0.151
     Acceptable version

     openjdk version "1.8.0_151"
     OpenJDK Runtime Environment (build 1.8.0_151-8u151-b12-1~deb9u1-b12)
     OpenJDK 64-Bit Server VM (build 25.151-b12, mixed mode)

     JAVA_DIR=/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/

     Copying the installation files ...
     Extracting PCNS files ...
     PCNS is extracted to /opt/APC/PowerChute
     Configuring startup files ...
     Startup script=/etc/rc.d/init.d/PowerChute
     Updating Linux symbolic link ...
     Configure Firewall
     Configuring uninstall script ...
     Setup the m11.cfg file

     Enable SNMP Support [Yes|No]? 
     no
     SNMP Not Enabled

     PowerChute Network Shutdown, v4.2.0
     Copyright (c) 1999-2016, Schneider Electric.  All Rights Reserved.
     Startup completed.


     Installation has completed.
     PowerChute Network Shutdown can be accessed through your browser at https://<your_server_ip_address>:6547
     Please complete the configuration wizard so that PowerChute Network Shutdown can protect your server.


Once you're finished with that, navigate to the new web portal on your server (second-to-last line in the output above), and complete the setup of your PCNS instance!

When you're configuring PCNS itself, you'll be prompted for the User Name, Password, and Authentication Phrase for the UPS.  These are the user details you use to log into your NMC.

By default, the Authentication Phrase is `admin user phrase`, but you should *totally* change this.  Assuming you've updated the firmware on your NMC, you can set the Authentication Phrase at `Configuration -> Shutdown`.

Setting up your outlet groups and shutdown times are left as an exercise to the reader.  :)
