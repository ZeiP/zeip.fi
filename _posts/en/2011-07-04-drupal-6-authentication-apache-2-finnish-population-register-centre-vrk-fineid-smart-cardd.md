---
layout: "post"
title: "Drupal 6 authentication on Apache 2 with a Finnish Population Register Centre (VRK) FINeID smart card"
lang: "en"
date: "2011-07-04T18:33:53+00:00"
permalink: "/en/blogi/2011-07-04_drupal-6-authentication-apache-2-finnish-population-register-centre-vrk-fineid-smart-cardd/"
theme: "technology"
tags:
  - "autentikaatio"
  - "Apache 2"
  - "VRK HST"
  - "Drupal 6"
  - "varmenteet"
  - "Drupal"
translation_key: "d7-1"
original_urls:
  - "/article/drupal-6-authentication-apache-2-finnish-population-register-centre-vrk-fineid-smart-cardd"
  - "/node/2"
  - "/en/node/2"
source: "d7"
render_with_liquid: false
---

Months ago I acquired the Finnish FINeID smart card produced by the Police and Population Register Centre, even though plans about discontinuing it altogether have already been made. In addition to being a traditional identification card, it has a certificate that can be used for both authentication and signing documents – although quite few services actually support it (pretty much the only ones are public sector and Itella NetPosti – one bank did allow it for quite a while, but they discontinued it stating lack of use). However, I've gained some interest on using it for authentication on my own services – I use e.g. my own OpenID service in quite a few places, so authenticating to that with a smart card would be quite cool (and, to be honest, that's probably the only benefit that I would gain from that...)

My OpenID service is based on Drupal, and I assumed that using a user certificate to authenticate to Drupal would be a piece of cake – there's even <a href="http://drupal.org/project/certificatelogin">a module</a> for that (too.)  Newsflash: It isn't. Apache is like a small crybaby, the <abbr title="Population Register Centre">PRC</abbr> root certificates are in the wrong format and life just plain sucks…

To be fair, the authentication was quite easy to install in the end. You just needed to realize, that either Firefox or the fine smart card software by Fujitsu like to bug, so if the thing just doesn't seem to work even when it should, restarting either your browser or your computer might just be the relief you need… (Figuring this out took me most of the hours spent on this project… The smart card worked for every other service, but for some reason it didn't for mine until Firefox restart.)

<h2>Installing client certificate authentication to Apache</h2>

Start by choosing the root certificate you want/need. The PRC has both a generic root certificate (”VRK Gov. Root CA”) and a root for citizen certificates (”VRK Gov. CA for Citizen Qualified Certificates”). The generic root makes it possible to use any PRC-issued client certificates with your service – that is, also organization and health care professionals' smart cards' certificates. The citizen certificate root, on the other hand, assumably contains only the FINeID certificates issued in the electric identity cards. I personally used the generic root, even though my sites rarely have any users in addition to myself – mostly just because I couldn't think of a reason not to use the generic root, and I trust all the PRC client certificates anyway.

When you've selected the root you want, you need to figure out where you want to obtain it. You can either download it from the PRC site or, and this is a bit more secure, you can extract it off a electrical identity card you have, if you just have a Linux computer that knows how to use the card (which isn't all that easy by itself… ;) )  Extracting the root certificate off an issued certificate better ensures that you actually do use the one and only PRC root instead of someone else's forged version – after all you've probably fetched your card directly from the police station, so it probably is real. If you download the root certificate from the Web page, you should check the validity of the certificate by checking it's fingerprint from an independent source. 

If you want to obtain the certificate by extracting it off the card, use the following commands depending on your choice of root:

a) Generic root
<code>$ pkcs15-tool -r $(pkcs15-tool -c|grep  -A4 "Root"|grep ID|cut -d: -f2) > vrkrootc.pem</code>
b) Citizen certificate root
<code>$ pkcs15-tool -r $(pkcs15-tool -c|grep  -A4 "Citizen Qualified"|grep ID|cut -d: -f2) > vrkcqc.pem</code>

