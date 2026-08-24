#!/usr/bin/env python3
import csv
import datetime as dt
import html
import os
import re
import shutil
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "extracted_db_dump" / "csv"
BASE_URL = "https://www.zeip.fi"
ARCHIVE_FILE_BASE_URLS = [
    "https://www.zeip.eu/sites/zeip.eu/files",
    "https://www.zeip.eu/sites/default/files",
    "https://zeip.eu/sites/zeip.eu/files",
    "https://zeip.eu/sites/default/files",
]
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
LOCAL_HERO_IMAGE = "/assets/images/jyri-petteri-paloposki.jpg"
IMPORTED_IMAGE_PATH = "/assets/images/imported"


CURRENT_PAGES = [
    ("fi", "/fi", "home", "/fi/", "home-fi"),
    ("en", "/en", "home", "/en/", "home-en"),
    ("fi", "/fi/kuka", "page", "/fi/kuka/", "who"),
    ("en", "/en/who", "page", "/en/who/", "who"),
    ("fi", "/fi/kuntateemat", "page", "/fi/kuntateemat/", "municipal"),
    ("en", "/en/municipal-issues", "page", "/en/municipal-issues/", "municipal"),
    ("fi", "/fi/alueteemat", "page", "/fi/alueteemat/", "county"),
    ("en", "/en/county-issues", "page", "/en/county-issues/", "county"),
    ("fi", "/fi/suosituksia", "page", "/fi/suosituksia/", "recommendations"),
    ("fi", "/fi/yhteys", "page", "/fi/yhteys/", "contact"),
    ("en", "/en/form/contact", "page", "/en/form/contact/", "contact"),
    ("fi", "/fi/tule-mukaan", "page", "/fi/tule-mukaan/", "join"),
    ("en", "/en/tule-mukaan", "page", "/en/tule-mukaan/", "join"),
    ("fi", "/fi/evasteet", "page", "/fi/evasteet/", "cookies"),
]

HOME_OVERRIDES = {
    "fi": {
        "title": "Jyri-Petteri Paloposki",
        "description": (
            "Olen turkulainen IT-yrittäjä, järjestöaktiivi ja yhteiskunnallisista asioista "
            "kiinnostunut tekijä. Työssäni rakennan ja ylläpidän verkkopalveluja, "
            "vapaaehtoistöissä ja luottamustehtävissä taas yritän saada yhteisiä rakenteita "
            "toimimaan vähän paremmin."
        ),
        "facts": [
            {"label": "Teknologia", "text": "Verkkopalveluja, avointa lähdekoodia ja toimivia järjestelmiä"},
            {"label": "Järjestötoiminta", "text": "Partiota, opiskelijajärjestöjä ja vihreää vapaaehtoistyötä"},
            {"label": "Yhteiskunta", "text": "Päätöksentekoa, avoimuutta ja arjen kannalta järkeviä rakenteita"},
        ],
        "body": """<p>Olen asunut Turussa vuodesta 2009. Taustani on teknologian, järjestötoiminnan ja avoimen lähdekoodin parissa, ja kirjoitan täällä erityisesti teknologiasta, taloudesta, avoimuudesta, kaupungeista, vapaaehtoistoiminnasta ja satunnaisista vastaan tulevista kiinnostavista asioista.</p>
<p>Sivusto kokoaa yhteen esittelyni, yhteystietoni, pidemmät kirjoitukseni sekä ajatuksia teemoista, joiden parissa olen tehnyt töitä tai joita pidän muuten tärkeinä.</p>
<h2>Teemoja, joihin palaan usein</h2>
<h3>Teknologia ja avoimuus</h3>
<p>Toimivia verkkopalveluja, avointa dataa ja järjestelmiä, jotka helpottavat ihmisten arkea.</p>
<h3>Kaupunki ja yhteiskunta</h3>
<p>Turkua, päätöksentekoa, luottamusta, taloutta ja sitä, miten yhteiset asiat saadaan hoidettua järkevästi.</p>
<h3>Järjestöt ja vapaaehtoistyö</h3>
<p>Partiota, opiskelijajärjestöjä, vihreää järjestötoimintaa ja muita paikkoja, joissa ihmiset tekevät asioita yhdessä.</p>""",
    },
    "en": {
        "title": "Jyri-Petteri Paloposki",
        "description": (
            "I’m an IT entrepreneur, civic-minded organiser and long-time volunteer from "
            "Turku. I work with web services and open source, and spend a fair amount of "
            "my free time trying to make shared organisations and public decision-making "
            "work a little better."
        ),
        "facts": [
            {"label": "Technology", "text": "Web services, open source and systems that work in practice"},
            {"label": "Organisations", "text": "Scouting, student organisations and Green civic activity"},
            {"label": "Society", "text": "Decision-making, openness and structures that make everyday life easier"},
        ],
        "body": """<p>I have lived in Turku since 2009. My background combines technology, volunteer work, open source, student organisations, scouting and Green civic activity. This site collects my profile, contact details and writings on technology, economy, openness, cities and whatever else happens to catch my attention.</p>
<h2>Themes I keep returning to</h2>
<h3>Technology and openness</h3>
<p>Web services, open data, open source and systems that should make everyday life easier.</p>
<h3>Cities and society</h3>
<p>Turku, public decision-making, trust, economy and the practical details of shared life.</p>
<h3>Organisations and volunteering</h3>
<p>Scouting, student organisations, Green civic work and the structures that help people do things together.</p>""",
    },
}


