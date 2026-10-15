"""Create the single-column PDF resume from the same content as Word and HTML."""
import json, html
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import letter

ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'scripts/va-resume.json').read_text(encoding='utf-8'))
output=ROOT/'downloads/Eric_John_Cruz_Virtual_Assistant_Resume.pdf'
styles={
 'name':ParagraphStyle('Name',fontName='Helvetica-Bold',fontSize=22,leading=26,spaceAfter=5),
 'subtitle':ParagraphStyle('Subtitle',fontName='Helvetica',fontSize=10.8,leading=14,spaceAfter=5),
 'body':ParagraphStyle('Body',fontName='Helvetica',fontSize=9.6,leading=11.6,spaceAfter=3),
 'h1':ParagraphStyle('Heading',fontName='Helvetica-Bold',fontSize=10.8,leading=13,spaceBefore=7,spaceAfter=4,keepWithNext=True),
 'h2':ParagraphStyle('Role',fontName='Helvetica-Bold',fontSize=9.9,leading=13,spaceBefore=3,spaceAfter=3,keepWithNext=True),
 'bullet':ParagraphStyle('Bullet',fontName='Helvetica',fontSize=9.6,leading=11.6,spaceAfter=3,leftIndent=11,firstLineIndent=-8)
}
story=[]
def p(text,style='body'): story.append(Paragraph(text,styles[style]))
def escape(text): return html.escape(text)
def link(label,url): return '<link href="'+escape(url)+'" color="#000000"><u>'+escape(label)+'</u></link>'
p(escape(d['name']),'name')
p(escape(d['headline']+' | '+d['subtitle']),'subtitle')
p(escape(d['location'])+' | '+link(d['email'],'mailto:'+d['email']))
p(link('Portfolio: ericcruzoperations.github.io/',d['portfolio'])+' | '+link('LinkedIn',d['linkedin']))
p('Professional Summary','h1');p(escape(d['summary']))
p('Core Skills','h1')
for label,text in d['skills']: p('<b>'+escape(label)+':</b> '+escape(text))
p('Professional Experience','h1')
for item in d['experience']:
 p(escape(item['title']),'h2')
 p(escape(item['company']+' | '+item['dates']))
 for text in item['bullets']: p('&#8226; '+escape(text),'bullet')
 if item.get('engagements'): p(escape(item['engagements']))
p('Tools','h1')
for label,text in d['tools']: p('<b>'+escape(label)+':</b> '+escape(text)+'.')
p('Selected Work','h1');p(escape(d['work']))
p(link(d['portfolio']+'work.html',d['portfolio']+'work.html'))
doc=SimpleDocTemplate(str(output),pagesize=letter,topMargin=37,bottomMargin=37,leftMargin=46,rightMargin=46,title='Eric John Cruz Operations Resume',author=d['name'])
doc.build(story)
print(output.relative_to(ROOT))
