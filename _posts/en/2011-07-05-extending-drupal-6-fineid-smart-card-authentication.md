---
layout: "post"
title: "Extending the Drupal 6 FINeID smart card authentication"
lang: "en"
date: "2011-07-05T09:19:50+00:00"
permalink: "/en/blogi/2011-07-05_extending-drupal-6-fineid-smart-card-authentication/"
theme: "technology"
tags:
  - "Drupal"
  - "Drupal 6"
  - "VRK HST"
translation_key: "d7-3"
original_urls:
  - "/article/extending-drupal-6-fineid-smart-card-authentication"
  - "/node/4"
  - "/en/node/4"
source: "d7"
render_with_liquid: false
---

On Sunday I wrote about <a href="http://www.zeip.eu/node/2">Drupal 6 authentication with a FINeID card</a>. In it I also claimed I was planning on expanding the Certificate Login module to facilitate an option for OpenID style identification, in which the user name doesn't need to be taken directly from the certificate but the user can instead be attached to any number of certificates. This is possible by using Drupal 6's authmap-table, which also Drupal's own OpenID module uses.

I spent a few hours last night to investigate the possibilities and managed to write a working extension for the module, in which the greatest shortcoming is that the user can't inspect certificates attached to him/herself and can't remove them. If the patch is accepted to the module, however, I will add that feature also. Meanwhile, here's a short tutorial for anyone interested in taking matters in their own hands and using the patch. 

<h2>Code changes</h2>

To use the new feature, you first need to apply the patch to the code. I recommend taking your module code from Drupal.org VCS <a href="http://drupal.org/node/206002/git-instructions/master">according to the instructions</a>, because the patch has been taken against it:

<code>$ git clone http://git.drupal.org/project/certificatelogin.git
$ cd certificatelogin</code>

After this, download the patch from <a href="http://drupal.org/node/1209114">the issue</a>. Move the downloaded patch to the certificatelogin directory that Git just created for you. Change to the directory and run the following command to apply the patch:

<code>$ patch -p0 < certificatelogin-authmap.patch
patching file certificatelogin.module</code>

If the output differs from the above (and especially if the output has ”FAILED” in it), the patching probably failed. In this case you shouldn't continue until you've successfully completed the patching.

One more thing: Move the module to your Drupal installation to a nice and warm directory (e.g. sites/default/modules/custom).

<h2>Settings</h2>

When you've moved the module under your Drupal installation and enabled it, bear with me a bit more: Visit the module settings site (admin/settings/certificatelogin). If you've previously used the module, you'll notice a new choice has appeared: ”Use authmap instead of user name.” Click it on. After this (save your settings and) visit path /login as a logged-in user. Click on the login button. If everything is as it should be, you now have a message ”Successfully added” and your certificate's information on your screen. Now certificate login works without the user name having to be the certificate ID string.

Using the method above, you can attach multiple certificates to your user account. Unfortunately, for now you can only remove certificates directly from the database authmap table. 

That's it, have fun!