If you want to obtain the certificate from the PRC site, just download it. The certificate, however, is in the wrong format – PRC disitributes their root certificates in DER form, and Apache wants the certificates in PEM format. So you just need to convert it to PEM:
<code>$ openssl x509 -in vrkrootc.crt -inform DER -outform PEM -out vrkrootc.pem</code>
(If you used the citizen certificate root, the file name is vrkcqc.)

Place the certificates in a good spot on your server. /etc/ssl works just fine.

After this you just need to add a few lines to Apache's SSL vhost file (in Debian it's in /etc/apache2/sites-enabled):
<code>SSLCACertificateFile /etc/ssl/vrkrootc.crt
SSLVerifyClient optional
SSLVerifyDepth 2</code>
SSLVerifyDepth value needs to be at least 2, if you use the generic root – in this case there is the abovementioned citizen certificate root between the generic root and the user's certificate, so the user certificate's ”depth” in the certificate chain is 2. If you use the citizen certificate root, setting the depth to 1 should be enough since the user certificate is directly in the given root.

These should have information about user's possible PRC certificate reach Drupal in the environment variable $_SERVER. Since the certificate is defined as optional, not required, also those not having / giving their certificate can access your site just like in the old days.

<h2>Configuring the Drupal module</h2>

When the Apache end is in good shape, you just need to have Drupal actually understand something of the authentication information given to it by Apache. This requires the <a href="http://drupal.org/project/certificatelogin">Certificate Login</a> module. 

When you've installed the module and enabled it, visit the module settings (Admin => Site settings => Certificate Login Settings) and define something like the following settings:

* Enable/Disable: Enabled
* PHP code to retrieve user name: ”$_SERVER['SSL_CLIENT_S_DN_CN']” (without the outer quotes)
* Account creation: Enabled

These settings have your certificate user's user names as full name + SATU (Sähköinen asiointitunnus = electrical citizen ID). My personal goal is to expand the Certificate Login module to also be able to save the SATU in a separate field in the user profile, so that the user's user name doesn't need to be directly derived of the certificate. Also a port to Drupal 7 would be nice… Let's see what I get done in the coming weeks. Until that, that's pretty much all you can do with current software. 'njoy.

<h2>Troubleshooting</h2>

Isn't it working? Set Apache's logging to something a little more extensive in the SSL vhost file, value debug should be good. Below are some problems I ran into:
<dl>
<dt>[error] [client 192.0.2.0] Certificate Verification: Certificate Chain too long (chain has 2 certificates, but maximum allowed are only 1)</dt>
<dd>Adjust the SSLVerifyDepth value so, that it is equal or greater than n in ”chain has n certificates”.</dd>
<dt>[info] SSL Library Error:  error::SSL routines:SSL3_GET_CLIENT_CERTIFICATE:peer did not return a certificate No CAs known to server for verification?</dt>
<dd>The client didn't pass a certificate. After a fresh restart of Apache, check from the error_log that it found the CA information:
<code>[debug] ssl_engine_init.c(598): Configuring client authentication
[debug] ssl_engine_init.c(1193): CA certificate: /C=FI/ST=Finland/O=Vaestorekisterikeskus CA/OU=Valtion kansalaisvarmenteet/CN=VRK Gov. CA for Citizen Qualified Certificates</code>
Assuming this is ok, I got rid of this problem just by restarting my browser.</dd>

<h2>More to read</h2>

These are some of the resources I used while troubleshooting this. Unfortunately they're only in Finnish...
<ul>
<li><a href="http://linux.fi/wiki/HST">Linux.fi-wikin sivu HST:stä</a></li>
<li><a href="http://linux.fi/wiki/Apache_httpd#S.C3.A4hk.C3.B6isen_henkil.C3.B6kortin_tuki">Linux.fi-wikin sivu HST-kortin asentamisesta Apacheen</a></li>
<li><a href="http://www.helsinki.fi/~aulaskar/tietos/korttitunnistus/kortti.html">Ismo Aulaskarin jo muutaman vuoden vanha ohje kortin käyttämisestä Linux-ympäristössä</a></li>
</ul>