THEME_RULES = {
    "politics": [
        "kampanja", "campaign", "kuntavaalit", "hyvinvointialue", "turku",
        "avoin hallinto", "governance", "kuntayhtiot", "tiedepuolue", "politi",
    ],
    "technology": [
        "drupal", "apache", "syslog", "rsyslog", "powerdns", "dns", "server",
        "security", "php", "modsecurity", "nginx", "jolla", "sms", "varmenteet",
        "autentikaatio", "vrk", "teknologia", "avoin data", "avoin lähdekoodi",
        "open data", "open source",
    ],
    "testing": ["testing", "testaus", "cucumber", "watir", "dojo"],
    "travel": ["irlanti", "dublin", "haltin", "matk", "travel"],
    "finance": ["talous", "finance", "gnucash", "kirjanpito", "opintolaina", "hankinnat", "laina", "euribor"],
}


class DrupalPageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.title = ""
        self.description = ""
        self.published = ""
        self.modified = ""
        self.alternates = []
        self.images = []
        self._in_title = False
        self._h1_depth = None
        self._h1_parts = []
        self._body_depth = None
        self._body_parts = []
        self._body_seen = False
        self._tag_depth = None
        self._tag_href = None
        self._tag_parts = []
        self.tags = []
        self._depth = 0
        self._article_depth = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = set(attrs_dict.get("class", "").split())
        if tag == "meta":
            prop = attrs_dict.get("property") or attrs_dict.get("name")
            if prop == "description":
                self.description = html.unescape(attrs_dict.get("content", ""))
            elif prop == "article:published_time":
                self.published = attrs_dict.get("content", "")
            elif prop in ("article:modified_time", "og:updated_time"):
                self.modified = attrs_dict.get("content", "")
            elif prop == "og:image":
                self.images.append(attrs_dict.get("content", ""))
        if tag == "link":
            rel = attrs_dict.get("rel", "")
            if "alternate" in rel and attrs_dict.get("hreflang") and attrs_dict.get("href"):
                self.alternates.append((attrs_dict["hreflang"], attrs_dict["href"]))
            if rel == "image_src" and attrs_dict.get("href"):
                self.images.append(attrs_dict["href"])
        if tag == "title":
            self._in_title = True
        if tag == "h1" and "page-title" in classes:
            self._h1_depth = self._depth
        if tag == "article" and "node" in classes and self._article_depth is None:
            self._article_depth = self._depth
        if (
            self._article_depth is not None
            and tag == "div"
            and "field--name-body" in classes
            and self._body_depth is None
            and not self._body_seen
        ):
            self._body_depth = self._depth
            self._body_seen = True
        elif self._body_depth is not None:
            self._body_parts.append(self._format_start(tag, attrs))
        if tag == "a" and self._tag_depth is None and "field--tags__item" not in classes:
            href = attrs_dict.get("href", "")
            if "/asiasana/" in href or "/tags/" in href:
                self._tag_depth = self._depth
                self._tag_href = href
                self._tag_parts = []
        if tag not in VOID_TAGS:
            self._depth += 1

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        self._depth -= 1
        if tag == "title":
            self._in_title = False
        if self._h1_depth is not None and self._depth == self._h1_depth:
            self.title = html.unescape("".join(self._h1_parts)).strip()
            self._h1_depth = None
        if self._body_depth is not None:
            if self._depth == self._body_depth:
                self._body_depth = None
            else:
                self._body_parts.append(f"</{tag}>")
        if self._tag_depth is not None and self._depth == self._tag_depth:
            text = html.unescape("".join(self._tag_parts)).strip()
            if text:
                self.tags.append(text)
            self._tag_depth = None
            self._tag_href = None
        if self._article_depth is not None and self._depth == self._article_depth:
            self._article_depth = None

    def handle_data(self, data):
        if self._in_title and not self.title:
            self.title = html.unescape(data.split("|")[0]).strip()
        if self._h1_depth is not None:
            self._h1_parts.append(data)
        if self._body_depth is not None:
            self._body_parts.append(html.escape(data, quote=False))
        if self._tag_depth is not None:
            self._tag_parts.append(data)

    def handle_entityref(self, name):
        text = f"&{name};"
        if self._body_depth is not None:
            self._body_parts.append(text)
        if self._h1_depth is not None:
            self._h1_parts.append(html.unescape(text))
        if self._tag_depth is not None:
            self._tag_parts.append(html.unescape(text))

    def handle_charref(self, name):
        text = f"&#{name};"
        if self._body_depth is not None:
            self._body_parts.append(text)
        if self._h1_depth is not None:
            self._h1_parts.append(html.unescape(text))
        if self._tag_depth is not None:
            self._tag_parts.append(html.unescape(text))

    def _format_start(self, tag, attrs):
        rendered = []
        for key, value in attrs:
            if value is None:
                rendered.append(key)
            else:
                rendered.append(f'{key}="{html.escape(value, quote=True)}"')
        suffix = " " + " ".join(rendered) if rendered else ""
        return f"<{tag}{suffix}>"

    @property
    def body(self):
        return "".join(self._body_parts).strip()


