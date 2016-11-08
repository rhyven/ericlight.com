Title: Tidying up Pelican's URLs with the Flex theme
Date: 2016-10-23
Tags: Pelican
Author: Eric Light

This is just a brain-dump of tweaks I've made to my Pelican environment to get tidy URLs.  In summary:  One theme tweak, one Nginx tweak.

Making the Flex Theme drop the ugly url#slug format:
----------------------------------------------------

I've decided I'm going to roll with the [Flex](https://github.com/alexandrevicenzi/Flex) theme for a while.  I like it, but it had this habit of putting anchors and slugs into my article URLs.

For example, my first page is known to Pelican as "welcome-to-the-internet".  However, links to the page were automatically created as "welcome-to-the-internet#welcome-to-the-internet".  It seems redundant.  Also, it says the same thing twice.  It repeats itself.

I discovered the issue in the Flex theme.  It's under /templates/index.html, circa lines 7 and 29.  Simply change:

    {{ article.url }}#{{ article.slug }} 

... to... 

    {{ article.slug }} 

Fixed!

I haven't submitted a pull request to Alexandre, because I suspect it's intentional.


Getting Nginx to serve tidy urls:
---------------------------------

By default, Pelican creates great urls like {server}/Ramblings/welcome-to-the-internet

This is great, but it CREATES files like /var/www/Ramblings/welcome-to-the-internet.html

Nginx by default doesn't see "welcome-to-the-internet" and automatically serve "welcome-to-the-internet.html".  The lack of a file extention means that the .html file is fundamentally _a different file_, so it returns a handy-dandy 404 error instead.

To fix this, open /etc/nginx/sites-available/yoursite, and find:

    location / {
        try_files $uri $uri/ =404;
    }

Change it to the following - note I've added $uri.htm and $uri.html, to inform Nginx that it should try appending .htm or .html onto the end of a uri if it can't find the page:

    location / {
        try_files $uri.htm $uri.html $uri =404;
    }


All done, happy tidy URLs!
