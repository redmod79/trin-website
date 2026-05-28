"""Build script for the Trinity series website.
Copies study files from bible-studies/ and egw-studies/ to docs/studies/.
"""
import shutil
from pathlib import Path

BIBLE_STUDIES = Path(r"D:\bible\bible-studies")
EGW_STUDIES = Path(r"D:\bible\egw-studies")
DOCS = Path(r"D:\bible\trin-website\docs\studies")

STUDIES = [
    ("trin-01-firstborn-created-being", BIBLE_STUDIES),
    ("trin-02-subordination-passages", BIBLE_STUDIES),
    ("trin-03-only-true-god", BIBLE_STUDIES),
    ("trin-04-ransom-sacrifice", BIBLE_STUDIES),
    ("trin-05-my-god-only-god-good", BIBLE_STUDIES),
    ("trin-06-holy-spirit-personhood", BIBLE_STUDIES),
    ("trin-07-what-breaks-if-not-god", BIBLE_STUDIES),
    ("trin-08-monotheism-deity-synthesis", BIBLE_STUDIES),
    ("trin-09-catholic-suppression-genetic-fallacy", EGW_STUDIES),
    ("trin-10-pre-nicene-nt-evidence", BIBLE_STUDIES),
]

COPY_FILES = [
    "CONCLUSION.md",
    "conclusion-simple.md",
    "03-analysis.md",
    "02-verses.md",
    "04-word-studies.md",
    "01-topics.md",
    "PROMPT.md",
    "00-references.md",
]

def main():
    for slug, source_base in STUDIES:
        src = source_base / slug
        dst = DOCS / slug
        dst.mkdir(parents=True, exist_ok=True)

        copied = 0
        for fname in COPY_FILES:
            src_file = src / fname
            if src_file.exists():
                shutil.copy2(src_file, dst / fname)
                copied += 1

        # Copy raw-data if it exists
        raw_src = src / "raw-data"
        raw_dst = dst / "raw-data"
        if raw_src.exists():
            raw_dst.mkdir(exist_ok=True)
            for f in raw_src.glob("*.md"):
                shutil.copy2(f, raw_dst / f.name)

        print(f"  {slug}: {copied} files copied")

    # Copy shared assets
    sv_js = Path(r"D:\bible\sv-website\docs\javascripts")
    trin_js = Path(r"D:\bible\trin-website\docs\javascripts")
    for js_file in ["verse-popup.js", "external-links.js"]:
        src_js = sv_js / js_file
        if src_js.exists():
            shutil.copy2(src_js, trin_js / js_file)
            print(f"  Copied {js_file}")

    # Copy CSS
    sv_css = Path(r"D:\bible\sv-website\docs\stylesheets")
    trin_css = Path(r"D:\bible\trin-website\docs\stylesheets")
    trin_css.mkdir(exist_ok=True)
    css_src = sv_css / "extra.css"
    if css_src.exists():
        shutil.copy2(css_src, trin_css / "extra.css")
        print("  Copied extra.css")

    # Copy overrides
    sv_over = Path(r"D:\bible\sv-website\overrides\main.html")
    trin_over = Path(r"D:\bible\trin-website\overrides\main.html")
    if sv_over.exists():
        shutil.copy2(sv_over, trin_over)
        print("  Copied overrides/main.html")

    print("\nBuild complete. Run: cd D:\\bible\\trin-website && mkdocs serve")

if __name__ == "__main__":
    main()