def fetch(path_or_url):
    url = path_or_url if path_or_url.startswith("http") else BASE_URL + path_or_url
    req = urllib.request.Request(url, headers={"User-Agent": "zeip-static-import/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def clean_generated():
    for path in [ROOT / "_posts", ROOT / "redirects", ROOT / "fi", ROOT / "en"]:
        if path.exists():
            shutil.rmtree(path)
    for path in [ROOT / "_posts" / "fi", ROOT / "_posts" / "en", ROOT / "redirects", ROOT / "fi", ROOT / "en"]:
        path.mkdir(parents=True, exist_ok=True)


def yaml_scalar(value):
    value = "" if value is None else str(value)
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def front_matter(data):
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append("  -")
                    for item_key, item_value in item.items():
                        lines.append(f"    {item_key}: {yaml_scalar(item_value)}")
                else:
                    lines.append(f"  - {yaml_scalar(item)}")
        elif value is None:
            lines.append(f"{key}:")
        else:
            lines.append(f"{key}: {yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def slugify(value):
    value = html.unescape(value).lower()
    translit = {
        "ä": "a", "ö": "o", "å": "a", "ü": "u", "é": "e", "è": "e",
        "á": "a", "í": "i", "ó": "o", "–": "-", "—": "-", "”": "", "“": "",
    }
    for src, dst in translit.items():
        value = value.replace(src, dst)
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "post"


def normalize_internal_links(fragment):
    fragment = rewrite_imported_file_urls(fragment)

    def repl(match):
        quote, url = match.groups()
        url = html.unescape(url)
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc and parsed.netloc not in ("www.zeip.fi", "zeip.fi"):
            return match.group(0)
        path = parsed.path or url
        query = ("?" + parsed.query) if parsed.query else ""
        fragment_part = ("#" + parsed.fragment) if parsed.fragment else ""
        if path.startswith("/fi/blogi/") or path.startswith("/en/blogi/"):
            new_path = path.rstrip("/") + "/"
        elif path == "/node/2":
            new_path = "/fi/kuka/"
        elif path == "/yhteys":
            new_path = "/fi/yhteys/"
        else:
            new_path = path
        return f'href={quote}{new_path}{query}{fragment_part}{quote}'

    fragment = re.sub(r'href=(["\'])(.*?)\1', repl, fragment)
    fragment = re.sub(r'(src|href)=(["\'])(/core/.*?)\2', rf'\1=\2{BASE_URL}\3\2', fragment)
    fragment = re.sub(r'srcset=(["\'])(.*?)\1', lambda m: f'srcset={m.group(1)}{rewrite_srcset(m.group(2))}{m.group(1)}', fragment)
    fragment = convert_image_paragraphs_to_markdown(fragment)
    return fragment


def imported_image_url(public_path):
    parsed = urllib.parse.urlparse(html.unescape(public_path))
    path = parsed.path
    for prefix in ("/sites/zeip.eu/files/", "/sites/default/files/"):
        if path.startswith(prefix):
            rel = path.removeprefix(prefix)
            quoted = urllib.parse.quote(rel, safe="/:@")
            return f"{IMPORTED_IMAGE_PATH}/{quoted}"
    return None


def rewrite_imported_file_urls(fragment):
    def replace_url(value):
        return imported_image_url(value) or value

    def replace_attr(match):
        attr, quote, value = match.groups()
        return f"{attr}={quote}{replace_url(value)}{quote}"

    fragment = re.sub(r'(src|href)=(["\'])(.*?)\2', replace_attr, fragment)

    def replace_srcset(match):
        quote, value = match.groups()
        parts = []
        for part in value.split(","):
            item = part.strip()
            if not item:
                continue
            bits = item.split()
            bits[0] = replace_url(bits[0])
            parts.append(" ".join(bits))
        return f"srcset={quote}{', '.join(parts)}{quote}"

    return re.sub(r'srcset=(["\'])(.*?)\1', replace_srcset, fragment)


def rewrite_srcset(value):
    parts = []
    for part in value.split(","):
        item = part.strip()
        if item.startswith("/") and not item.startswith("/assets/"):
            item = BASE_URL + item
        parts.append(item)
    return ", ".join(parts)


def parse_tag_attrs(tag):
    return {
        key.lower(): html.unescape(value)
        for key, _quote, value in re.findall(r'([\w:-]+)\s*=\s*(["\'])(.*?)\2', tag, flags=re.S)
    }


def markdown_escape(value):
    value = re.sub(r"\s+", " ", value or "").strip()
    return value.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def markdown_image_from_tag(tag):
    attrs = parse_tag_attrs(tag)
    src = attrs.get("src")
    if not src:
        return tag
    title = re.sub(r"\s+", " ", attrs.get("title", "")).strip()
    title_part = ""
    if title:
        title_part = ' "' + title.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return f"![{markdown_escape(attrs.get('alt', ''))}]({src}{title_part})"


def convert_image_paragraphs_to_markdown(fragment):
    img_pattern = re.compile(r"<img\b[^>]*>", flags=re.I)

    def replace_paragraph(match):
        inner = match.group(1)
        if not img_pattern.search(inner):
            return match.group(0)

        parts = []
        cursor = 0
        for image in img_pattern.finditer(inner):
            text = inner[cursor:image.start()].strip()
            if text:
                parts.append(f"<p>{text}</p>")
            parts.append(markdown_image_from_tag(image.group(0)))
            cursor = image.end()

        text = inner[cursor:].strip()
        if text:
            parts.append(f"<p>{text}</p>")

        return "\n\n" + "\n\n".join(parts) + "\n\n"

    return re.sub(r"<p>(.*?)</p>", replace_paragraph, fragment, flags=re.S | re.I)


def parse_drupal_page(path):
    parser = DrupalPageParser()
    parser.feed(fetch(path))
    body = normalize_internal_links(parser.body)
    title = parser.title or path.strip("/") or "Home"
    return {
        "title": title,
        "description": parser.description,
        "published": parser.published,
        "modified": parser.modified,
        "alternates": parser.alternates,
        "images": [img for img in parser.images if img],
        "tags": list(dict.fromkeys(parser.tags)),
        "body": body,
    }


def first_paragraph_text(body):
    match = re.search(r"<p[^>]*>(.*?)</p>", body, flags=re.S | re.I)
    if not match:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(match.group(1)))).strip()


def recommendation_markup(body):
    items = []
    pattern = re.compile(r"<blockquote>\s*(.*?)\s*</blockquote>", flags=re.S | re.I)
    paragraphs = re.compile(r"<p[^>]*>(.*?)</p>", flags=re.S | re.I)
    for match in pattern.finditer(body):
        parts = paragraphs.findall(match.group(1))
        if not parts:
            continue
        attribution = parts[-1].strip()
        quote = "".join(f"<p>{part.strip()}</p>" for part in parts[:-1] or parts)
        if parts[:-1]:
            attribution = re.sub(r"^\s*[–—-]\s*", "", html.unescape(attribution))
        items.append(
            '<figure class="recommendation">\n'
            f"  <blockquote>{quote}</blockquote>\n"
            f"  <figcaption>{html.escape(attribution, quote=False)}</figcaption>\n"
            "</figure>"
        )
    return "\n".join(items) if items else body


def write_current_pages(redirects):
    for lang, source_path, layout, permalink, key in CURRENT_PAGES:
        page = parse_drupal_page(source_path)
        home_override = HOME_OVERRIDES.get(lang) if layout == "home" else None
        data = {
            "layout": layout,
            "title": home_override["title"] if home_override else page["title"],
            "lang": lang,
            "permalink": permalink,
            "translation_key": key,
            "description": home_override["description"] if home_override else page["description"] or first_paragraph_text(page["body"]),
            "source": "current",
            "render_with_liquid": False,
        }
        if key == "recommendations":
            data["description"] = None
        if layout == "home":
            data["hero_image"] = LOCAL_HERO_IMAGE if (ROOT / LOCAL_HERO_IMAGE.lstrip("/")).exists() else ""
            data["facts"] = home_override["facts"] if home_override else []
        rel = permalink.strip("/") or "index"
        out = ROOT / rel / "index.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        body = home_override["body"] if home_override else page["body"]
        if key == "recommendations":
            body = recommendation_markup(body)
        out.write_text(front_matter(data) + body + "\n", encoding="utf-8")
        if source_path.rstrip("/") != permalink.rstrip("/"):
            redirects[source_path] = permalink
            redirects[source_path + "/"] = permalink


def current_blog_paths():
    paths = set()
    xml = fetch("/sitemap.xml")
    root = ET.fromstring(xml.encode("utf-8"))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
    for url in root.findall("s:url", ns):
        loc = url.findtext("s:loc", namespaces=ns) or ""
        for candidate in [loc] + [a.attrib.get("href", "") for a in url.findall("x:link", ns)]:
            parsed = urllib.parse.urlparse(candidate)
            path = parsed.path
            path = path.replace("/fi/fi/", "/fi/").replace("/fi/en/", "/en/")
            if "/blogi/" in path and re.search(r"/blogi/\d{4}-\d{2}-\d{2}_", path):
                paths.add(path)
    return sorted(paths)


def parse_date(value, fallback):
    if value:
        try:
            return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass
    return fallback


def infer_theme(title, tags):
    haystack = " ".join([title] + tags).lower()
    for theme, needles in THEME_RULES.items():
        if any(needle in haystack for needle in needles):
            return theme
    return "personal"


def write_current_posts(redirects):
    translation_by_date = {}
    for path in current_blog_paths():
        lang = "en" if path.startswith("/en/") else "fi"
        page = parse_drupal_page(path)
        published = parse_date(page["published"], dt.datetime.now(dt.UTC))
        date_slug = re.search(r"(\d{4}-\d{2}-\d{2})_(.+)$", path.rstrip("/"))
        slug = date_slug.group(2) if date_slug else slugify(page["title"])
        canonical = f"/{lang}/blogi/{published.date().isoformat()}_{slug}/"
        date_key = published.date().isoformat() + "-" + slugify(page["title"]).replace("im-running", "running")
        translation_key = translation_by_date.setdefault(published.date().isoformat(), f"current-{published.date().isoformat()}")
        data = {
            "layout": "post",
            "title": page["title"],
            "lang": lang,
            "date": published.isoformat(),
            "permalink": canonical,
            "theme": infer_theme(page["title"], page["tags"]),
            "tags": page["tags"],
            "translation_key": translation_key,
            "original_urls": [path],
            "source": "current",
            "render_with_liquid": False,
        }
        out = ROOT / "_posts" / lang / f"{published.date().isoformat()}-{slugify(slug)}.md"
        out.write_text(front_matter(data) + page["body"] + "\n", encoding="utf-8")
        redirects[path] = canonical
        redirects[path + "/"] = canonical


def read_csv(name):
    with (CSV_DIR / f"{name}.csv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def ensure_imported_images():
    image_rows = [
        row for row in read_csv("file_managed")
        if row.get("filemime", "").startswith("image/") and row.get("uri", "").startswith("public://")
    ]
    missing = []
    imported_root = ROOT / IMPORTED_IMAGE_PATH.lstrip("/")
    for row in image_rows:
        rel = urllib.parse.unquote(row["uri"].removeprefix("public://")).lstrip("/")
        target = imported_root / rel
        if target.exists() and target.stat().st_size > 0:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        downloaded = False
        quoted_rel = urllib.parse.quote(rel, safe="/:@")
        for base_url in ARCHIVE_FILE_BASE_URLS:
            url = f"{base_url}/{quoted_rel}"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "zeip-static-import/1.0"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    content_type = response.headers.get("Content-Type", "")
                    if response.status != 200 or not content_type.startswith("image/"):
                        continue
                    target.write_bytes(response.read())
                    downloaded = True
                    break
            except Exception:
                continue
        if not downloaded:
            missing.append(row["uri"])
    if missing:
        print("Missing imported images:")
        for uri in missing:
            print(f"  {uri}")
    else:
        print(f"Imported {len(image_rows)} images")


def d7_data():
    nodes = {r["nid"]: r for r in read_csv("node") if r["type"] == "article" and r["status"] == "1"}
    bodies = {r["entity_id"]: r["body_value"] for r in read_csv("field_data_body") if r["entity_id"] in nodes}
    terms = {r["tid"]: r["name"] for r in read_csv("taxonomy_term_data") if r["vid"] == "1"}
    tags = {nid: [] for nid in nodes}
    for row in read_csv("field_data_field_tags"):
        if row["entity_id"] in tags and row["field_tags_tid"] in terms:
            tags[row["entity_id"]].append(terms[row["field_tags_tid"]])
    aliases = {nid: [] for nid in nodes}
    for row in read_csv("url_alias"):
        if row["source"].startswith("node/"):
            nid = row["source"].split("/", 1)[1]
            if nid in aliases:
                aliases[nid].append("/" + row["alias"].strip("/"))
    return nodes, bodies, tags, aliases


def d7_translation_key(node):
    group = node.get("tnid") or node["nid"]
    if group == "0":
        group = node["nid"]
    return f"d7-{group}"


def write_d7_posts(redirects):
    nodes, bodies, tags, aliases = d7_data()
    for nid, node in sorted(nodes.items(), key=lambda item: int(item[1]["created"])):
        lang = node["language"] if node["language"] in ("fi", "en") else "fi"
        created = dt.datetime.fromtimestamp(int(node["created"]), dt.UTC)
        title = node["title"]
        alias = aliases.get(nid, [])
        source_slug = alias[0].split("/")[-1] if alias else slugify(title)
        canonical = f"/{lang}/blogi/{created.date().isoformat()}_{slugify(source_slug)}/"
        original_urls = alias + [f"/node/{nid}", f"/{lang}/node/{nid}"]
        data = {
            "layout": "post",
            "title": title,
            "lang": lang,
            "date": created.isoformat(),
            "permalink": canonical,
            "theme": infer_theme(title, tags.get(nid, [])),
            "tags": tags.get(nid, []),
            "translation_key": d7_translation_key(node),
            "original_urls": original_urls,
            "source": "d7",
            "render_with_liquid": False,
        }
        body = normalize_internal_links(bodies.get(nid, ""))
        out = ROOT / "_posts" / lang / f"{created.date().isoformat()}-{slugify(source_slug)}.md"
        out.write_text(front_matter(data) + body + "\n", encoding="utf-8")
        for url in original_urls:
            redirects[url] = canonical
            redirects[url + "/"] = canonical


def write_blog_indexes():
    for lang in ("fi", "en"):
        title = "Blogi" if lang == "fi" else "Blog"
        desc = ""
        out = ROOT / lang / "blogi" / "index.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(front_matter({
            "layout": "blog_index",
            "title": title,
            "lang": lang,
            "permalink": f"/{lang}/blogi/",
            "translation_key": "blog-index",
            "description": desc,
        }), encoding="utf-8")


