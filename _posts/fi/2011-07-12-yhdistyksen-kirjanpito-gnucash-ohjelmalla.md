---
layout: "post"
title: "Yhdistyksen kirjanpito Gnucash-ohjelmalla"
lang: "fi"
date: "2011-07-12T23:15:33+00:00"
permalink: "/fi/blogi/2011-07-12_yhdistyksen-kirjanpito-gnucash-ohjelmalla/"
theme: "finance"
tags:
  - "gnucash"
  - "kirjanpito"
translation_key: "d7-5"
original_urls:
  - "/artikkeli/yhdistyksen-kirjanpito-gnucash-ohjelmalla"
  - "/node/5"
  - "/fi/node/5"
source: "d7"
render_with_liquid: false
---

Aloitin vuoden 2010 alusta ainejärjestöni rahastonhoitajana &ndash; iso haaste, kun ei tiedä yhtään mitään kirjanpidosta. Vuoden aikana selvisi kaikenlaista, mutta heti kärkeen päätin, että en halua käyttää yleisesti Suomessa käytettyä (sinänsä varsin käyttökelpoisen oloista) Tappio-ohjelmaa, vaan haluan kokeilla, miten avoimen lähdekoodin voimat yltävät suomalaisen yhdistyksen kirjanpitoon. 

Tähän löytyy nykyisellään useampikin vaihtoehto. Saattaa olla että löytyi silloinkin, mutta syystä tahi toisesta (osittain ehkä siksi, että se vaikutti kaikkein aktiivisimmin kehitetyltä ja taisi jo silloin tukea ainakin joitain tietokantoja, nykyisellään myös MySQL:ää) valitsin <a href="http://www.gnucash.org/">Gnucashin</a>. Gnucash kuitenkin on jopa suomenkielisenä versiona pitkälti englanninkielinen (eli sen käännös on puutteellinen), ja muutenkin se on selvästi tarkoitettu käytettäväksi tietyllä tavalla. <a href="http://www.asteriski.fi/">Asteriskin</a> tilikartan muoto ei ole ihan se GnuCashin omin &ndash; esimerkiksi uudenkin version tuloslaskelma-raportti tulostaa käyttökelvottoman tuloslaskelman, jos kulutilit ja tulotilit eivät olekaan täysin erillään, vaan ovat kukin oman kategoriansa alla. 

Koko vuoden jännitin, saanko tilinpäätöksen tehtyä ohjelmalla, vai joudunko näpyttelemään kaiken tiedon uudestaan Tappioon häntä koipien välissä. Totta kai tein testejä jo tilikauden aikana, mutta olin myös kuullut huhuja siitä, kuinka joku oli aiemmin kokeillut Gnucashia samaisen yhdistyksen kirjanpidossa ja joutunut sinä kuuluisana viimeisenä yönä vaihtamaan ohjelmaa. Ei kaikkein kannustavin vinkki kuulla puolessavälissä tilikautta...

Lopunperin onnistuin kuitenkin saamaan omaan silmääni ihan käyttökelpoiset tulosteet Gnucashista. Tähän koitan koota pari vinkkiä siitä, miten tulosteista saa totutun näköisiä &ndash; en varsinaisesti lupaa että ne ovat tietosisällöiltään, ulkonäöltään tai miltään muultakaan oikeita, mutta yhdestä (maallikko)tilintarkastuksesta näillä on jo menty läpi. Jos löydät parempia tapoja tai toteat että tuloste ei ole lain tai hyvän tavan mukainen, kuulen siitä mielelläni.

<h2>Tase</h2>
<ol>
<li>Avaa Raportit-valikosta Vastaavat ja vastattavat -alakohdasta Tase-raportti</li>
<li>Klikkaa työkalupalkista Ominaisuudet</li>
<li>Aseta Tilit-välilehdeltä näytettävien alitilitasojen määräksi "Kaikki"</li>
<li>Aseta Näytä-välilehdeltä seuraavat:
<ul>
<li>Ylätilin tase: Älä näytä</li>
<li>Ylätilien välisummat: Näytä välisummat</li></ul></li>
<li>Käy vielä asettamassa Yleistä-välilehdeltä raportin nimeksi ja otsikoksi "Tase" ja yrityksen nimeksi yhdistyksesi nimi. Tyylitiedosto Helppo tekee taseesta helppolukuisemman &ndash; ainakin näytöltä.</li>
<li>Klikkaa lopuksi Ok ja tarkista tulos. Raportin päivämääränä ylälaidassa pitäisi olla tilikautesi viimeinen päivä (31.12.[vuosi]). Jos ei ole, käy säätämässä tilikausiasetusta muokkaa-valikosta, asetukset-kohdan takaa avautuvan ikkunan Accounting Period -välilehdeltä.</li>
</ol>

