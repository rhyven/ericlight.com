Title: Using ECDSA certificates with Let's Encrypt
Author: Eric Light
Tags: Security

[Let's Encrypt](https://www.letsencrypt.org)'s Certbot will generate an RSA key by default.  But we want to step into the new and exciting world of elliptic curve cryptography! Unfortunately Certbot doesn't really roll that way, so there are a couple hoops to jump through first.

A word of caution: this post has been written in retrospect, some time after I actually got ECDSA working.  That means there are bound to be squiggly little steps that I've missed, and I certainly should have provided screenshots or snippets that I've missed.  Sorry.

This post assumes you've already installed Certbot.  I had a working regular certificate from Certbot before I changed to ECDSA, so if you have problems following this from scratch, I do recommend trying that first.

For future reference, I'm running the latest certbot available in Debian unstable, which is version 0.8.1-3.

I got most of this information from [Scott Helme's website](https://scotthelme.co.uk/tag/lets-encrypt/), which has been awesome.

In brief:

1)  Generate yourself an ECDSA private key:

    openssl ecparam -genkey -name secp384r1 | openssl ec -out ec.key

You can change the curve that you use, if you feel a bit wiggly about the [controversy around the NSA & NIST](http://blog.cr.yp.to/20140323-ecdsa.html) degrading the quality of the curves.  I don't feel particularly wiggly about that, myself.


2)  Generate a Certificate Signing Request (CSR) with your shiny new key:

    openssl req -new -sha256 -key ec.key -nodes -out ec.csr -outform pem

That will give you ec.key (your private key), and ec.csr (your certificate signing request).  Time to get Let's Encrypt involved.


3)  Create your certificate:

    certbot certonly -w /var/www/html/ -d {your_domain} --email "{your_email}" --csr ./ec.csr --agree-tos

If everything goes perfectly, that should leave you with a new shiny set of certificates -- quite possibly named something clumsy like 0000-cert.pem and 0001-fullchain.pem, or similar.  Throw those into your nginx config and give it a test to see if it's working.


4)  Schedule your certificate renewals:

I had particular trouble with the renewal process of ECDSA certificates, because `certbot renew` isn't compatible with custom CSR's.  You need to run `certbot certonly` to pass the --csr argument, and then you need to deal with the output yourself.

Even more irksome, the certonly function will fail if you ask it to renew certificates which already exist:

    An unexpected error occurred:
    OSError: [Errno 17] File exists: '/etc/letsencrypt/live/{your_domain}/cert_ecdsa.pem'
    Please see the logfiles in /var/log/letsencrypt for more details.

There doesn't seem to be any way to tell certbot to overwrite the old certificates automatically, so I created a /etc/letsencrypt/temp folder, and wrote up a really yuck cron job for it.  If I were working on a production system I'd do something better, but this works for my lowly domain:

    # Recreate certs under /etc/letsencrypt/temp
    30 2 24 * * certbot certonly -w /var/www/html/ -d {your_domain} --email "{your_email}" --csr /path/to/your/ec.csr --agree-tos --non-interactive --webroot --cert-path /etc/letsencrypt/temp/cert_ecdsa.pem --fullchain-path /etc/letsencrypt/temp/fullchain_ecdsa.pem
    
    # Backup current certs to home dir
    31 2 24 * * mv /etc/letsencrypt/live/{your_domain}/cert_ecdsa.pem ~/certbackup/
    31 2 24 * * mv /etc/letsencrypt/live/{your_domain}/fullchain_ecdsa.pem ~/certbackup/
    
    # Move new certs to live folder
    32 2 24 * * mv /etc/letsencrypt/temp/* /etc/letsencrypt/live/{your_domain}/
    
    # Restart nginx
    33 2 24 * * service nginx restart


And that's all!  It seems to be working so far, but I'm sure something is going to fail at some point -- maybe I'll hit my request limit, or the Let's Encrypt service will be down, and I'll lose my certs.  If it happens too often I'll come up with a nicer cronjob and update this post.