def write_theme_pages():
    labels = {
        "technology": {"fi": "Teknologia", "en": "Technology"},
        "politics": {"fi": "Politiikka", "en": "Politics"},
        "travel": {"fi": "Matkailu", "en": "Travel"},
        "finance": {"fi": "Talous", "en": "Finance"},
        "testing": {"fi": "Testaus", "en": "Testing"},
        "personal": {"fi": "Henkilökohtainen", "en": "Personal"},
    }
    for key, lang_labels in labels.items():
        for lang in ("fi", "en"):
            base = "themes" if lang == "en" else "teemat"
            out = ROOT / lang / base / key / "index.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(front_matter({
                "layout": "theme",
                "title": lang_labels[lang],
                "lang": lang,
                "permalink": f"/{lang}/{base}/{key}/",
                "theme_key": key,
                "translation_key": f"theme-{key}",
            }), encoding="utf-8")


def redirect_path(url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path if parsed.scheme else url
    path = path.strip("/")
    if not path:
        path = "root"
    safe = [slugify(part) or "index" for part in path.split("/")]
    return ROOT / "redirects" / Path(*safe) / "index.html"


def write_redirects(redirects):
    extra = {
        "/": "/fi/",
        "/rss.xml": "/fi/rss.xml",
        "/blog.xml": "/fi/rss.xml",
        "/blog": "/fi/blogi/",
        "/blog/": "/fi/blogi/",
        "/fi/blogs": "/fi/blogi/",
        "/en/blogs": "/en/blogi/",
    }
    redirects.update(extra)
    seen = {}
    for source, target in redirects.items():
        if source == target or not source:
            continue
        seen[source] = target
    for source, target in sorted(seen.items()):
        out = redirect_path(source)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(front_matter({"layout": "redirect", "permalink": source, "redirect_to": target}), encoding="utf-8")


def write_static_xml():
    (ROOT / "robots.txt").write_text(
        "---\npermalink: /robots.txt\nlayout: null\n---\nUser-agent: *\nAllow: /\nSitemap: {{ site.url }}/sitemap.xml\n",
        encoding="utf-8",
    )
    (ROOT / "sitemap.xml").write_text(
        textwrap.dedent(
            """\
            ---
            permalink: /sitemap.xml
            layout: null
            ---
            <?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            {% assign all_docs = site.pages | concat: site.posts %}
            {% for doc in all_docs %}
            {% unless doc.url contains '/404.html' or doc.layout == 'redirect' %}
              <url><loc>{{ site.url }}{{ doc.url }}</loc></url>
            {% endunless %}
            {% endfor %}
            </urlset>
            """
        ),
        encoding="utf-8",
    )
    for lang in ("fi", "en"):
        out = ROOT / lang / "rss.xml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            textwrap.dedent(
                f"""\
                ---
                permalink: /{lang}/rss.xml
                layout: null
                ---
                <?xml version="1.0" encoding="UTF-8"?>
                <rss version="2.0"><channel>
                <title>{{{{ site.title | xml_escape }}}}</title>
                <link>{{{{ site.url }}}}/{lang}/blogi/</link>
                <description>{{{{ site.description | xml_escape }}}}</description>
                {{% assign posts = site.posts | where: "lang", "{lang}" %}}
                {{% for post in posts limit: 20 %}}
                <item>
                  <title>{{{{ post.title | xml_escape }}}}</title>
                  <link>{{{{ site.url }}}}{{{{ post.url }}}}</link>
                  <guid>{{{{ site.url }}}}{{{{ post.url }}}}</guid>
                  <pubDate>{{{{ post.date | date_to_rfc822 }}}}</pubDate>
                  <description>{{{{ post.excerpt | strip_html | xml_escape }}}}</description>
                </item>
                {{% endfor %}}
                </channel></rss>
                """
            ),
            encoding="utf-8",
        )


def main():
    clean_generated()
    ensure_imported_images()
    redirects = {}
    write_current_pages(redirects)
    write_current_posts(redirects)
    write_d7_posts(redirects)
    write_blog_indexes()
    write_theme_pages()
    write_static_xml()
    write_redirects(redirects)
    print("Generated static site content")


if __name__ == "__main__":
    main()
