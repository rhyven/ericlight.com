Title: Getting rid of the <url>#<slug> format in Flex
Author: Eric Light
Tags: Tech, Pelican
Date: 2018-01-12

Back when I was getting this blog set up, I had a [short whinge]({filename}pelican-config.md) about the default way that the [Flex theme](https://github.com/alexandrevicenzi/Flex) created links to pages.

Specficially, creating a link to "[Tuna Patties]({filename}../Food/tuna-patties.md)" (for example), Flex would append the link with an identical stub, such as <https://www.ericlight.com/tuna-patties.html#tuna-patties>

I thought this was silly, so I found a way to fix it, but never bothered submitting a Pull Request to Alexandre because I figured it was intentional.

Well, it turns out I wasn't the only one.  The good [Dmytro Litvinov](https://github.com/DmytroLitvinov) thought the same, and he created a [Pull Request](https://github.com/alexandrevicenzi/Flex/pull/88) to fix it, almost a whole year ago!

Now, you can avoid this behaviour by simply adding `DISABLE_URL_HASH = True` to your `pelicanconf.py`!
