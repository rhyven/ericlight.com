Title: Making MindTouch's Dekiwiki work on Debian Stretch
Author: Eric Light
Tags: Tech, Security
Date: 2017-09-17

We had accumulated a certain amount of technical debt, due to a Wiki solution that was selected a few years ago:  Dekiwiki, by MindTouch.  Unfortunately a few months after implementation, MindTouch Core (which Dekiwiki builds on) was [well-and-truly deprecated](https://mindtouch.com/resources/mindtouch-core-and-platform-this-is-the-end-beautiful-friend) back in 2013.

It all happened before my time, but it seems as if Dekiwiki came as a pre-built VMware Appliance, based on Debian Etch ([Debian 4.0; released in 2007](https://en.wikipedia.org/wiki/Debian_version_history#Debian_4.0_.28Etch.29)).  After giving our Dekiwiki environment some serious side-eye for a while, I finally decided to get my hands dirty and try to upgrade it.

Jedd, over at Jeddi.org, wrote [a really helpful post back in 2015](https://jeddi.org/b/2015/08/30/resurrecting-mindtouch-dekiwiki/) about his experiences updating the ageing version of Debian that the VM is based on.  The whole Dekiwiki image is held together by sticky-tape, but that post is really helpful in getting Etch upgraded to Wheezy.

Here are a couple **additional** things I've had to do (please, please look at Jedd's post above - he covers a whole lot that I'm not covering here):

Upgrading Etch -> Lenny:
-----------------------------

Follow [the guide at Jeddi.org](https://jeddi.org/b/2015/08/30/resurrecting-mindtouch-dekiwiki/) above to get to Lenny.  I can't remember much failing for that upgrade step, but I remember something happened.

From Lenny -> Squeeze:
----------------------

**DNS Breaks.**  You'll notice that SSH takes aaaages to log into, and other things will start being slow and complaining.  

Resolve this by editing the 'hosts' line in /etc/nsswitch.conf:

`hosts:          files dns`

Originally this reads `hosts:          files mdns4_minimal [NOTFOUND=return] dns mdns4`

Note I'm not actually sure this happened between Lenny and Squeeze; it may have been from Squeeze to Wheezy.  \*shrug\*


From Squeeze -> Wheezy:
-----------------------

**MySQL breaks.**  When visiting the wiki, you'll be informed that it couldn't access the backend, and that the API might be warming up.  However, you'll notice that the MySQL service fails to start.  When you run 'mysqld' from command line, you'll see it's missing a folder.  

Resolve this by running `mkdir /var/lib/mysql-files ; chown mysql:mysql /var/lib/mysql-files`

From Wheezy -> Jessie (upgrade-only):
-------------------------------------

**Apache breaks.**  You'll notice Apache starts serving just the contents of /var/www.  This is because the Apache config file now looks for \*.conf in /etc/apache2/sites-enabled; of course, the dekiwiki config file doesn't have the .conf ending.

Resolve this by running `mv /etc/apache2/sites-enabled/dekiwiki /etc/apache2/sites-enabled/dekiwiki.conf`

From Wheezy -> Jessie (dist-upgrade):
-------------------------------------

**Mono breaks.**  If you upgrade mono, Dekiwiki will fall back into unlicensed mode.  The licensing engine will no longer be able to interpret license files correctly.  You'll see the error "Server license validation failed. The license signature is not valid."

Resolve this by holding back the mono packages before you run a dist-upgrade:

`apt-mark hold libapache2-mod-mono libmono-2.0-1 libmono-2.0-dev libmono-accessibility2.0-cil libmono-accessibility4.0-cil libmono-bytefx0.7.6.2-cil libmono-c5-1.1-cil libmono-cairo2.0-cil libmono-cairo4.0-cil libmono-cecil-private-cil libmono-codecontracts4.0-cil libmono-compilerservices-symbolwriter4.0-cil libmono-corlib2.0-cil libmono-corlib4.0-cil libmono-cscompmgd8.0-cil libmono-csharp4.0-cil libmono-custommarshalers4.0-cil libmono-data-tds2.0-cil libmono-data-tds4.0-cil libmono-data2.0-cil libmono-db2-1.0-cil libmono-debugger-soft2.0-cil libmono-debugger-soft4.0-cil libmono-dev libmono-firebirdsql1.7-cil libmono-getoptions2.0-cil libmono-http4.0-cil libmono-i18n-cjk4.0-cil libmono-i18n-mideast4.0-cil libmono-i18n-other4.0-cil libmono-i18n-rare4.0-cil libmono-i18n-west2.0-cil libmono-i18n-west4.0-cil libmono-i18n2.0-cil libmono-i18n4.0-all libmono-i18n4.0-cil libmono-ldap2.0-cil libmono-ldap4.0-cil libmono-management2.0-cil libmono-management4.0-cil libmono-messaging-rabbitmq2.0-cil libmono-messaging-rabbitmq4.0-cil libmono-messaging2.0-cil libmono-messaging4.0-cil libmono-microsoft-build-engine4.0-cil libmono-microsoft-build-framework4.0-cil libmono-microsoft-build-tasks-v4.0-4.0-cil libmono-microsoft-build-utilities-v4.0-4.0-cil libmono-microsoft-build2.0-cil libmono-microsoft-csharp4.0-cil libmono-microsoft-visualc10.0-cil libmono-microsoft-web-infrastructure1.0-cil libmono-microsoft8.0-cil libmono-npgsql2.0-cil libmono-npgsql4.0-cil libmono-opensystem-c4.0-cil libmono-oracle2.0-cil libmono-oracle4.0-cil libmono-peapi2.0-cil libmono-peapi4.0-cil libmono-posix2.0-cil libmono-posix4.0-cil libmono-rabbitmq2.0-cil libmono-rabbitmq4.0-cil libmono-relaxng2.0-cil libmono-relaxng4.0-cil libmono-security2.0-cil libmono-security4.0-cil libmono-sharpzip2.6-cil libmono-sharpzip2.84-cil libmono-sharpzip4.84-cil libmono-simd2.0-cil libmono-simd4.0-cil libmono-sqlite2.0-cil libmono-sqlite4.0-cil libmono-system-componentmodel-composition4.0-cil libmono-system-componentmodel-dataannotations4.0-cil libmono-system-configuration-install4.0-cil libmono-system-configuration4.0-cil libmono-system-core4.0-cil libmono-system-data-datasetextensions4.0-cil libmono-system-data-linq2.0-cil libmono-system-data-linq4.0-cil libmono-system-data-services-client4.0-cil libmono-system-data-services4.0-cil libmono-system-data2.0-cil libmono-system-data4.0-cil libmono-system-design4.0-cil libmono-system-drawing-design4.0-cil libmono-system-drawing4.0-cil libmono-system-dynamic4.0-cil libmono-system-enterpriseservices4.0-cil libmono-system-identitymodel-selectors4.0-cil libmono-system-identitymodel4.0-cil libmono-system-ldap2.0-cil libmono-system-ldap4.0-cil libmono-system-management4.0-cil libmono-system-messaging2.0-cil libmono-system-messaging4.0-cil libmono-system-net4.0-cil libmono-system-numerics4.0-cil libmono-system-runtime-caching4.0-cil libmono-system-runtime-durableinstancing4.0-cil libmono-system-runtime-serialization-formatters-soap4.0-cil libmono-system-runtime-serialization4.0-cil libmono-system-runtime2.0-cil libmono-system-runtime4.0-cil libmono-system-security4.0-cil libmono-system-servicemodel-discovery4.0-cil libmono-system-servicemodel-routing4.0-cil libmono-system-servicemodel-web4.0-cil libmono-system-servicemodel4.0-cil libmono-system-serviceprocess4.0-cil libmono-system-transactions4.0-cil libmono-system-web-abstractions4.0-cil libmono-system-web-applicationservices4.0-cil libmono-system-web-dynamicdata4.0-cil libmono-system-web-extensions-design4.0-cil libmono-system-web-extensions4.0-cil libmono-system-web-mvc1.0-cil libmono-system-web-mvc2.0-cil libmono-system-web-routing4.0-cil libmono-system-web-services4.0-cil libmono-system-web2.0-cil libmono-system-web4.0-cil libmono-system-windows-forms-datavisualization4.0-cil libmono-system-windows-forms4.0-cil libmono-system-xaml4.0-cil libmono-system-xml-linq4.0-cil libmono-system-xml4.0-cil libmono-system2.0-cil libmono-system4.0-cil libmono-tasklets2.0-cil libmono-tasklets4.0-cil libmono-wcf3.0-cil libmono-web4.0-cil libmono-webbrowser2.0-cil libmono-webbrowser4.0-cil libmono-webmatrix-data4.0-cil libmono-windowsbase3.0-cil libmono-windowsbase4.0-cil libmono-winforms2.0-cil libmono0 libmono2.0-cil mono-2.0-devel mono-2.0-gac mono-4.0-gac mono-apache-server2 mono-common mono-csharp-shell mono-dmcs mono-gac mono-gmcs mono-mcs mono-runtime mono-utils mono-xbuild`

**Note:**  Some of these can certainly be unheld.  I haven't yet gone through and identified exactly which component is breaking on upgrade.  If you put in the effort to determine the culprit, please let me know.

That's all!  You should now have Dekiwiki running on Debian Stretch!  I'm planning to upgrade it to Debian Buster in the next week or two.
