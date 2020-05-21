Title: Roundcube not loading email contents
Author: Eric Light
Tags: Tech
Date: 2020-05-11
Summary: Here's another quick one!  I had a [Roundcube](https://roundcube.net) instance, chugging along fine.  Then one day it just stopped loading emails!  Everything else was all fine - no problems with login etc, but trying to preview an email just game me a sadfaec.  Chrome couldn't load the contents, and told me that the server had refused to connect.


Here's another quick one!  I had a [Roundcube](https://roundcube.net) instance, chugging along fine.

Then one day it just stopped loading emails!  Everything else was all fine - no problems with login etc, but trying to preview an email just game me a sadfaec.  Chrome couldn't load the contents, and told me that the server had refused to connect:

<figure align="center">
  <img src="{static}/images/Tech/roundcube.png" alt="Roundcube webmail - everything looks perfect, except there's a error loading the preview of the selected email."/>
</figure>

So of course, I can't just let this go - being able to see the contents of the emails is relatively important!  But what the heck was causing it?

I spent some time in Chrome's developer tools and console, as well as time grepping and tailing log files... this would have all been fixed much earlier if I were running Firefox I think, as it's a bit more explicit with errors.

So, what was the fix?  It was nothing to do with Roundcube, routing, firewalls, or reverse proxies.  (Seriously, I checked all of these...)

The problem is that, last week, I'd modified the HTTP Headers on the reverse proxy to include:

```
   X-Frame-Options ("DENY")
```

... no good.  It all came right when I changed the X-Frame-Options directive to "SAMEORIGIN".  Suddenly, all fixed.

Sheesh!
