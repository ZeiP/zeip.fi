---
layout: "post"
title: "Drupal 6 -autentikointi Apache 2:ssa VRK:n HST-kortilla"
lang: "fi"
date: "2011-07-03T22:04:28+00:00"
permalink: "/fi/blogi/2011-07-03_drupal-6-autentikointi-apache-2ssa-vrkn-hst-kortilla/"
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
  - "/artikkeli/drupal-6-autentikointi-apache-2ssa-vrkn-hst-kortilla"
  - "/node/1"
  - "/fi/node/1"
source: "d7"
render_with_liquid: false
---

Hankin jo kuukausia sitten kuopattavaksikin jo kaavaillun Väestörekisterikeskuksen ja poliisin tuottaman sähköisen henkilökortin. Normaalin henkilöllisyystodistuksen lisäksi se sisältää siis varmenteen, jota voi käyttää sekä tunnistautumiseen että asiakirjojen allekirjoittamiseen – olkoonkin, että harvat palveluntarjoajat sitä ottavat vastaan (oikeastaan ainoina ovat viranomaiset ja Itellan NetPosti – Osuuspankkikin kuoppasi oman HST-tukensa vähäisen käytön vuoksi.)  Itseäni kuitenkin alkoi kiinnostamaan kortin ottaminen käyttöön omaan omiin palveluihini tunnistautumiseen liittyen - käytän paljon mm. omaa OpenID-palveluani, johon tunnistautuminen henkilökortilla olisi melko coolia (muuta hyötyä siitä tuskin olisi…)

OpenID-palveluni pyörii Drupalin päällä, ja oletin, että käyttäjävarmenneautentikaatio siihen on lasten leikkiä, kun tarkoitukseen on <a href="http://drupal.org/project/certificatelogin">modulikin</a>. Newsflash: Ei se ole. Apache kiukuttelee vastaan, VRK:n juurivarmenteet ovat väärässä muodossa ja elämä on muutenkin kovin kurjaa…

Lopun perin todennus on kohtalaisen helppo asentaa – kunhan vaan tajuaa, että joko Firefox tai Fujitsun hieno korttiajuri tykkäävät kaatuilla välillä, eli jos homma ei tunnu toimivan niin eri selaimen käyttäminen ja/tai selaimen uudelleenkäynnistys voi olla kaipaamasi helpotus… (Tämän tajuaminen vei itseltäni aika monta tuntia, koska varmenne toimi kuitenkin hienosti useimmissa muissa HST-palveluissa.)

<h2>Varmennetodennuksen asettaminen Apacheen</h2>

Aloita valitsemalla haluamasi juurivarmenne. VRK:lla on sekä yleinen juurivarmenne (”VRK Gov. Root CA”) että kansalaisvarmennejuuri (”VRK Gov. CA for Citizen Qualified Certificates”). Yleinen juuri mahdollistaa kaikkien VRK:n myöntämien asiakasvarmenteiden käyttämisen palvelussa – siis myös esimerkiksi organisaatio- ja terveydenhuollon ammattihenkilöiden varmenteet. Henkilövarmennejuuri taas sisältänee lähinnä kansalaisille myönnettävät sähköiset henkilökortit. Itse käytin tässä yleistä juurta, vaikka käyttäjiä palveluilla on yleensä itseni lisäksi 0 – ihan vaan siksi, että en keksinyt hyviä syitä rajoittaa, koska joka tapauksessa kyseessä ovat luotetut varmenteet.

Kun olet löytänyt haluamasi varmennejuuren, päätä vielä mistä haluat hakea sen. Voit hakea juurivarmenteen joko VRK:n sivustolta tai purkaa sen omistamallasi Linux-koneella sähköisestä henkilökortista (jos siis olet saanut kortin toimimaan koneessasi…)  Juurivarmenteen purkaminen henkilökortista varmistaa paremmin, että kyseessä on oikea varmenne – olet hakenut korttisi todennäköisesti suoraan poliisilta, eli kortti tuskin on väärennetty. Sen sijaan netistä haettaessa varmenteen aitous pitäisi tarkistaa sormenjäljen perusteella jostain riippumattomasta lähteestä. 

Jos haluat hakea varmenteen kortilta, käytä seuraavia komentoja, riippuen juurivalinnastasi:

a) Yleinen juuri
<code>$ pkcs15-tool -r $(pkcs15-tool -c|grep  -A4 "Root"|grep ID|cut -d: -f2) > vrkrootc.pem</code>
b) Kansalaisvarmennejuuri
<code>$ pkcs15-tool -r $(pkcs15-tool -c|grep  -A4 "Citizen Qualified"|grep ID|cut -d: -f2) > vrkcqc.pem</code>

Jos taas haet varmenteesi VRK:n sivustolta, käy lataamassa se. Tällöin varmenne kuitenkin on väärässä muodossa – VRK:n sivustolla käytetään DER-muotoa, kun Apache taas haluaa varmenteensa PEM-muodossa. Muunna se siis PEM-muotoon:
<code>$ openssl x509 -in vrkrootc.crt -inform DER -outform PEM -out vrkrootc.pem</code>
(Tai vastaavasti tiedostonimeksi vrkcqc, jos käytät kansalaisvarmennejuurta.)

