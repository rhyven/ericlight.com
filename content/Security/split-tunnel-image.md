Title: Why are all Split-Tunnel VPN diagrams so ugly?
Author: Eric Light
Tags: Security, Tech
Date: 2020-05-21

Right.

Today I needed to find a diagram of the traffic flow for a split-tunnel VPN.  Nothing fancy, just a real simple user-facing diagram to form part of an article.

And friends, there was _nothing_.  Nothing at all.  I found proper technical ones from [Cisco Meraki](https://documentation.meraki.com/@api/deki/files/721/c6ddeaa8-5df4-4e5e-b542-c52766568816?revision=1); fancy Office365 ones, depicting an [ExpressRoute to O365](https://docs.microsoft.com/en-us/office365/enterprise/media/vpn-split-tunneling/vpn-model-2.png) and tunnelling everything _else_ through the VPN; and another Office365 tunnel with [ExpressRoute and a split-tunnel](https://docs.microsoft.com/en-us/office365/enterprise/media/vpn-split-tunneling/vpn-model-5.png) for the rest of the traffic.

Pretty much the closest I came to my needs was this atrocity, via <http://blog.soundtraining.net/2013/03/how-to-configure-split-tunneling-on.html>:

<figure align="center">
  <img src="{static}/images/Security/split_tunnel_yes.jpg" alt="An accurate, but not aesthetic, diagram of how split tunnels work." width="300"/>
  <figcaption><em>Although accurate and functional, this is not a pleasant sight.</em></figcaption>
</figure>

So I went over to <https://www.draw.io> and whipped up something a bit prettier.  This isn't marvelous, but it's way better than I could find anywhere else:

<figure align="center">
  <img src="{static}/images/Security/split_tunnel_better.png" alt="A slightly more pleasant diagram of how split tunnels work."/>
</figure>

In retrospect, I could have done better - I really should have had the corporate tunnel going **through** the cloud of the internet.  However this works for ne.

If you'd like to use this, feel free.  You can even use [this fancy URL](https://app.diagrams.net/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=VPN%20Split%20Tunnel(2).drawio#R7Vddb5swFP01PCbCfCV5XJKmU9VKrSp1W1%2BQAzdgxWBkTCD99TPFTiCwtZMSdZWqRMI%2B9%2Foa33Nscw17kVTXHGfxHQuBGpYZVoa9NCwLOZZl1H8z3DeIN7MbIOIkbCDzCDySF1AjNVqQEHKFNZBgjAqSdcGApSkEooNhzlnZddswGnaADEfQAx4DTPvoDxKKWKGe6xwN34FEsZ4aebPGkmDtrZaSxzhkZSusfWXYC86YaFpJtQBaZ6%2BbmNUfrIc345CK9wy4dZ9vls8%2F4e7p9uEO3QTldTQaKTZ2mBZqxeplxV6nIGMkFcCvdnKeOpvIsOeHtZiyE%2BI8hlB1YpFQ7SQ428KCUcYlkrJUBpxvCKUaMizbNeufxCleA71nORGEpdIWQD2pNOyACyIJuT1xWDMhWNJy%2BEZJVBsEyyTKCkFJKmfXuqgnwcrlEFyuI6uXmVRRrd8x22xIAOMQdvKRj0vGt7nAzYzzfsIVB%2FUbQHXKrNwTwBIQfC9dlNX2lBjUdrBnql8exaV3SNySlXbDSs7RIfKRcNlQnP8D%2F84F%2Bf%2BvKM2By6i5evobzJO%2BGlerqWOaPem2LWcQgTc9EcG0LwJkeX0VIHQpGUy%2BjoFBzQQFJ2I%2FpizY%2BiURsb%2BFva9hf%2F2arXNIwnVOz4VpTxL66GgrYuJcSBCzzy%2BIQeqHVfJeQQSUFWE%2Bzoo1JYH%2F2jsP%2F84MdfiXX079I2EyIABkowspQJ81n1kCF7xHRCFHU18uBDdszDnTXwrLEZqe6a5wJt2DwXH6d4U7G9DFpW4KhL5k8fGy8NDHyYK%2F4EfysCrTnefSp8p9iX%2FxkfW2KnTmNhSqb3VpJlMBaaiay4DiPCdBVxDSrssuNG36qkZ0x7b1t1wKzCMQb99wEHYKwH7G2xkdOIA1xoFKmnfdsnEozWqG%2B3qPtPa55XQJNb1uiJwVPAA1ql3lnQaadAPZ7kmgJjG9QK%2BsH5Y9JATZPRarjfux5revfgM%3D) to open the drawing as an editable vector graphic at [Draw.io](https://www.draw.io) directly!


