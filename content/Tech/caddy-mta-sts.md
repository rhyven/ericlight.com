Title: Using Caddy to enable MTA-STS
Author: Eric Light
Tags: Tech, Security, Linux
Date: 2021-01-19


About 7 months ago, I left Nginx and [moved to Caddy]({filename}/Tech/caddy.md). I've found it super easy, and have now experienced using it as a reverse proxy, a static site server (this one!), as well as a hosting a [handy place](https://shrug.ericlight.com) for me to copy my favourite [Kaomoji](http://kaomoji.ru).

_Note:  the Caddyfile fragment to generate <https://shrug.ericlight.com> looks like this:_

```cfg
shrug.ericlight.com { respond "<meta charset='UTF-8'>¯\_(ツ)_/¯" }
```

Anyway, once I'd used Caddy's `respond` directive, it was a simple step to take it forward and use it to serve my handy-dandy MTA-STS policy file!

Simply add this new Server block to your Caddyfile:

```cfg
mta-sts.ericlight.com {
respond "version: STSv1
mode: testing
mx: in1-smtp.messagingengine.com
mx: in2-smtp.messagingengine.com
max_age: 86401"
}
```

This simple Server block will get you a shiny HTTPS certificate, redirect any HTTP visitors to HTTPS, and will provide enquirers with your MTA policy file.  _(Obviously, replace my domain name and MX entries with your own.)_

Sharp observers will notice that the MTA-STS policy file should be hosted at `https://mta-sts.ericlight.com/.well-known/mta-sts.txt`... but that's the elegance of the Respond directive in Caddy: _wherever_ you go at `mta-sts.ericlight.com`, you get exactly that response!

Example:  <https://mta-sts.ericlight.com/my/hovercraft/is/full/of/eels.txt>

Okay, that was easy... the next part is just creating your _**three**_ DNS records:

* **Record #1:**  An A record for `mta-sts.ericlight.com`, pointing to your Caddy server.

* **Record #2:**  A TXT record at `_mta-sts.ericlight.com`, reading `v=STSv1; id=20210112`.  (Note the underscore!  Also, the ID can be anything.)

* **Record #3:**  A TXT record at `_smtp._tls.ericlight.com`, reading `v=TLSRPTv1; rua=mailto:tls-reports@targetdomain.com`.  (update that email address)


... There you go!  Now you have a shiny new MTA-STS policy, and your Reporting email target (configured in DNS Record #3) will start reciving daily reports from sending mail servers, letting you know if your policy is working correctly.

Eventually (once you're sure it's all configured properly), you should change your `testing` policy to `enforce`.  When you do this, **make sure you update the ID in your TXT Record!**  This is how sending mail servers know that there has been a policy update.

Enjoy!
