# CareerLens — NLP-Based Resume Analyzer & Job Recommendation System

A local Streamlit app for an MCA AI & ML project. It extracts PDF, DOCX and TXT resume text, detects curated skills, ranks sample role profiles with TF-IDF/cosine similarity, and shows skill gaps.

Match scores are relative to the bundled illustrative dataset. They are not hiring probabilities or guarantees.

## Features
- In-memory PDF, DOCX, TXT parsing; 10 MB upload cap.
- Normalization, TF-IDF unigram/bigram features and cosine similarity.
- Curated skill aliases, role recommendations and explainable skill gaps.
- Weighted score: 70% text similarity + 30% role skill coverage; coverage fallback if text overlap is zero.
- Career dashboard with stronger visual hierarchy, four summary cards, and a high-contrast resume uploader.
- Filter recommendations by career area and compare text similarity with listed-skill coverage.
- Prioritized skill-gap action plan, role-specific interview practice prompts, Plotly chart, and full CSV export.
- Ten sample roles and sample resume. Scanned PDFs require OCR (not included).

## Run locally
Requires Python 3.10+.
~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
~~~
On macOS/Linux activate using source .venv/bin/activate. Open the localhost URL printed by Streamlit. Try samples/sample_resume.txt.

## Validate
Run python -m unittest discover -s tests -v. For a UI smoke check, upload the sample and verify skills, category filtering, text/skill score breakdowns, gap plan, interview prompts and CSV download.

## Structure
~~~text
ResumeMatchAI/
├── app.py
├── data/jobs.csv
├── samples/sample_resume.txt
├── src/resume_matcher.py
├── src/resume_parser.py
├── tests/test_resume_matcher.py
├── requirements.txt
└── README.md
~~~

## Report-ready content
### Abstract
This project builds an NLP-based resume analyzer and job recommendation system. It extracts text from common document formats, detects technical skills with a rule-based vocabulary, and compares resumes with role profiles using TF-IDF and cosine similarity. Skill coverage exposes missing requirements. A Streamlit dashboard displays results and allows CSV export. It is an educational prototype, not a hiring decision tool.

### Objectives
Parse common resumes; normalize and vectorize text; extract known skills; rank roles; show skill gaps; present an interactive local dashboard.

### Methodology
Uploaded bytes are parsed in memory. Text is normalized and represented with TF-IDF unigrams and bigrams with English stopword filtering. A curated alias dictionary extracts skills using word boundaries. Cosine similarity compares resume and role vectors. Skill coverage is the proportion of listed role skills detected. Score = 0.70 × cosine similarity + 0.30 × skill coverage. With zero text overlap, skill coverage is used. If scikit-learn is unavailable, token Jaccard overlap provides a text similarity fallback.

### Architecture
app.py provides upload/UI/chart/export; resume_parser.py extracts PDF with pypdf, DOCX with python-docx and TXT as UTF-8; resume_matcher.py preprocesses text, detects skills, ranks roles and computes gaps; data/jobs.csv contains illustrative role records.

### Limitations and evaluation
Unit checks cover TXT parsing, aliases, ranking and zero-overlap behavior. The small illustrative dataset is not a benchmark. Scores are not probabilities. The dictionary is English and finite; synonyms may be missed. Scanned PDFs need OCR. The project supports exploration and should not automate hiring.

### Extensions
Add curated rows to data/jobs.csv and aliases to SKILL_ALIASES. Use a reviewed benchmark and ranking metrics to evaluate real-world performance.
