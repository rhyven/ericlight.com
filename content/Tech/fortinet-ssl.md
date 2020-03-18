Title: Fortinet SSL VPN Certificate extensions
Author: Eric Light
Tags: Tech, Security
Date: 2020-01-19

If you're setting up a new SSL VPN with certificate authentication, and if you already have an internal PKI, you're probably considering using your internal certification authority to create the SSL keys and certificates for your VPN clients.  Awesome!  This is a great and easy way to do this job.

But there's a dearth of information on the Interwebs regarding what Extended Key Usages you need to have enabled in your Certificate Template for these.  There are a heap available, including Email Signing, Timestamping, Code Signing, IPSec SSL things (about 8 of these), and way more options.

Well, your search can end now.  There's only one Extended Key Usage option required for SSL certificate authentication with the Fortinet FortiClient VPN:

**_Client Authentication_**

That's it.  That's the post.
