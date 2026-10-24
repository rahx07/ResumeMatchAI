# CareerLens — NLP-Based Resume Analyzer & Job Recommendation System

An NLP-powered resume analyzer and job recommendation system built with Python and Streamlit. CareerLens extracts information from resumes, identifies relevant skills, recommends matching job roles, and highlights skill gaps to help users plan their career development.

Developed as an MCA Artificial Intelligence & Machine Learning project.

> **Disclaimer:** CareerLens is an educational prototype that uses an illustrative dataset. Match scores are relative similarity indicators, not hiring probabilities or guarantees.

---

## Application Preview

![CareerLens Dashboard](assets/careerlens-dashboard.png)

---

## Key Features

- **Resume Parsing:** Extract text from PDF, DOCX, and TXT resumes.
- **Skill Extraction:** Identify technical skills using a curated vocabulary and skill aliases.
- **NLP-Based Matching:** Use TF-IDF unigram/bigram features and cosine similarity to compare resumes with job descriptions.
- **Job Recommendations:** Rank illustrative job profiles according to resume relevance.
- **Skill Gap Analysis:** Highlight missing skills for recommended roles.
- **Weighted Matching Score:** Combine text similarity and role-specific skill coverage.
- **Career Dashboard:** Display key results through an interactive Streamlit interface.
- **Career Area Filtering:** Filter recommended roles by career category.
- **Interview Preparation:** Generate role-specific interview practice prompts.
- **Visual Analytics:** Explore recommendation results through interactive Plotly charts.
- **CSV Export:** Download recommendation results for further analysis.
- **Privacy-Conscious Processing:** Process uploaded resume content in memory without intentionally saving uploaded resume files to disk.
- **Upload Validation:** Apply a 10 MB upload limit.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| Natural Language Processing | TF-IDF |
| Text Similarity | Cosine Similarity |
| Machine Learning Utilities | scikit-learn |
| PDF Parsing | pypdf |
| DOCX Parsing | python-docx |
| Data Processing | Pandas |
| Data Visualization | Plotly |
| Dataset Format | CSV |
| Testing | Python unittest |
| Version Control | Git and GitHub |

## How It Works

CareerLens follows a structured resume analysis and recommendation workflow:

1. **Resume Upload:** The user uploads a PDF, DOCX, or TXT resume.
2. **Text Extraction:** The application extracts readable text from the uploaded document.
3. **Text Preprocessing:** The text is normalized and prepared for analysis.
4. **Skill Detection:** A curated skill dictionary and alias mapping identify known skills.
5. **Text Vectorization:** TF-IDF represents resume and job-description text using unigram and bigram features.
6. **Similarity Calculation:** Cosine similarity estimates the textual relevance between the resume and each role.
7. **Skill Coverage Analysis:** Detected resume skills are compared with the listed skills for each role.
8. **Recommendation Ranking:** A weighted score ranks the available role profiles.
9. **Skill Gap Analysis:** Missing role-specific skills are highlighted.
10. **Results and Export:** The dashboard displays recommendations, visualizations, interview prompts, and downloadable CSV results.

### Matching Score

The default weighted matching score is:

**Matching Score = (0.70 × Text Similarity) + (0.30 × Skill Coverage)**

Where:

- **Text Similarity:** Measures the similarity between resume text and job-description text using cosine similarity.
- **Skill Coverage:** Measures the proportion of listed role skills detected in the resume.

If text similarity is zero, the implementation uses skill coverage as a fallback.

The score is a relative ranking indicator for the bundled dataset. It must not be interpreted as a probability of getting hired.

## Project Structure

```text
ResumeMatchAI/
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   └── careerlens-dashboard.png
│
├── data/
│   └── jobs.csv
│
├── samples/
│   └── sample_resume.txt
│
├── src/
│   ├── __init__.py
│   ├── resume_matcher.py
│   └── resume_parser.py
│
├── tests/
│   └── test_resume_matcher.py
│
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

*Note: The structure above documents the intended project layout. The dashboard screenshot is optional; add it to `assets/` before using the preview image link.*

## Prerequisites

Before running CareerLens, make sure you have:

- Python 3.10 or later
- pip
- Git (optional, for cloning the repository)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rahx07/ResumeMatchAI.git
```

### 2. Open the Project Directory

```bash
cd ResumeMatchAI
```

### 3. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can activate the environment from Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Application

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to use CareerLens.

## Using the Application

1. Start the application using Streamlit.
2. Upload a supported resume file.
3. Review the extracted resume information and detected skills.
4. Explore recommended job profiles and their matching scores.
5. Compare text similarity with role-specific skill coverage.
6. Review missing skills and the suggested skill-gap action plan.
7. Explore interview practice prompts and visual analytics.
8. Export the recommendation results as a CSV file.

