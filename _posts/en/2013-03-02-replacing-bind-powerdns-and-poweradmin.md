---
layout: "post"
title: "Replacing BIND with PowerDNS and PowerAdmin"
lang: "en"
date: "2013-03-02T18:28:55+00:00"
permalink: "/en/blogi/2013-03-02_replacing-bind-powerdns-and-poweradmin/"
theme: "technology"
tags:
  - "powerdns"
  - "dns"
  - "server administration"
translation_key: "d7-97"
original_urls:
  - "/article/replacing-bind-powerdns-and-poweradmin"
  - "/node/97"
  - "/en/node/97"
source: "d7"
render_with_liquid: false
---

<h2>Why the switch?</h2>
<p>Recently I started wondering if there would be something better than the old, trustworthy BIND for all my DNS daemon needs. BIND is good, don't get me wrong, but I have to say that I don't feel it makes my job as an administrator for hundreds of domains any easier being (primarily) based on weirdly syntaxed plain-text files that are quite error-prone. So, encouraged by my not-so-recent discovery of Nginx, a very good alternative for the industrial standard Apache, I went on with my crusade to find a perfect DNS daemon.</p>
<p>I found a variety of candidates that all seemed good and useable, but based on some further enquiries it seemed that BIND was one of the quite few that had enough users to make it stable. Enter <a href="http://www.powerdns.com/">PowerDNS</a>, which has quite many users and seems to be commonly thought of as a more secure and better alternative for BIND. So I decided to give it a shot, especially after I found out that it has a bearable admin tool, PowerAdmin. </p>
<p>One important point in deciding if I'd go on with the switch was finding out if it'd actually make my life easier. Security is a good point itself, but changing is also a lot of work. Here are a few points I based my decision on:</p>
<ul>
<li>Administration interface features templates, the changes of which can be applied to all the zones the template is used on. This was an important requirement; previously I was using ISPconfig as an admin interface, and although it, too, has templates, they are only applied when the zone is installed and any changes after that are not reflected on the zones. So any time I want to make a simple change to a specific set of domains, I had to do it one-by-one. Not good.
<li>Administration interface allows control of some zones be delegated to other users; so at least technically I can give my customers an user account with which they can then modify the zone themselves. </li>
<li>Switchover was supposed to be easy, thanks to the zone2sql program that the kind folk of PowerDNS have made for us.</li>
<li>And of course the security aspect was also important :)</li>
</ul>
<h2>What's there to it?</h2>
<p>It's quite simple, really. But there were a few problems that I wasn't expecting, and that took a bit of time to resolve. It's supposed to be easier in PowerDNS 3.0, but since Debian Squeeze currently only has 2.9.something, I had to fight my way though that. Here's how.</p>
<p>Start by installing PowerDNS. This was the easy part, so I'm not going to replicate that here. At least Debian has separate packages for the core and the storage module (which, for me, was MySQL); remember to install both!</p>
<p>Then comes the (more) tricky part, migrating the data:</p>
<dl>
<dt>First, find your BIND configuration file and use zone2sql to export the records into a SQL file:</dt>
<dd>zone2sql --slave --named-conf=/etc/bind/named.conf.local --start-id=1 > records.sql</dd>
<dt>Create domain insert clauses (this is a step that zone2sql apparently does itself in PowerDNS 3). </dt>
<dd>Get the awk script at <a href="http://wiki.powerdns.com/trac/wiki/Zone2SQLFAQ#domainsimport">Zone2SQL FAQ</a>.</dt>
<dd>./import2zone.awk records.sql > domains.sql</dd>
<dt>Run the SQL scripts, the order shouldn't matter.</dt>
</dl>
<p>After this you should have your data migrated and server set up. However, in my environment a few of the domains did not work right after the migration. This was because the name value of those domains (both in domains and records tables) included a dot after the domain name. I removed these by running one UPDATE clause for the domains table and one for the records table and tadaa, everything worked fine. </p>
<p>All in all, it wasn't exactly difficult, but since some of these tips were a bit hard to find, I decided to write them up for future reference. Hope it's useful for someone else also!</p>
