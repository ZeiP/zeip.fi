---
layout: "post"
title: "Hyvän SMS-gatewayn valitseminen käyttöön Suomessa"
lang: "fi"
date: "2012-02-06T22:15:59+00:00"
permalink: "/fi/blogi/2012-02-06_hyvan-sms-gatewayn-valitseminen-kayttoon-suomessa/"
theme: "technology"
tags:
  - "SMS"
translation_key: "d7-18"
original_urls:
  - "/artikkeli/hyvän-sms-gatewayn-valitseminen-käyttöön-suomessa"
  - "/node/19"
  - "/fi/node/19"
source: "d7"
render_with_liquid: false
---

<p>Tajusin tänään, että tarvitsen tekstiviestihälytykset rakkaaseen Zabbixiini, joka yrittää kovasti pysyä kärryillä ylläpitämieni palvelimien tilasta. Sähköposti-ilmoituksia ongelmista ei vaan aina huomaa tarpeeksi ajoissa. Mutta kun hakee SMS gatewayta hakukoneella, saa mallia miljoona tulosta – mitä niistä kannattaisi oikeasti käyttää?</p>
<p>Kokeilin niistä muutamia, yrittäen löytää palvelun joka olisi edullinen, joustava, nopea ja luotettava. Jep, tiedän – ei pitäisi kuvitellakaan löytävänsä tuollaista all in one -pakettia. Siitä huolimatta näyttäisi siltä että löysin sellaisen, joka täyttää kaikki kohdista vähintään riittävällä tarkkuudella.</p>
<p>Tässä muutamia kokemuksia niistä mistä jotain muistan.</p>
<dl>
<dt><a href="http://budgetsms.net/">BudgetSMS</a></dt>
<dd>Alkuni BudgetSMS:n kanssa oli kivikkoinen – yritin käyttää heidän API:aan, mutta en saanut tekstiviestiä OK-kuittauksesta huolimatta. Itse asiassa luovutin koko palvelun kanssa, mutta pari tuntia myöhemmin siivotessani roskapostikansioitani löysin sähköpostin BudgetSMS:ltä, jossa kyseltiin lisätietoja käyttötarkoituksestani. Ilmeisesti BudgetSMS:n palveluita ei ollut suuremmin käytetty Suomeen lähettämiseen; tukikaveri lähetti minulle muutamia testiviestejä eri reittejä pitkin testatakseen mikä niistä toimii parhaiten.</dd>
<dd>Sain palvelun toimimaan hyvin, ja he suostuivat ottamaan pienemmän kertamaksun kuin mitä sivuilla luki. Pidin heidän henkilökohtaisesta palvelustaan ja päätin valita heidän palvelunsa. </dd>
<dt><a href="http://www.clickatell.com/">Clickatell</a></dt>
<dd>Clickatell oli ensimmäinen kokeilemani. Se näytti melko suurelta ja ammattimaiselta, ja API-vaihtoehtoja oli järjetön määrä. Huonoin asia Clickatellissä oli se, että sitä ei voi testata kunnolla ostamatta minimimäärää viestejä (joka oli itselleni 400). Testikrediteillä pystyi lähettämään kyllä viestejä, mutta viestin sisältö oli Clickatellin oma testiviesti eikä asiakkaan määrittämä.</dd>
<dt><a href="http://www.nexmo.com/">Nexmo</a></dt>
<dd>Nexmo oli toinen valintani; käytän sitä omaan käyttööni koska BudgetSMS on jonkin verran kalliimpi ALV:in takia. Rekisteröintiprosessi ja käyttöliittymä ylipäätäänkin ovat hyviä ja hinnat ovat melko halpoja. Nexmolla on myös löytämistäni palveluista pienin minimikertamaksu; tosin BudgetSMS:n kanssa sai saman kertamaksun pyydettäessä. </dd>
<dt>Ne muut</dt>
<dd>Kokeilin muutamia muitakin, ja surffasin ainakin tusinan muiden Web-sivustoja yrittäen löytää järkevää palvelua. Turhan monet eivät toimineet Suomeen lupauksistaan huolimatta, ja jotkut olivat käyttööni naurettavan kalliita. Käytännössä itse olen tyytyväinen valintoihin ja uskon löytäneeni ainakin keskitasoa paremmat palvelut.</dd>
</dl>
<p>P.S. Tein myös uuden version skriptistä, jolla SMS:t voi Zabbixista lähettää – se löytyy tällä hetkellä vain <a href="https://support.zabbix.com/browse/ZBX-4617">Zabbixin JIRA:sta</a>, mutta toivon että se ilmestyy myös Zabbixin dokumentaatioon vanhan version tilalle.</p>
