"""Check the extracted project can resolve its pages and assets independently."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ericcruzoperations.github.io/'
PAGES = ['index.html', 'work.html', 'resume.html']

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

documents = {}
texts = {}
for name in PAGES:
    text = (ROOT/name).read_text(encoding='utf-8')
    assert 'ericcruzdigital.github.io/virtual-assistant/' not in text, name
    assert not re.search(r'(?:href|src)=[\"\']/virtual-assistant/', text), name
    assert not any(ord(c) < 32 and c not in '\r\n\t' for c in text), name
    assert '\ufffd' not in text, name
    assert not re.search(r'\bVA\b|Virtual Assistant', text, re.I), name
    assert 'Eric Cruz Operations' in text, name
    assert 'ericcruzdigital.github.io/virtual-assistant-portfolio/' not in text, name
    documents[name] = Document(text)
    texts[name] = text

resolved = set()
external = set()
for name, document in documents.items():
    page_url = BASE + ('' if name == 'index.html' else name)
    canonical = [a['href'] for t,a in document.tags if t == 'link' and a.get('rel') == 'canonical']
    og_url = [a['content'] for t,a in document.tags if t == 'meta' and a.get('property') == 'og:url']
    assert canonical == [page_url] and og_url == [page_url], name
    assert len([1 for t,a in document.tags if t == 'h1']) == 1, name
    for tag, attrs in document.tags:
        if tag not in ['a', 'img', 'link', 'script']:
            continue
        target = attrs.get('href') or attrs.get('src')
        if not target:
            continue
        url = urljoin(page_url, target)
        parts = urlsplit(url)
        if parts.scheme in ['mailto', 'tel']:
            continue
        if not url.startswith(BASE):
            assert tag == 'a', f'External dependency: {url}'
            external.add(url)
            continue
        relative = unquote(parts.path.removeprefix(urlsplit(BASE).path)) or 'index.html'
        file = ROOT/relative
        assert file.is_file(), f'{name}: missing {relative}'
        resolved.add(relative)
        if parts.fragment:
            ids = [a.get('id') for t,a in documents[relative].tags]
            assert unquote(parts.fragment) in ids, f'Missing anchor: {url}'
        if tag == 'img':
            assert attrs.get('alt'), 'Missing photo description'

manifest = json.loads((ROOT/'scripts/recovery-manifest.json').read_text(encoding='utf-8'))
for name, expected in manifest['preserved_assets'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name
for fragment in ['reporting', 'coordination', 'content']:
    assert f'id="{fragment}"' in texts['work.html'], fragment
for marker in ['Blank portfolio template', 'anonymized', 'not completed client records']:
    assert marker in texts['work.html'], marker
assert len(list((ROOT/'samples').glob('*.csv'))) == 4
locs = [e.text for e in ET.parse(ROOT/'sitemap.xml').iter() if e.tag.endswith('loc')]
assert sorted(locs) == sorted(BASE + ('' if p == 'index.html' else p) for p in PAGES)
assert BASE + 'sitemap.xml' in (ROOT/'robots.txt').read_text(encoding='utf-8')
report = {
    'result': 'passed',
    'pages': len(PAGES),
    'caseStudies': 3,
    'localTargets': sorted(resolved),
    'preservedAssets': len(manifest['preserved_assets']),
    'externalLinks': sorted(external),
    'externalNetworkVerification': 'pending',
    'scope': 'Static migration checks; browser and live checks are separate.'
}
out = ROOT/'qa-va'
out.mkdir(exist_ok=True)
(out/'migration-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
