# Methodology

## Research Pipeline

Studies 1-8 and 10 were produced through the **bible-study7** pipeline — a seven-phase, multi-agent system with structured JSON validation. Study 9 used the **egw-pioneer-study2** pipeline for historical source research.

### bible-study7 Pipeline (Studies 1-8, 10)

1. **Web Research** — A web research agent searches for scholarly commentary, seminary publications, peer-reviewed articles, and linguistic analysis online. Findings become leads for downstream verification, not evidence.

2. **Reference Gathering** — A reference agent searches the 640+ study library for prior work, reads completed series studies, and queries external corpora (EGW writings, Secrets Unsealed, Apocrypha) for research leads.

3. **Scope Discovery** — A scoping agent uses tools (not training knowledge) to discover the study's scope: Nave's Topical Dictionary queries, Strong's concordance searches, semantic search for related studies, and word-studies/grammar-reference library checks. The output is a `prompt.json` file validated by Python, then rendered as PROMPT.md.

4. **Library Generation** — Missing word studies and grammar references are generated as canonical entries by parallel subagents before research begins. Over 30 new word studies and several grammar reference entries were created for this series.

5. **Data Gathering** — A research agent retrieves full verse text with chapter context, runs cross-testament parallels in both directions, parses Hebrew and Greek morphology via Text-Fabric, and writes structured `research.json`. The research agent does NOT interpret — it only gathers. Python validates the research against the scope manifest.

6. **Structured Analysis** — For studies with more than 25 primary verses (all studies in this series), a two-pass analysis runs: Pass 1 writes per-verse theological interpretation, Pass 2 writes cross-verse synthesis (patterns, word study integration, difficult passages, conclusion). The outputs are JSON files.

7. **Validation and Rendering** — Python merges the analysis skeleton (factual data from research) with the interpretation (theological synthesis), validates every claim against raw tool output (Strong's numbers, occurrence counts, verse references), and renders the final `03-analysis.md` and `CONCLUSION.md` only if validation passes. If validation fails, the agent corrects errors and re-submits.

### egw-pioneer-study2 Pipeline (Study 9)

Study 9 used the EGW/pioneer corpus as a **lead-finding tool for primary historical sources**, not as a theological authority. The corpus indexes works by historians including Foxe, Schaff, Wylie, D'Aubigne, Froom, Guinness, and Elliott. Additional web research supplemented the corpus with primary source documentation.

1. **Reference Gathering** — Prior studies searched across both the EGW and Bible study libraries
2. **Scope Discovery** — EGW search queries planned with specific book/author filters
3. **Research** — 38 semantic searches executed across the 1.32M-paragraph corpus; historian quotes extracted with full refcodes
4. **Web Research** — 10 additional web searches for primary historical documentation (council records, trial records, contemporary accounts)
5. **Analysis** — Historical claims attributed to primary historians (Foxe, Schaff, Wylie); EGW referenced only for the SDA pioneer transition counter-example

## Interpretive Principles

- **Scripture interprets Scripture** — meaning is derived from how the Bible itself uses terms, not from external theological frameworks
- **Contextual analysis** — expanding circles: verse, chapter, book, same author, cross-testament
- **Historical-grammatical method** — Hebrew and Greek grammar inform meaning; context must match before importing meaning across passages
- **Scripture is the only authority for doctrine** — external corpora (EGW, historians, scholars) are research leads, not evidence
- **Self-supporting studies** — each study stands on its own evidence from tools; no study depends on conclusions from unpublished standalone studies
- **Honest engagement** — genuine difficulties are acknowledged, not dismissed; the strongest anti-Trinity arguments are stated fairly before being addressed

## Tools Used

All tools are local Python scripts running against local databases:

| Tool | Purpose |
|------|---------|
| **Nave's Topical Dictionary** | 5,319 topics with verse references |
| **Strong's Concordance** | Hebrew, Aramaic, and Greek word database with translation distributions |
| **Hebrew Parser** (Text-Fabric/BHSA) | Morphological parsing, clause structure, construct chains |
| **Greek Parser** (Text-Fabric/N1904) | Morphological parsing, tense/voice/mood analysis |
| **Cross-Testament Parallels** | Hybrid scoring (semantic + keyword + theological phrase matching) |
| **Concept Context** | Finds verses with same theological concepts, prioritized by proximity |
| **Grammar Reference Search** | Semantic search across 10 Hebrew/Greek grammar textbooks |
| **Word Studies Library** | 1,400+ canonical word studies by Strong's number |
| **Grammar Reference Library** | Hebrew stems, Greek tenses, passage analyses |
| **EGW Semantic Search** | 1.32M indexed paragraphs from EGW, Haskell, Froom (Study 9 only) |
| **Web Search** | Scholarly articles, seminary publications, peer-reviewed commentary |

## What the Validation Catches

The Python validation scripts enforce:

- Every required verse from the scope manifest has been researched
- Every Strong's number occurrence count matches actual tool output
- Every parsing claim matches the Greek/Hebrew parser output
- Every conclusion claim references a verse that was actually researched
- Every word study integration entry uses the canonical transliteration from the library
- Minimum quality thresholds for analysis depth (character counts per section)

Claims that fail validation are sent back to the agent for correction. No study reaches publication with unverified factual claims about original-language data.

## Word Studies Generated for This Series

Over 30 new canonical word studies were created during this series, including:

- **G4416** prototokos (firstborn) — the central battleground for Study 1
- **G3187** meizon (greater) and **G2909** kreitton (better) — the critical distinction for Study 2
- **G5293** hypotasso (subject/subordinate) — key to 1 Corinthians 15:28
- **G2470** isos (equal) — John 5:18 and Philippians 2:6
- **G725** harpagmos (grasped) — the Philippians 2:6 hapax
- **G473** anti (instead of) — substitutionary force in Matthew 20:28
- **G1014** boulomai (to will deliberately) — the Spirit's volitional agency
- **G3076** lupeo (to grieve) — the Spirit as grievable person
- **G5427** phronema (mind/mindset) — the Spirit's cognitive faculty
- **G2320** theotes (deity/Godhead) — Colossians 2:9 hapax
- **G5287** hypostasis (substance/essence) — Hebrews 1:3
- **G179** akatalytos (indestructible) — Hebrews 7:16 hapax
- **G1941** epikaleomai (to call upon/invoke) — prayer directed to Jesus

Each word study includes occurrence counts, translation distributions, semantic categories, LXX Hebrew-source mappings with PMI values, collocations, and word family connections — all verified against tool output.
