---
layout: "post"
title: "Installing ModSecurity to Nginx in Debian 10"
lang: "en"
date: "2019-08-09T09:19:12+00:00"
permalink: "/en/blogi/2019-08-09_installing-modsecurity-nginx-debian-10/"
theme: "technology"
tags:
  - "debian 10"
  - "modsecurity"
  - "nginx"
translation_key: "d7-110"
original_urls:
  - "/article/installing-modsecurity-nginx-debian-10"
  - "/node/110"
  - "/en/node/110"
source: "d7"
render_with_liquid: false
---

Debian finally has a ModSecurity package ready for use in the repository. However, using it with Nginx requires a few steps, which it took a while to figure out.

<pre>
# Create a work dir for the compilation process
$ mkdir modsecurity-tmp

# Install modsecurity
$ libmodsecurity3 libmodsecurity-dev

# Fetch sources
$ git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git
$ apt-get source nginx-full

# Figure out the necessary configuration options
$ /usr/sbin/nginx -V

$ cd nginx-[version]
# Configure. Replace NGINX OPTIONS with all the options from the above command <strong>except for options starting "--add-dynamic-module"</strong>.
# https://github.com/SpiderLabs/ModSecurity-nginx/issues/159 and https://github.com/SpiderLabs/ModSecurity-nginx/issues/117
$ ./configure [NGINX OPTIONS] --add-dynamic-module=../ModSecurity-nginx

# Compile.
$ make modules

# Copy to location
$ sudo mkdir /etc/nginx/modules
$ sudo cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/ngx_http_modsecurity_module.so

# Load the module.
$ echo "load_module /etc/nginx/modules/ngx_http_modsecurity_module.so;" | sudo tee /etc/nginx/modules-available/modsecurity.conf
$ sudo ln -s /etc/nginx/modules-available/modsecurity.conf /etc/nginx/modules-enabled/

# Add configuration
$ sudo mkdir /etc/nginx/modsec
$ sudo curl -o /etc/nginx/modsec/modsecurity.conf https://raw.githubusercontent.com/SpiderLabs/ModSecurity/v3/master/modsecurity.conf-recommended

# You might also want to change the SecRuleEngine parameter in /etc/nginx/modsec/modsecurity.conf to On.
# Load the missing file per https://github.com/SpiderLabs/ModSecurity/issues/1941
$ sudo curl -o /etc/nginx/modsec/unicode.mapping https://raw.githubusercontent.com/SpiderLabs/ModSecurity/49495f1925a14f74f93cb0ef01172e5abc3e4c55/unicode.mapping
$ echo "Include \"/etc/nginx/modsec/modsecurity.conf\"\nSecRule ARGS:testparam \"@contains test\" \"id:1234,deny,status:403\"" | sudo tee /etc/nginx/modsec/main.conf

# Then add these lines to your site's server block:
    modsecurity on;
    modsecurity_rules_file /etc/nginx/modsec/main.conf;

# Restart Nginx
$ sudo service nginx restart
</pre>

Voilá. If you changed SecRuleEngine to on, adding ?testparam=test to your website URL should return Forbidden 403. Now you can start figuring out the correct ruleset for your site.