<h2>Tuloslaskelma</h2>
<p>Tämä löytyy myös valikosta suoraan, mutta ainakaan omalla tilikartallani se ei toiminut. Kokeile kuitenkin, se löytyy raportit => tulot ja menot => tuloslaskelma -kohdasta valikosta.</p>
<ol>
<li>Avaa Raportit-valikosta Yhteenveto tileistä</li>
<li>Klikkaa työkalupalkista Ominaisuudet</li>
<li>Siirry Tilit-välilehdelle ja valitse taas näytettävien alitilitasojen määräksi "kaikki"</li>
<li>Tilit-kohdasta valitse ensin Tyhjennä valinnat. Klikkaa sitten Tulos-ylätiliäsi (joka ainakin itselläni sisältää siis kaikki tulostilit) ja sen jälkeen listan alla olevaa painiketta Select Children.</li>
<li>Aseta taas Näytä-välilehdeltä seuraavat:
<ul>
<li>Ylätilin tase: Älä näytä</li>
<li>Ylätilien välisummat: Näytä välisummat</li></ul></li>
<li>Käy vielä asettamassa Yleistä-välilehdeltä raportin nimeksi ja otsikoksi "Tuloslaskelma" ja yrityksen nimeksi yhdistyksesi nimi. Tyylitiedosto Helppo tekee taseesta helppolukuisemman &ndash; ainakin näytöltä.</li>
<li>Klikkaa lopuksi Ok ja tarkista tulos. Raportin päivämääränä ylälaidassa pitäisi olla tilikautesi viimeinen päivä (31.12.[vuosi]). Jos ei ole, käy säätämässä tilikausiasetusta muokkaa-valikosta, asetukset-kohdan takaa avautuvan ikkunan Accounting Period -välilehdeltä.</li>
</ol>

<h2>Pääkirja</h2>
<ol>
<li>Avaa Raportit-valikosta Vastaavat ja vastattavat -kohdasta Pääkirja-raportti.</li>
<li>Klikkaa työkalupalkista Ominaisuudet</li>
<li>Siirry Tilit-välilehdelle ja valitse taas näytettävien alitilitasojen määräksi "kaikki"</li>
<li>Tilit-kohdasta valitse ensin Tyhjennä valinnat. Klikkaa sitten jokaista ylätiliäsi vuorollaan ja avaa ne käyttämällä Select Children -painiketta.</li>
<li>Kun kaikki tilit ovat näkyvissä, klikkaa "Valitse kaikki"</li>
<li>Klikkaa Suodata-kohdan alla olevaa Tyhjennä valinnat -painiketta</li>
<li>Poista Näytä-välilehdeltä Juokseva tase -valinta</li>
<li>Käy asettamassa Yleistä-välilehdeltä raportin nimeksi "Pääkirja". Tyylitiedosto Helppo tekee taseesta helppolukuisemman &ndash; ainakin näytöltä.</li>
</ol>

<h2>Päiväkirja</h2>
<ol>
<li>Avaa Raportit-valikosta Vastaavat ja vastattavat -kohdasta Päiväkirja-raportti.</li>
<li>Klikkaa työkalupalkista Ominaisuudet</li>
<li>Valitse Näytä-välilehdeltä Num-kenttä, jolloin myös tositenumero näkyy päiväkirjassa.</li>
<li>Käy asettamassa Yleistä-välilehdeltä raportin nimeksi "Päiväkirja". Tyylitiedosto Helppo tekee taseesta helppolukuisemman &ndash; ainakin näytöltä.</li>
</ol>

Siinä se. Asetukset varmaan voisi laittaa fiksumminkin, enkä voi väittää tuntevani liian tarkasti yhdistysten tilinpäätösten asiakirjojen muodosta olevia määräyksiä, mutta näillä asetuksilla pääset melko lähelle Tappio-ohjelman muotoa. Have fun!