Sijoita varmenteet tämän jälkeen sopivaan paikkaan palvelimellasi. /etc/ssl toimii hienosti.

Tämän jälkeen lisää vielä (Debianissa hakemistosta /etc/apache2/sites-enabled löytyvään) SSL-vhost-tiedostoosi muutama rivi:
<code>SSLCACertificateFile /etc/ssl/vrkrootc.crt
SSLVerifyClient optional
SSLVerifyDepth 2</code>
SSLVerifyDepth-arvon tulee olla 2, jos käytät yleistä juurivarmennetta – tällöin juuren ja varmenteen välissä on nimittäin tuo yllä mainittu kansalaisvarmennejuuri, jolloin käyttäjän varmenteen ”syvyys” antamastasi juuresta on kaksi varmennetta. Jos käytät suoraan kansalaisjuurivarmennetta, syvyydeksi pitäisi riittää 1, koska tällöin käyttäjän varmenne on suoraan antamassasi juuressa.

Näillä eväillä pitäisi Drupalin päähän saada ympäristömuuttujassa $_SERVER tieto käyttäjän mahdollisesta VRK:n myöntämästä henkilövarmenteesta. Koska varmenne on määritelty valinnaiseksi, pääsevät myös varmenteettomat sivustolle vanhaan malliin. 

<h2>Drupal-modulin käyttöönotto</h2>

Kun itse Apachen pää on saatu kuntoon, täytyy vielä saada Drupal ymmärtämään jotain Apachen antamasta tunnistustiedosta. Tähän liittyen täytyykin asentaa <a href="http://drupal.org/project/certificatelogin">Certificate Login</a> -moduli. 

Kun olet asentanut modulin ja käynyt laittamassa sen päälle, vieraile modulin asetussivulla (Ylläpito => Sivuston asetukset => Certificate Login Settings), ja laita ainakin seuraavanlaisia asetuksia:

* Enable/Disable: Enabled
* PHP code to retrieve user name: ”$_SERVER['SSL_CLIENT_S_DN_CN']” (ilman uloimpia lainausmerkkejä)
* Account creation: Enabled

Näillä asetuksilla saat käyttäjätunnuksiksi koko nimen + SATU:n (Sähköinen asiointitunnus.) Ei ihan optimaalista, muita vaihtoehtoja on mikä tahansa yhdistelmä etunimestä, sukunimestä ja SATU:sta. Omana tavoitteenani on laajentaa Certificate Login -modulia siten, että se osaisi käyttää tunnistamiseen tiettyä kenttää ja tallentaa sen käyttäjäprofiiliin, jotta käyttäjän käyttäjätunnus voisi olla jotain mitä sertifikaatista ei löydy. Myös porttaus Drupal 7:aan olisi kiva... Katsotaan mitä tulevina viikkoina saan aikaan. Siihen asti edellämainittu on nähdäkseni pitkälti se, mitä näillä nappuloilla saadaan aikaan. 'njoy.

<h2>Ongelmanratkaisu</h2>

Eikö toimi? Käy asettamassa Apacheen enemmän kertovat logit laittamalla SSL-vhostin asetuksissa oleva LogLevel-asetus esimerkiksi arvoon debug. Alla muutamia löytämiäni ongelmia:
<dl>
<dt>[error] [client 192.0.2.0] Certificate Verification: Certificate Chain too long (chain has 2 certificates, but maximum allowed are only 1)</dt>
<dd>Säädä SSLVerifyDepth-arvoa siten, että se on vähintään ”chain has n certificates”-kohdan n-arvon mukainen.</dd>
<dt>[info] SSL Library Error:  error::SSL routines:SSL3_GET_CLIENT_CERTIFICATE:peer did not return a certificate No CAs known to server for verification?</dt>
<dd>Asiakkaalta ei tullut varmennetta. Tarkista Apachen restartin jälkeen error_logista, että se on löytänyt CA-tiedot:
<code>[debug] ssl_engine_init.c(598): Configuring client authentication
[debug] ssl_engine_init.c(1193): CA certificate: /C=FI/ST=Finland/O=Vaestorekisterikeskus CA/OU=Valtion kansalaisvarmenteet/CN=VRK Gov. CA for Citizen Qualified Certificates</code>
Kunhan tämä on ok, niin ainakin itselläni tähän auttoi ihan selaimen uudelleenkäynnistys. </dd>

<h2>Lisälukemista</h2>

<ul>
<li><a href="http://linux.fi/wiki/HST">Linux.fi-wikin sivu HST:stä</a></li>
<li><a href="http://linux.fi/wiki/Apache_httpd#S.C3.A4hk.C3.B6isen_henkil.C3.B6kortin_tuki">Linux.fi-wikin sivu HST-kortin asentamisesta Apacheen</a></li>
<li><a href="http://www.helsinki.fi/~aulaskar/tietos/korttitunnistus/kortti.html">Ismo Aulaskarin jo muutaman vuoden vanha ohje kortin käyttämisestä Linux-ympäristössä</a></li>
</ul>
