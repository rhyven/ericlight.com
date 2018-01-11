Title: Staying Secure in Business
Author: Eric Light
Tags: Security, Tech
Date: 2017-06-28

A friend asked a question today on Facebook.  I started writing a reply, and it turned into a 700-word essay.  Hate it when that happens...

The question was: 

#### _"If large multi-international companies are getting hacked in Europe who have millions if not billions of $$ and capacity to protect their IT systems - how can small/micro businesses protect their IT platforms and systems?"_

Firstly - nobody is safe from an APT ("Advanced Persistent Threat").  The recent [NotPetya](https://twitter.com/search?q=NotPetya) outbreak was an APT - malicious actors hacked a Ukrainian firm that produced accounting software, and [used their software's update facility](https://medium.com/@thegrugq/pnyetya-yet-another-ransomware-outbreak-59afd1ee89d4) to literally deliver malicious code specifically to the users of this particular software package ("M.E. Doc").  Nothing's keeping folks safe from that level of sophistication.

However, the exploit by which NotPetya *spreads* was [actually patched by Microsoft](https://technet.microsoft.com/en-us/library/security/ms17-010.aspx) in **March**.  If people had updated their internet-connected devices, this virus would have been limited to only users of M.E. Doc.

Aside from that though, there's actually a disappointingly simple answer to this.  Security is actually relatively within reach, if we all follow these simple steps:


### 1)  Update. Everything. At every opportunity.

That includes Windows Updates, but also [Adobe Reader](http://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=adobe+reader) (annoying!), [Java](http://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=java) (double annoying!), [anti-virus engines](https://twitter.com/taviso/status/860679110728622080), etc.  This is absolutely the top priority, and the cybersecurity industry has been trotting this line out for years, but people just don't.  Because annoying.

Real life incident:  June 22, 2017 - Honda falls prey to the WannaCry worm, 37 days after release (four months after the patch was released), due to poor patching hygiene.  

See <http://thehackernews.com/2017/06/honda-wannacry-attack.html>

### 2)  Backup everything important.

The more important it is, the more places you should keep it.  You should have at least three copies of every important file.  THIS IS ANNOYING, but if you don't do it, data loss will hit you.  Something like [Crashplan](https://www.crashplan.com) (a low-cost service that sends backups to the cloud), plus a regular (weekly?) copy to a read-only media (e.g. a DVD), should be enough for a small business.

Real life incident:  Feb 1, 2017 - GitLabs suffers a major outage after data was accidentally deleted, followed by a sequence of discoveries that none of their five layers of backup or replication techniques “are working reliably or set up in the first place”.  

See <https://techcrunch.com/2017/02/01/gitlab-suffers-major-backup-failure-after-data-deletion-incident/>

### 3)  Use next-generation anti-virus software.

Many of the AV products these days include very clever ways of analysing the behaviour of unknown software, and literally just rolling back all the changes if the AV decides it's not trustworthy.  [Webroot](https://www.webroot.com) is a good example of this, at a very affordable price.

Real life incident:  April 23, 2017 - the Adylkuzz virus started quietly spreading around the internet, and setting up Monero cryptocurrency mining operations on infected PC's.  Because the payload wasn't destructive, it flew under the radar and was missed by many antiviruses for weeks.  

See <https://www.proofpoint.com/us/threat-insight/post/adylkuzz-cryptocurrency-mining-malware-spreading-for-weeks-via-eternalblue-doublepulsar>

### 4)  Be alert, cautious, and sufficiently paranoid.

The last - and hardest - step is to maintain a healthy sense of distrust; sometimes referred to as "[sufficient paranoia](https://pthree.org/2013/10/04/sufficient-paranoia/)".  When you receive an email, ask yourself:  is this email in-character for this person?  Is the spelling what I'd expect?  Is it appropriate?  Is it asking me to take an action (even if that action is just opening a file)?  If so, is it expected, or is it out of the blue?  If it's out of the blue, why?  What's the story behind that?

Real life incident:  Sept 30, 2011 - I received an email from a lady I'd once interviewed for a job.  It was a distraught email saying she was stuck in Wales, had been mugged, lost all her money, and needed a brief loan until she got home.  I wrote her an email (not a reply), telling her email had been hacked; lo and behold, I got a reply!  "It's me... this is for real, i have checked with the consulate but there is nothing really working out, most important is i don't have enough money on please, please i need you to loan me some, i can pay you back once i get home."

I ended up finding her cellphone number and sending her a message - she was at home, safe and sound.

See <https://blog.malwarebytes.com/cybercrime/2014/08/email-hijack-leads-to-i-was-robbed-send-me-money-scam/> -- this was exactly the wording I received.

### Geez, that was a long Facebook post Eric.

It really was, and a few minutes afterwards, this tweet came to my attention:

<https://twitter.com/josephfcox/status/879982828418719744>

It's fun to laugh, but it's a good reminder that there's always going to be a weakness.  You need to structure your business disaster recovery in a way that you can quickly and efficiently deal with a complete wipe-out like this.

### And we're done.

So, to summarise this essay, you need to:

- Always install updates
- Always take backups
- Use AV software with full journaling and rollback capabilities
- Practice sufficient paranoia

With these four steps, you will be as safe as the biggest corporate.  (roughly speaking)


