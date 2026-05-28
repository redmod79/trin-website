# Research Tools & Process

## How Each Study Was Built

Every study folder contains the complete research trail — from web research through final validated conclusion. Here's what each file represents:

### Research Files

| File | Phase | Agent | Purpose |
|------|-------|-------|---------|
| `00-references.md` | 2 | Reference Agent | Prior studies found, external corpus leads, web research integration |
| `PROMPT.md` | 3 | Scoping Agent | Tool-discovered scope: topics, verses, Strong's numbers, focus areas (rendered from validated `prompt.json`) |
| `01-topics.md` | 5 | Research Agent | Nave's Topical Dictionary entries retrieved |
| `02-verses.md` | 5 | Research Agent | Full KJV verse text with chapter context |
| `04-word-studies.md` | 5 | Research Agent | Strong's word data, library references, parsing results |
| `03-analysis.md` | 6-7 | Analysis Agent + Python | Verse-by-verse analysis, patterns, synthesis (validated against raw data) |
| `CONCLUSION.md` | 6-7 | Analysis Agent + Python | Final conclusion with all evidence (validated) |
| `conclusion-simple.md` | 8 | Summary Agent | Plain-language summary for general readers |

### The bible-study7 Difference

This series uses bible-study7, which adds two critical improvements over earlier pipelines:

1. **Structured JSON output** — The analysis agent writes `analysis_interpretation.json` with designated fields for every claim, not free-form markdown. This enables machine verification.

2. **Python validation** — A validation script cross-checks every Strong's number, every occurrence count, every parsing code, and every verse reference against the actual raw tool output before rendering the final markdown. If any factual claim doesn't match the tools, the study fails validation and the agent must correct it.

This means: no hallucinated Greek/Hebrew parsing claims, no invented occurrence counts, no verse references to passages that weren't actually researched.

### What "Tool-Discovered" Means

The scoping agent finds verses by querying Nave's Topical Dictionary and Strong's Concordance — it does NOT rely on training knowledge to select verses. This means:

- **Verses you wouldn't expect** may appear — tools find connections humans miss
- **Common proof-texts may be absent** if the tools didn't surface them for this specific question
- **The scope is reproducible** — running the same queries produces the same scope

### Two-Pass Analysis

Every study in this series had more than 25 primary verses, triggering the two-pass analysis mode:

- **Pass 1 (Verse Analysis Agent)** — Writes theological interpretation for each individual verse
- **Pass 2 (Synthesis Agent)** — Reads Pass 1 output and writes cross-verse patterns, word study integration, difficult passages, and the conclusion
- **Python Merge + Validate** — Combines both passes, validates against the factual skeleton, renders final markdown

This separation ensures the verse-level analysis doesn't contaminate the synthesis, and the synthesis builds on (rather than repeating) the verse work.

### Study 9: Historical Research

Study 9 (Catholic Suppression and the Genetic Fallacy) used a different pipeline — **egw-pioneer-study2** — because the question is historical rather than exegetical. The EGW/pioneer corpus indexes historical works by Foxe, Schaff, Wylie, D'Aubigne, Froom, and Guinness, making it an efficient way to find primary source quotes. The corpus was used as a lead-finding tool; all historical claims in the final study are attributed to the primary historians, not to EGW.

Additional web research supplemented the corpus with:

- Council of Toulouse (1229) canon text from historical records
- Wycliffe's 45 condemned articles from the Council of Constance
- Tyndale's formal trial charges at Vilvorde
- Servetus execution account from Geneva (1553)
- Legate and Wightman execution records (1612)
- Peace of Westphalia Article VII text (1648)
- Pliny the Younger's letter to Trajan (c. 112 AD)
- Ignatius of Antioch's letters (c. 108-117 AD)
- Bart Ehrman's statements on Nicaea

### Interactive Features

This website includes:

- **Search** — Full-text search across all studies
- **Dark/Light Mode** — Toggle in the header
- **Navigation** — Tab-based navigation with expandable study sections
- **Simple Conclusions** — Each study's default page is a plain-English summary; the full technical conclusion is one click deeper
