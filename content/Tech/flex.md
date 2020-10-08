Title: Make the Flex theme center images
Author: Eric Light
Tags: Tech
Date: 2020-10-07

Previously I've been frustrated that the CSS in the [Pelican](https://www.getpelican.com) [Flex theme](https://github.com/alexandrevicenzi/Flex) doesn't centre images.  However, I'm only one user with one use-case, so I haven't raised a pull request.

Instead, I've finally gotten around to creating a quick-and-dirty sed string to fix the minified CSS file:

    sed -i 's/}img{max-width:100%}/}img{max-width:100%;margin-left:auto;margin-right:auto;display:block}/' style.min.css

I also like my caption text to be italicised and centered, so I extended this a little: 

    sed -i 's/}img{max-width:100%}/}img{max-width:100%;margin-left:auto;margin-right:auto;display:block}figcaption{font-style:italic;text-align:center}' style.min.css

Run either of those in `./Flex/static/stylesheet`.  It'll modify just the img class in the CSS and suddenly all your images will center unless you tell them not to!

