---
layout: "post"
title: "Selecting a good SMS gateway for Finland"
lang: "en"
date: "2012-02-06T21:42:36+00:00"
permalink: "/en/blogi/2012-02-06_selecting-good-sms-gateway-finland/"
theme: "technology"
tags:
  - "SMS"
translation_key: "d7-18"
original_urls:
  - "/article/selecting-good-sms-gateway-finland"
  - "/node/18"
  - "/en/node/18"
source: "d7"
render_with_liquid: false
---

<p>Today I realized I need to add SMS alerts to my dear Zabbix that tries to keep track of my servers' status. I just don't notice email alerts soon enough. However, when you search for SMS gateway from a search engine, there's something like a million results. Which one do I want to use?</p>
<p>I tried a few of them, and tried to find one that was budget-friendly, flexible, fast and reliable. I know, I shouldn't expect to find one that actually fits all those – however I do think I found one that certainly seems to fit most of them. </p>
<p>Here's my experiences on the ones I remembered.</p>
<dl>
<dt><a href="http://budgetsms.net/">BudgetSMS</a></dt>
<dd>With BudgetSMS I got off with a rocky start – I tried to use their API, but didn't get an SMS despite the OK reply. I actually gave up on it, but a few hours later I was looking through my Junk folders and found an email from BudgetSMS's staff asking for some info on my plans. It seems that BudgetSMS's services hadn't perhaps been used a lot to send to Finland; the support guy sent me some test SMS's through different routes to find out the best one. </dd>
<dd>I got the service working fine, and they were also open to taking a smaller top up payment than officially offered on their web site. I loved the personal service and decided to stay with them. </dd>
<dt><a href="http://www.clickatell.com/">Clickatell</a></dt>
<dd>Clickatell was the first one I found and tried. It seems to be quite big and professional, and the API choices are overwhelming. The worst thing about Clickatell is that you can't actually try sending real SMS's without investing on credit for the minimum amount of messages (which was 400 for me.) The test credit only sends a boilerplate test message instead of the message the user specified.</dd>
<dt><a href="http://www.nexmo.com/">Nexmo</a></dt>
<dd>Nexmo was my second choice; I'm using it for my personal use since BudgetSMS is a bit more expensive for non-company use because of the VAT. The registration process and user interface are good and the prices are quite cheap. Nexmo also had the smallest minimum top up payment of the services I tried; though BudgetSMS was able to do the same when I asked for it. </dd>
<dt>The others</dt>
<dd>I tried a few others, and surfed on at least a dozen more web pages looking for a feasible one. Quite a few didn't work at all to Finland despite the promises, and some were ridiculously expensive for my use. I'm satisfied with my choices and believe both of the services I found are at least better than most of them.</dd>
</dl><p>P.S. I also made a better version of the script, that can be used to send SMSs' from Zabbix. Currently it can only be found from the <a href="https://support.zabbix.com/browse/ZBX-4617">Zabbix JIRA</a>, but I'm hoping that they also replace the old version on the Zabbix documentation with that one.</p>
