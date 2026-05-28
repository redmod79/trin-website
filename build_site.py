"""Build script for the Trinity series website.
Copies study files from bible-studies/ and egw-studies/ to docs/studies/.
Generates verses.json and strongs.json for the popup system.
"""
import json
import re
import shutil
from pathlib import Path

BIBLE_STUDIES = Path(r"D:\bible\bible-studies")
EGW_STUDIES = Path(r"D:\bible\egw-studies")
DOCS = Path(r"D:\bible\trin-website\docs\studies")
KJV_PATH = Path(r"D:\bible\tools\data\kjv.txt")
STRONGS_DB = Path(r"D:\bible\tools\data\strongs_translations.db")
JS_DIR = Path(r"D:\bible\trin-website\docs\javascripts")

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


def build_verses_json():
    """Build verses.json from KJV text for popup system."""
    if not KJV_PATH.exists():
        print("  KJV text not found, skipping verses.json")
        return

    book_map = {
        'Genesis': 'Gen', 'Exodus': 'Exo', 'Leviticus': 'Lev',
        'Numbers': 'Num', 'Deuteronomy': 'Deu', 'Joshua': 'Jos',
        'Judges': 'Jdg', 'Ruth': 'Rth', '1 Samuel': '1Sa',
        '2 Samuel': '2Sa', '1 Kings': '1Ki', '2 Kings': '2Ki',
        '1 Chronicles': '1Ch', '2 Chronicles': '2Ch', 'Ezra': 'Ezr',
        'Nehemiah': 'Neh', 'Esther': 'Est', 'Job': 'Job',
        'Psalms': 'Psa', 'Proverbs': 'Pro', 'Ecclesiastes': 'Ecc',
        'Song of Solomon': 'Sng', 'Isaiah': 'Isa', 'Jeremiah': 'Jer',
        'Lamentations': 'Lam', 'Ezekiel': 'Ezk', 'Daniel': 'Dan',
        'Hosea': 'Hos', 'Joel': 'Jol', 'Amos': 'Amo',
        'Obadiah': 'Oba', 'Jonah': 'Jon', 'Micah': 'Mic',
        'Nahum': 'Nah', 'Habakkuk': 'Hab', 'Zephaniah': 'Zep',
        'Haggai': 'Hag', 'Zechariah': 'Zec', 'Malachi': 'Mal',
        'Matthew': 'Mat', 'Mark': 'Mrk', 'Luke': 'Luk',
        'John': 'Jhn', 'Acts': 'Act', 'Romans': 'Rom',
        '1 Corinthians': '1Co', '2 Corinthians': '2Co',
        'Galatians': 'Gal', 'Ephesians': 'Eph', 'Philippians': 'Php',
        'Colossians': 'Col', '1 Thessalonians': '1Th',
        '2 Thessalonians': '2Th', '1 Timothy': '1Ti',
        '2 Timothy': '2Ti', 'Titus': 'Tit', 'Philemon': 'Phm',
        'Hebrews': 'Heb', 'James': 'Jas', '1 Peter': '1Pe',
        '2 Peter': '2Pe', '1 John': '1Jn', '2 John': '2Jn',
        '3 John': '3Jn', 'Jude': 'Jud', 'Revelation': 'Rev'
    }

    verses = {}
    pattern = re.compile(r'^(.+?)\s+(\d+):(\d+)\t(.+)$')

    with open(KJV_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line.strip())
            if not m:
                continue
            book_full, ch, vs, text = m.groups()
            abbr = book_map.get(book_full, book_full[:3])
            chapter_key = f"{abbr} {ch}"
            verse_key = f"{abbr} {ch}:{vs}"
            if chapter_key not in verses:
                verses[chapter_key] = {}
            verses[chapter_key][verse_key] = text

    JS_DIR.mkdir(parents=True, exist_ok=True)
    out = JS_DIR / "verses.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(verses, f, separators=(',', ':'))
    size_mb = out.stat().st_size / (1024 * 1024)
    print(f"  Built verses.json ({size_mb:.1f} MB)")


def build_strongs_json():
    """Build strongs.json from the strongs database."""
    import sqlite3
    if not STRONGS_DB.exists():
        print("  Strong's DB not found, skipping strongs.json")
        return

    conn = sqlite3.connect(str(STRONGS_DB))
    cur = conn.cursor()

    strongs = {}
    try:
        cur.execute("SELECT strongs_number, word, transliteration, definition FROM lexicon")
        for num, word, translit, defn in cur.fetchall():
            strongs[num] = {
                "word": word or "",
                "translit": translit or "",
                "def": (defn or "")[:300]
            }
    except Exception as e:
        print(f"  Error reading Strong's DB: {e}")
        try:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cur.fetchall()]
            print(f"  Available tables: {tables}")
        except:
            pass
    finally:
        conn.close()

    if strongs:
        out = JS_DIR / "strongs.json"
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(strongs, f, separators=(',', ':'))
        print(f"  Built strongs.json ({len(strongs)} entries)")
    else:
        print("  No Strong's data found")


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

        raw_src = src / "raw-data"
        raw_dst = dst / "raw-data"
        if raw_src.exists():
            raw_dst.mkdir(exist_ok=True)
            for f in raw_src.glob("*.md"):
                shutil.copy2(f, raw_dst / f.name)

        print(f"  {slug}: {copied} files copied")

    # Copy shared assets
    sv_js = Path(r"D:\bible\sv-website\docs\javascripts")
    for js_file in ["verse-popup.js", "external-links.js"]:
        src_js = sv_js / js_file
        if src_js.exists():
            shutil.copy2(src_js, JS_DIR / js_file)
            print(f"  Copied {js_file}")

    # Copy CSS
    sv_css = Path(r"D:\bible\sv-website\docs\stylesheets")
    trin_css = Path(r"D:\bible\trin-website\docs\stylesheets")
    trin_css.mkdir(exist_ok=True)
    css_src = sv_css / "extra.css"
    if css_src.exists():
        shutil.copy2(css_src, trin_css / "extra.css")
        print("  Copied extra.css")

    # Build JSON data files for popups
    build_verses_json()
    build_strongs_json()

    print("\nBuild complete. Run: cd D:\\bible\\trin-website && mkdocs serve")


if __name__ == "__main__":
    main()
