import argparse, json, re, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--word-render', type=Path)
args = parser.parse_args()
d = json.loads((root/"scripts/va-resume.json").read_text(encoding="utf-8"))
out = root/"qa-va"
out.mkdir(exist_ok=True)
docx = root/"downloads/Eric_John_Cruz_Virtual_Assistant_Resume.docx"
pdf = root/"downloads/Eric_John_Cruz_Virtual_Assistant_Resume.pdf"
ns = {"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
with zipfile.ZipFile(docx) as z:
    xml = ET.fromstring(z.read("word/document.xml"))
    doc_text = " ".join(n.text or "" for n in xml.findall(".//w:t", ns))
    assert not xml.findall(".//w:pBdr", ns), "No decorative paragraph borders"
    assert not xml.findall(".//w:tbl", ns), "Resume must use a single text column, no tables"
    assert not xml.findall(".//w:drawing", ns), "No images in ATS resume"
    assert not xml.findall(".//w:ins", ns) and not xml.findall(".//w:del", ns)
    styles = ET.fromstring(z.read('word/styles.xml'))
    assert not styles.findall('.//w:pBdr', ns), 'No inherited decorative borders'
    relationships = z.read('word/_rels/document.xml.rels').decode('utf-8')
    assert d['portfolio'] in relationships
    assert 'ericcruzdigital.github.io/virtual-assistant' not in relationships
reader = PdfReader(pdf)
assert len(reader.pages) == 1, f"Unexpected PDF page count: {len(reader.pages)}"
pdf_text = "\n".join(p.extract_text() for p in reader.pages)
html = (root/"resume.html").read_text(encoding="utf-8")
def normalize(s):
    return re.sub(r"\s+", " ", s).replace("\u2013","-").strip()
facts = [d["name"],d["headline"],d["subtitle"],d["summary"],d["email"]]
for e in d["experience"]:
    facts += [e["title"], e["company"], e["dates"], *e["bullets"]]
    if "engagements" in e: facts.append(e["engagements"])
facts += [text for _,text in d["skills"]] + [text for _,text in d["tools"]] + [d["work"]]
assert "ericcruzdigital.github.io/virtual-assistant/" not in doc_text + pdf_text + html
assert d["portfolio"] in doc_text and d["portfolio"] in pdf_text
import html as htmlmodule
html_text = htmlmodule.unescape(re.sub("<[^>]+>", " ", html))
for fact in facts:
    for name, text in [("Word", doc_text), ("PDF", pdf_text), ("online", html_text)]:
        assert normalize(fact) in normalize(text), f"{name} missing fact: {fact}"
for pattern in [r"JDS1", r"\$\d", "Electrical Engineer", "cold calling", "Salesforce", "HubSpot", "Zapier"]:
    assert not re.search(pattern, doc_text, re.I), f"Unverified or out-of-scope content: {pattern}"
report={"pages":len(reader.pages),"sharedFacts":len(facts),"formats":["Word","PDF","online"],"tables":0,"images":0,"selectableText":True,"result":"passed"}
if args.word_render:
    rendered = list(args.word_render.glob('*.pdf'))
    assert len(rendered) == 1, f'Expected one rendered Word PDF: {rendered}'
    word_pdf = PdfReader(rendered[0])
    assert len(word_pdf.pages) == 1, f'Word resume spills to {len(word_pdf.pages)} pages'
    rendered_text = '\n'.join(page.extract_text() for page in word_pdf.pages)
    for fact in facts:
        assert normalize(fact) in normalize(rendered_text), f'Word render missing fact: {fact}'
    assert list(args.word_render.glob('*.png')), 'Word page images missing'
    report['renderedWordPages'] = len(word_pdf.pages)
    report['renderedWordFacts'] = len(facts)
(out/"resume-report.json").write_text(json.dumps(report,indent=2))
(out/"resume-text.txt").write_text(pdf_text,encoding="utf-8")
print(json.dumps(report))
