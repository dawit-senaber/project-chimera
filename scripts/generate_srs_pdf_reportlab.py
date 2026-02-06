from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pathlib


def main():
    src = pathlib.Path("docs/Project_Chimera_SRS_Report.md")
    out = pathlib.Path("docs/Project_Chimera_SRS_Report.pdf")
    if not src.exists():
        print(f"Source not found: {src}")
        raise SystemExit(1)
    text = src.read_text(encoding="utf-8")
    doc = SimpleDocTemplate(str(out), pagesize=letter)
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    story = []
    for para in text.split('\n\n'):
        para = para.strip()
        if not para:
            story.append(Spacer(1, 6))
            continue
        # Keep Markdown raw, escaped for XML
        safe = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        story.append(Paragraph(safe.replace('\n', '<br/>'), normal))
        story.append(Spacer(1, 6))
    doc.build(story)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
