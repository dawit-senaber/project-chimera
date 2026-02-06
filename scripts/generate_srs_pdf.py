import pathlib
import markdown
from weasyprint import HTML


def main():
    src = pathlib.Path("docs/Project_Chimera_SRS_Report.md")
    out = pathlib.Path("docs/Project_Chimera_SRS_Report.pdf")
    if not src.exists():
        print(f"Source not found: {src}")
        raise SystemExit(1)
    text = src.read_text(encoding="utf-8")
    html = markdown.markdown(text)
    HTML(string=html).write_pdf(str(out))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
