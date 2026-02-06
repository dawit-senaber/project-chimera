import re
from markdown import markdown
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

SRC = 'docs/Project_Chimera_SRS_Report.md'
OUT = 'docs/Project_Chimera_SRS_Report.pdf'

with open(SRC, 'r', encoding='utf-8') as f:
    md = f.read()

html = markdown(md, extensions=['extra'])
# Basic normalization: map some tags to simpler text
html = html.replace('<strong>', '<b>').replace('</strong>', '</b>')
html = html.replace('<em>', '<i>').replace('</em>', '</i>')
html = re.sub(r'<h1>(.*?)</h1>', r'<b><font size=18>\1</font></b>', html, flags=re.S)
html = re.sub(r'<h2>(.*?)</h2>', r'<b><font size=14>\1</font></b>', html, flags=re.S)
# Convert lists to simple bullets
html = html.replace('<ul>', '').replace('</ul>', '')
html = html.replace('<li>', '• ').replace('</li>', '\n')
# Strip remaining tags for robust output
text = re.sub(r'<[^>]+>', '', html)

# Build PDF with ReportLab
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(OUT, pagesize=letter)
flow = []
for para in text.split('\n\n'):
    p = para.strip()
    if not p:
        continue
    for line in p.split('\n'):
        line = line.strip()
        if not line:
            continue
        flow.append(Paragraph(line, styles['Normal']))
        flow.append(Spacer(1, 6))

try:
    doc.build(flow)
    print('WROTE', OUT)
except Exception as e:
    print('ERROR', e)
