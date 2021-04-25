Title: Configuring a custom SSL certificate in Zentyal
Author: Eric Light
Tags: Tech, Security, Linux
Date: 2021-04-25

Zuper-quick post for when this bites me again in the future!

Tonight I upgraded from Zentyal 6.2 to Zentyal 7.0.  Smooth as butter, everything went great.

Until I logged in, and my shiny Actual Paid Money SSL certificate had vanished, replaced by a self-signed commoner's certificate.  Piffle.

Instructions for installing a custom SSL certificate in Zentyal are actually kinda shaky, so here you go:

``` bash
cd /var/lib/zentyal/conf/ssl/
mkdir old
mv * old
nano ssl.key
nano ssl.cert
cat ssl.cert ssl.key > ssl.pem
chmod 0400 ssl*
```

That's it!  Your Private Key lives in `ssl.key`, and your SSL certificate lives in `ssl.cert`.  

Reboot, and job done.
