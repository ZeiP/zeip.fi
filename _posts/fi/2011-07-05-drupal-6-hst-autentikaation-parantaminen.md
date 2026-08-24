---
layout: "post"
title: "Drupal 6 -HST-autentikaation parantaminen"
lang: "fi"
date: "2011-07-05T09:03:08+00:00"
permalink: "/fi/blogi/2011-07-05_drupal-6-hst-autentikaation-parantaminen/"
theme: "technology"
tags:
  - "Drupal"
  - "Drupal 6"
  - "VRK HST"
translation_key: "d7-3"
original_urls:
  - "/artikkeli/drupal-6-hst-autentikaation-parantaminen"
  - "/node/3"
  - "/fi/node/3"
source: "d7"
render_with_liquid: false
---

Sunnuntaina kirjoitin <a href='"/artikkeli/drupal-6-autentikointi-apache-2ssa-vrkn-hst-kortilla">Drupal 6 -autentikoinnista HST-kortilla</a>. Kirjoituksessa väitin myös aikovani laajentaa Certificate Login -modulia mahdollistamaan OpenID-tyylisen ratkaisun, jossa käyttäjän nimeä ei tarvitse olla saatavissa suoraan varmenteesta vaan käyttäjä voidaan liittää mielivaltaiseen määrään eri varmenteita. Tämä on Drupal 6:ssa mahdollista authmap-taulun avulla, jota Drupalin oma OpenID-modulikin käyttää. 

Käytin viime yöstä muutaman tunnin asian tutkimiseen ja sain aikaiseksi toimivan laajennuksen moduliin, jonka suurin jäljellä oleva puute on se, ettei käyttäjä voi tarkastella itseensä liitettyjä varmenteita eikä poistaa niitä. Lisään tuon ominaisuuden, mikäli patchini hyväksytään osaksi modulia. Tässä kuitenkin ohje ominaisuuden omatoimiseen käyttöön ottamiseen. 

<h2>Koodimuutokset</h2>

Ensimmäiseksi ominaisuutta hyödyntääkseen tulee patchia käyttäen toteuttaa koodimuutokset koodiin. Suosittelen hakemaan Drupal.orgin versionhallinnasta <a href="http://drupal.org/node/206002/git-instructions/master">ohjeen mukaisesti</a> uusimman version koodista, koska patch on tehty sitä vasten:

<code>$ git clone http://git.drupal.org/project/certificatelogin.git
$ cd certificatelogin</code>

Tämän jälkeen käy lataamassa patch <a href="http://drupal.org/node/1209114">issuesta</a>. Siirrä ladattu patch certificatelogin-hakemistoon, jonka Git juuri loi. Siirry hakemistoon, ja aja seuraava komento:

<code>$ patch -p0 < certificatelogin-authmap.patch
patching file certificatelogin.module</code>

Jos tulosteena tuli jotain muuta kuin yllä mainittu (erityisesti jos tulosteessa lukee FAILED), patch epäonnistui. Tällöin ei kannata jatkaa ennen ongelman korjaamista. 

Siirrä vielä moduli Drupal-asennukseesi sopivaan hakemistoon (esim. sites/default/modules/custom).

<h2>Asetukset</h2>

Kun olet siirtänyt modulin asennukseesi ja laittanut sen päälle, käy vielä modulin asetussivulla (admin/settings/certificatelogin). Jos olet aiemmin käyttänyt modulia, huomaat yhden uuden valinnan: ”Use authmap instead of user name.” Klikkaa se päälle. Tämän jälkeen mene kirjautuneena käyttäjän osoitteeseen /login ja klikkaa Login-painiketta. Jos kaikki meni kuten kuuluu, ruudullasi lukee nyt ”Successfully added” ja perässä varmenteesi tunniste. Nyt varmennekirjautuminen toimii ilman, että käyttäjätunnuksen tarvitsee olla varmennetunnus. 

Voit liittää edellämainitulla tavalla käyttäjätunnukseen useammankin varmenteen. Varmenteita voi tällä hetkellä poistaa ainoastaan suoraan tietokannasta authmap-taulusta. 

That's it, have fun!
