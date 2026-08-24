---
layout: "post"
title: "Fixing a hacked Drupal site"
lang: "en"
date: "2019-08-08T14:20:41+00:00"
permalink: "/en/blogi/2019-08-08_fixing-hacked-drupal-site/"
theme: "technology"
tags:
  - "Drupal 7"
  - "security"
  - "php"
  - "hacked"
translation_key: "d7-109"
original_urls:
  - "/article/fixing-hacked-drupal-site"
  - "/node/109"
  - "/en/node/109"
source: "d7"
render_with_liquid: false
---

<h2>Figure out what's going on</h2>

Try to figure out what exactly has been done on the site. If there are no visible content changes, it is possible that your site is used as a proxy server for black-hat <abbr title="Search engine optimisation">SEO</abbr>. Check the web server access logs to see if there are any <abbr title="Unified resource locator">URL</abbr>s that shouldn't be there. Checking Google Search console might also give you some insight in this.

<h2>Fixing the site</h2>

It is always best to restore the site from a clean backup. If this is not possible due to circumstances, make sure to clean the site properly using the instructions below. Please note, that cleaning a hacked Drupal site requires advanced knowledge of Drupal development! If you're uncertain on any of the themes mentioned below, it's best to get help from a seasoned expert.

<h3>Server config</h3>

Make sure you have a valid firewall preventing access to database, cache service etc. If at all possible, consider adding a <abbr title="Web application firewall">WAF</abbr> (modsecurity).

<h3>System files</h3>

Check if the www user of the hacked site has access to other directories than the webroot. Any files the user has read access to should be considered leaked, and any files the user has write access to compromised.<p>

<pre>
# Run as the WWW user to discover any writeable files.
$ find / -perm -2 -type f -exec ls -la {} 2>/dev/null \;
</pre>

<h3 id="rebuilding">Rebuilding</h3>

Fetch all code from upstream, for example using drush make or composer. Check any custom code and themes for backdoors! For Drupal 7 I recommend <a href="https://github.com/wunderio/build.sh">Wunder's build management system</a>, which makes deployments and updates easy by clearly defining all versions and patches necessary for composing the site.

<h3 id="modules">Modules</h3>

Check the system table in your database. It is possible to reference module files outside the Drupal root – so a backdoor module could reside for example under /tmp. Be especially wary of filenames that start with dots (for example ../../tmp/...) and filenames ending in something else than .module – for example .jpg or other innocent-looking filenames.<p>

When reviewing custom code in modules, themes and database PHP fields note that often the hacker has made an effort to conceal the inner workings of the code to prevent it from showing up on greps etc. This means that function calls may be hidden by concatenating the function name in a variable (for example <code>$cmd = "st"."r"."_"."rep"."la"."ce";</code>. Code can often be hidden as Base64 encoded and decoded on runtime. This highlights the fact that all code must be manually checked, not just grepped for suspicious content!

<h3>Any PHP in the database</h3>

The core PHP module shouldn't be used, but if it has, make sure that there are no backdoors in the PHP code saved in the database – for example block visibility definitions and block or node contents. Make sure to search for all opening tags – both <?php and <?= work in most configurations, but there are also other possibilities depending on the PHP version and configuration.<p>

I also wrote a <a href="https://gist.github.com/ZeiP/f05e573a6e0f0a9007d4718a17648b9c">Drush PHP script</a> which helps find the PHP code in a Drupal installation for audit. Note that the script doesn't cover all modules, so be sure to check the coverage and make other checks as necessary!<p>

When checking the PHP code in database, refer to the checking instructions above in <a href="#modules#modules">modules section</a>.

<h3>Users and permissions</h3>

Check the site users and remove any user accounts added by the attacker. Additionally make sure to check your user permissions – be especially wary of the permissions assigned to unauthenticated users (and authenticated users, if you have more than a few trusted users.)

<h3>Change the keys</h3>

Make sure to change:
<ul>
<li>Drupal secret in settings.php to prevent using one-time login links, which can be easily forged if the attacker knows the drupal secret and the user's password hash.</li>
<li>Any SSH keys that are readable to the WWW user</li>
<li>Database keys</li>
<li>If your site uses any APIs (for example mail sending or data retrieval), change the access keys or passwords!</li>
<li>All user's passwords.</li>
</ul>

<h3>Clear the sessions</h3>

Clear the sessions database table to disable any sessions the attacker has opened, otherwise they might be able to get in using an old session. 

<h3>Cron and running processes</h3>

Check the crontab of the WWW user for crons that attempt to re-install any backdoors.<p>

Also check all the processes the WWW user is running and kill any unknown processes.

<h3>Disallow any proxied URLs from your site</h3>

If your site had either unwanted content or proxy URLs, it is useful to speed removing them from the search engines. <p>

First make the unwanted URLs respond with the HTTP status code 410 instead of the standard 404 in your WWW server – for example using something like this in Nginx:
<pre>
location ~ ^/.shop/ {
  return 410;
}
</pre>

You should also add the URLs to your robots.txt as disallowed with a wildcard, if possible. These actions together should speed up removing them from the search index. If there are only a few URLs, you might of course request removing them manually through the search engines' control panels.

<h2>Monitoring the situation</h2>

It's important to keep monitoring the situation after the fixes have been done. Make sure your server logs the real IP in access logs and retains the logs for at least several months.<p>

Log all HTTP traffic, if possible, to detect any remaining backdoors. Logging all traffic allows you to closely analyse what the attacker is doing and figure out the remaining fixes. On a Linux server you can log all traffic with a command such as <code>sudo tcpdump -C 500 -z bzip2 -i lo -s 65535 -w http.pcap 'tcp port 8080'</code>. It's best if you're able to log the traffic after HTTPS offloading (if you're using Varnish or a similar HTTP cache); otherwise you need to do additional steps to be able to decrypt HTTPS traffic.<p>

Check the logged HTTP traffic regularly with Wireshark for some time after fixing the hacked site to check for anything out of the ordinary. Analyse all exploit attempts, both successful and unsuccessful, to make sure no backdoors are left. Analysing the calls is difficult and tiresome, but pays off in the long run when you find the last backdoor that was left and avoid another fixing process or website defacement.<p>

After you think all the backdoors have been fixed and attacks seem to be failing, make sure to check in periodically – the attacker might have left a backdoor that they didn't use right away to be utilised in a few weeks, once the admin is no longer watching closely.