You can also try the bundled sample resume:

```text
samples/sample_resume.txt
```

## Testing and Validation

CareerLens includes unit tests for core resume analysis functionality.

Run the tests from the project root:

```bash
python -m unittest discover -s tests -v
```

The tests cover core behavior such as:

- TXT resume parsing
- Skill detection and aliases
- Role recommendation ranking
- Zero-text-overlap fallback behavior

For a manual UI smoke test, upload the sample resume and verify:

- Resume text extraction
- Skill detection
- Career area filtering
- Text similarity and skill coverage
- Skill-gap recommendations
- Interview practice prompts
- Plotly visualizations
- CSV export

## NLP Methodology

### Text Preprocessing

Resume and job-description text is normalized before vectorization to make textual comparisons more consistent.

### TF-IDF Vectorization

Term Frequency–Inverse Document Frequency (TF-IDF) represents documents numerically. The implementation uses unigram and bigram features with English stopword filtering.

### Cosine Similarity

Cosine similarity compares the vector representations of a resume and a job description. Higher similarity indicates greater textual overlap in the vector space.

### Skill Extraction

A curated dictionary and skill alias mapping identify known technical skills. Word-boundary matching helps reduce accidental matches within unrelated words.

### Skill Coverage

Skill coverage measures how many of a role's listed skills are detected in the resume.

### Recommendation Ranking

The application combines text similarity and skill coverage using the weighted matching formula described above. When text overlap is zero, skill coverage provides a fallback score.

If scikit-learn is unavailable, the implementation includes a token-based Jaccard similarity fallback.

## System Architecture

The application is organized into separate components:

| Component | Responsibility |
|---|---|
| `app.py` | Streamlit interface, resume upload, dashboard, charts, filters, and CSV export |
| `src/resume_parser.py` | Extract text from PDF, DOCX, and TXT files |
| `src/resume_matcher.py` | Text preprocessing, skill extraction, similarity calculation, recommendation ranking, and skill-gap analysis |
| `data/jobs.csv` | Illustrative job-role profiles and associated skills |
| `samples/sample_resume.txt` | Sample resume for testing the application |
| `tests/test_resume_matcher.py` | Unit tests for core matching functionality |
| `.streamlit/config.toml` | Streamlit application configuration |
| `requirements.txt` | Python dependency list |

## Dataset

CareerLens uses a bundled illustrative dataset of ten sample job roles.

The dataset supports demonstration and testing of the recommendation workflow. It is not a comprehensive representation of the job market and should not be used to draw conclusions about actual hiring outcomes.

The dataset can be extended by adding appropriately formatted role records to:

```text
data/jobs.csv
```

Skill aliases can be extended in the relevant skill dictionary within the matching implementation.

## Limitations

- The bundled dataset is small and illustrative.
- Matching scores are relative similarity indicators, not hiring probabilities.
- The curated skill dictionary is finite and primarily English-based.
- Unrecognized synonyms and contextual meanings may be missed.
- Scanned PDFs require OCR, which is not included.
- Resume formatting and document quality can affect text extraction.
- TF-IDF and cosine similarity do not fully understand the semantic meaning of a resume.
- The current implementation is an educational prototype rather than a validated recruitment assessment system.
- The included tests cover selected functionality, not every possible input or real-world scenario.

## Future Enhancements

Potential improvements include:

- Expanding the job-role dataset with reviewed and representative data.
- Adding OCR support for scanned resumes.
- Improving skill extraction with named entity recognition and semantic NLP models.
- Incorporating semantic embeddings for more context-aware matching.
- Adding a reviewed benchmark and ranking metrics for systematic evaluation.
- Improving multilingual resume support.
- Adding more comprehensive automated tests.
- Supporting configurable job descriptions and user-defined skill requirements.
- Improving accessibility and responsive dashboard design.

## Academic Project Information

**Project Title:** CareerLens — NLP-Based Resume Analyzer & Job Recommendation System

**Domain:** Natural Language Processing, Machine Learning, and Career Analytics

**Application Framework:** Streamlit

**Purpose:** To demonstrate how text processing, skill extraction, and similarity-based ranking can support resume analysis and exploratory job recommendations.

**Academic Context:** MCA — Artificial Intelligence & Machine Learning

## Author

**Rahul Ranjan**

GitHub: [@rahx07](https://github.com/rahx07)

## Disclaimer

CareerLens is intended for educational and informational purposes only. Its recommendations depend on the available dataset, extracted resume text, and implemented matching rules.

The system does not guarantee employment, predict hiring decisions, or replace professional career guidance. Users should independently evaluate job requirements and career opportunities.

---

⭐ If you find this project useful, consider starring the repository.
