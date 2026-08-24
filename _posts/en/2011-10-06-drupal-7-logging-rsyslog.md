---
layout: "post"
title: "Drupal 7 logging to rsyslog"
lang: "en"
date: "2011-10-06T15:15:34+00:00"
permalink: "/en/blogi/2011-10-06_drupal-7-logging-rsyslog/"
theme: "technology"
tags:
  - "Drupal"
  - "Drupal 7"
  - "syslog"
  - "rsyslog"
translation_key: "d7-8"
original_urls:
  - "/article/drupal-7-logging-rsyslog"
  - "/node/8"
  - "/en/node/8"
source: "d7"
render_with_liquid: false
---

The usual way to do Drupal 7 logging is to save all the log entries to the database. This has it's benefits and it's problems: On one hand it works fine on every Drupal site without requiring any additional software or access to the server. On the other hand, it causes a few extra database queries (which in itself isn't that horrible, but when there are already plenty, you usually want to do everything in your power to minimize the amount...). And of course, for the logs to be useful they should be monitored and acted upon. This might prove to be a challenge if you're trying to maintain a multisite installation with tens of sites – you probably don't have time to check all the sites' logs every day via the web interface.

The last point can of course be remedied by creating a custom tool that queries all the sites' databases and gathers the data to one interface. I haven't seen this kind of thing done ready, so it might be that you need to do it yourself. And usually you also have to add all new sites to one more system – which you'll probably forget anyway.

<h2>Ok, ok, what's your point?</h2>

You can actually do this better – logging all the site activity without the small overhead and monitoring difficulties. This is possible via syslog (of course this usually requires that you host your own server – otherwise you probably won't be able to set this up.)

Syslogd is the server software responsible for all the logging your Linux system does. It logs something probably every minute: Incoming emails, outgoing emails, shell connection attempts, cron runs... You name it, syslog has it. It's a highly dedicated tool that does one thing, and one thing only: Logs whatever something in your system wants it to log.

Therefore it's sensible to use syslog to log also your Drupal installations' problems and errors. Less surprisingly, Drupal already has a module for this (too): The Drupal core includes a module called Syslog. 

<h2>So how do I do it?</h2>

It's quite easy to use: You actually just need to enable the module and go to admin/config/development/logging. Fill the following fields and click save, and you're halfway done:

<dl>
<dt>Syslog identity</dt>
<dd>This should be a string that you use to separate the installation from others that you have on your servers. I usually use the site domain name without the full stop, so www.zeip.eu becomes zeipeu.</dd>
<dt>Syslog facility</dl>
<dd>This is a kind of ”channel” that the syslogd uses to divide different software to different log files according to it's rules. Drupal only lets you use the LOCAL facilities – I myself use LOG_LOCAL1. LOG_LOCAL7 is reserved in some systems, so I don't suggest using it.</dd>
</dl>

When you've done this, you're already logging your Drupal errors to syslogd. But it might still not be saving them: It hasn't been told what to do with the facility you chose. So next, let's setup our syslogd. If you're using Debian, you probably have rsyslog as your syslogd, so I'll demonstrate the configuration of that one. If you're using something else, you'll probably want to use a similar config, but that one you'll have to figure out yourself.

On Debian, create a new file as /etc/rsyslog.d/drupal.conf with the following content:

<code>$template RFC3164fmt,"<%PRI%>1 %TIMESTAMP:::date-rfc3339% %HOSTNAME% %syslogtag%- - - %msg%\n"
local1.*                                -/var/log/drupal.log;RFC3164fmt</code>

The first row configures a new template for logging format, and the second row defines that all messages on facility local1 are logged to /var/log/drupal.log using the format. If you chose something else than LOG_LOCAL1, change the second row accordingly.

Now you can log in to your site and after that check that your login has been recorded to /var/log/drupal.log. Then you can disable the ”Database logging” module to save a few queries. Congrats, you're done!
