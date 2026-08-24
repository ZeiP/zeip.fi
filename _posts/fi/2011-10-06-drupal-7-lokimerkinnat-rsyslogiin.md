---
layout: "post"
title: "Drupal 7 -lokimerkinnät rsyslogiin"
lang: "fi"
date: "2011-10-06T15:36:16+00:00"
permalink: "/fi/blogi/2011-10-06_drupal-7-lokimerkinnat-rsyslogiin/"
theme: "technology"
tags:
  - "Drupal"
  - "Drupal 7"
  - "syslog"
  - "rsyslog"
translation_key: "d7-8"
original_urls:
  - "/artikkeli/drupal-7-lokimerkinnät-rsyslogiin"
  - "/node/9"
  - "/fi/node/9"
source: "d7"
render_with_liquid: false
---

Tavallinen tapa Drupal 7:n lokitukseen on kaikkien lokimerkintöjen tallentaminen tietokantaan. Tällä on etunsa ja haittansa: Toisaalta se toimii hienosti minkä tahansa Drupal-sivuston kanssa vaatimatta ylimääräisiä ohjelmistoja tai pääsyä palvelimelle. Toisaalta se aiheuttaa muutama ylimääräisen tietokantakyselyn silloin tällöin (mikä itsessään ei toki ole kamalaa, mutta kun Drupal jo valmiiksi tekee niitä ”muutaman”, voi olla fiksua yrittää karsia kaikki ylimääräiset pois...) Ja luonnollisesti lokeja pitäisi myös seurata ja tarpeen tullen toimia merkintöjen pohjalta. Tämä voi osoittautua haasteeksi jos yrität ylläpitää kymmeniä sivustoja käsittävää multisite-asennusta – sinulla todennäköisesti ei ole aikaa tarkistaa jokaisen sivuston lokeja päivittäin Web-käyttöliittymän kautta.

Viimeisen pointin hyväksi voisi toki tehdä jotain vaikka kirjoittelemalla näppärän pikku skriptin joka hakee kaikkien sivustojen tietokannoista lokimerkinnät ja näyttää ne yhdessä käyttöliittymässä. En ole itse törmännyt valmiiseen toteutukseen tästä, joten voi olla että joudut kodastelemaan sen itse. Ja riippuen toteutuksesta voi olla että tällaiseen skriptiin pitäisi lisätä jokaisen uuden sivuston kantatunnukset erikseen – minkä todennäköisesti kuitenkin unohdat.

<h2>Ok, ok, oliko sinulla joku pointtikin?</h2>

Lokituksen voi tehdä paremminkin – sivuston toimintojen lokittamisen ilman (pientä) overheadia ja seurannan vaikeuksia. Tämä on mahdollista syslogin avulla (tämä toki yleensä vaatii että hallitset itse omaa palvelintasi – muuten et todennäköisesti saa tätä asennettua.)

Syslogd on palvelinohjelmisto, joka on vastuussa Linux-järjestelmäsi kaikista lokitustarpeista. Se kirjoittaa jotain lokiin todennäköisesti joka minuutti: Saapuvat ja lähtevät sähköpostit, shell-yhteysyritykset, cron-ajot... Mitä ikinä kaipaatkin, syslogilla todennäköisesti on se. Se on pitkälle erikoistunut työkalu joka tekee yhden ja vain yhden asian: Lokittaa mitä ikinä järjestelmäsi vaan haluaa.

Tämän takia on tietysti järkevää käyttää syslogia myös Drupal-asennustesi ongelmien ja virheiden lokittamiseen. Vähemmän yllättäen, tälle(kin) on jo Drupal-moduli: Drupalin ytimestä löytyy Syslog-moduli.

<h2>Miten se sitten tehdään?</h2>

Syslog-moduli on melko helppo käyttää: Oikeasti sinun vaan tarvitsee ottaa se käyttöön ja tehdä sen asetukset osoitteessa admin/config/development/logging. Täytä seuraavat kentät ja klikkaa Tallenna, ja olet jo melkein valmis:

<dl>
<dt>Syslog identiteetti</dt>
<dd>Tämän pitäisi olla merkkijono jota käytät tämän Drupal-asennuksen erottamiseen kaikista muista palvelimesi Drupal-asennuksista. Itse käytän yleensä sivuston domain-nimeä ilman pistettä, eli www.zeip.eu:sta tulee zeipeu.</dd>
<dt>Syslog facility</dl>
<dd>Tämä on tavallaan ”kanava” jota syslogd käyttää jakamaan eri ohjelmistojen merkinnät eri lokitiedostoihin omien sääntöjensä mukaisesti. Drupal antaa sinun käyttää vain LOCAL-vaihtoehtoja – itse käytän LOG_LOCAL1:tä. LOG_LOCAL7 on joissain järjestelmissä varattu, joten en suosittele sen käyttämistä.</dd>
</dl>

Kun olet tehnyt tämän, Drupalisi lokittaa jo virheensä syslogiin. Mutta syslogd ei välttämättä vielä tallenna niitä: Sille ei ole kerrottu, mitä valitsemallasi facilityn virheillä pitäisi tehdä. Joten seuraavaksi sinun tulee tehdä syslogdisi asetukset. Jos käytät Debiania, käytät todennäköisesti rsyslogia syslogdinasi, joten se on se järjestelmä jonka asetukset näytän tässä. Jos käytät jotain muuta, haluat todennäköisesti tehdä vastaavat asetukset, mutta muotoilun joudut selvittämään itse.

Debianissa, luo uusi tiedosto nimellä /etc/rsyslog.d/drupal.conf seuraavan sisältöisenä:

<code>$template RFC3164fmt,"<%PRI%>1 %TIMESTAMP:::date-rfc3339% %HOSTNAME% %syslogtag%- - - %msg%\n"
local1.*                                -/var/log/drupal.log;RFC3164fmt</code>

Ensimmäinen rivi määrittelee uuden mallin lokimuotoiluksi, ja toinen rivi määrittelee että kaikki viestit local1-facilityssä tallennetaan /var/log/drupal.logiin. Jos valitsin jonkun muun kuin LOG_LOCAL1:n, korjaa toista riviä vastaavasti.

Voit nyt kirjautua sisään sivustollesi ja sen jälkeen tarkistaa, että kirjautumisesi on tallennettu tiedostoon /var/log/drupal.log. Tämän jälkeen voit poistaa Database logging -modulin pois käytöstä säästääksesi muutaman tietokantakyselyn. Se on siinä!
