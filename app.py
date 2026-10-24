from pathlib import Path
import html
import pandas as pd
import plotly.express as px
import streamlit as st

from src.resume_matcher import analyze_resume, load_jobs
from src.resume_parser import extract_resume_text, ResumeParseError

ROOT = Path(__file__).parent
JOBS = load_jobs(ROOT / "data" / "jobs.csv")
st.set_page_config(page_title="CareerLens | Resume Intelligence", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root{--ink:#14251f;--muted:#72827b;--line:#e4ece7;--paper:#f4f7f5;--green:#176b50;--mint:#d8f3e7}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.stApp{background:var(--paper);color:var(--ink)}
[data-testid="stSidebar"]{background:#14251f}[data-testid="stSidebar"] *{color:#e8f1ec}
.brand{font:800 25px Manrope,sans-serif;color:#f7fbf9;padding:16px 4px 0;letter-spacing:-1px}.brand span{color:#75d3aa}
.side-caption{color:#9bb1a6!important;font-size:11px;letter-spacing:1.4px;margin:2px 4px 24px}
.hero{background:linear-gradient(115deg,#153b2e,#176b50 65%,#24835f);border-radius:22px;padding:30px 34px;color:white;margin:2px 0 22px;box-shadow:0 16px 36px #173e2b22}
.hero-kicker{color:#aee7ca;font-size:11px;font-weight:700;letter-spacing:1.7px;text-transform:uppercase}
.hero-title{font:800 32px Manrope,sans-serif;letter-spacing:-1.2px;margin:7px 0 3px;color:white}
.hero-copy{color:#d5ebe0;font-size:14px;margin:0}
.section-title{font:700 20px Manrope,sans-serif;letter-spacing:-.4px;margin:18px 0 10px}
.eyebrow{color:var(--green);text-transform:uppercase;font-size:10px;font-weight:700;letter-spacing:1.4px}
.card{background:white;border:1px solid var(--line);border-radius:17px;padding:18px 20px;box-shadow:0 4px 16px #173e2b08}
.metric-label{color:var(--muted);font-size:12px;font-weight:600}.metric-value{font:800 27px Manrope,sans-serif;letter-spacing:-.7px;color:var(--ink);margin-top:3px}
.metric-note{color:var(--muted);font-size:11px;margin-top:2px}
.tag{display:inline-block;background:#e6f5ed;color:#176b50;padding:6px 10px;margin:3px 4px 3px 0;border-radius:22px;font-size:11px;font-weight:600}
.tag-missing{background:#fff0e8;color:#a35326}
div[data-testid="stFileUploader"]{background:#fff;border:1px dashed #9bbcab;border-radius:16px;padding:10px}
div[data-testid="stFileUploader"] section{background:#edf5f0!important;border:1px dashed #a9c7b9!important}
div[data-testid="stFileUploader"] section *{color:#244c3b!important}
div[data-testid="stFileUploader"] button{background:white!important;border:1px solid #bfd3c7!important}
div.stButton>button,div.stDownloadButton>button{border-radius:10px;font-weight:700;min-height:42px}
div[data-testid="stExpander"]{background:#fff;border:1px solid var(--line);border-radius:13px}
div[data-testid="stProgress"]>div>div{background:#20825e}
[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 18px}
hr{border-color:var(--line)}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="brand">Career<span>Lens</span></div><div class="side-caption">RESUME INTELLIGENCE · NLP PROJECT</div>', unsafe_allow_html=True)
    page = st.radio("Workspace", ["Resume analysis", "How it works", "Project details"], label_visibility="collapsed")
    st.divider()
    st.markdown("**Your analysis toolkit**")
    st.caption("✦ Skill extraction")
    st.caption("↗ Role matching")
    st.caption("◎ Gap planner")
    st.caption("◉ Interview practice")
    st.divider()
    st.caption(f"{len(JOBS)} sample role profiles")
    st.caption("Local-first · files processed in memory")

def hero(kicker, title, copy):
    st.markdown(f'<div class="hero"><div class="hero-kicker">{kicker}</div><div class="hero-title">{title}</div><p class="hero-copy">{copy}</p></div>', unsafe_allow_html=True)

def chips(items, missing=False):
    cls = "tag tag-missing" if missing else "tag"
    return "".join(f'<span class="{cls}">{html.escape(str(item))}</span>' for item in items)

def interview_prompts(role):
    category = role["category"]
    if "Data" in category:
        return [
            ("How would you investigate a dataset with missing values and inconsistent formats?", "Explain profiling, cleaning decisions, validation and documenting assumptions."),
            ("Describe a project where analysis changed or clarified a decision.", "Use a clear situation, method, result structure; quantify the result if you can."),
            ("How would you explain a model or chart to a non-technical stakeholder?", "Focus on the audience, the takeaway, limitations and next action."),
        ]
    if "AI" in category:
        return [
            ("How would you choose a baseline for a new machine-learning problem?", "Cover the task, simple baseline, metric, data leakage and iteration plan."),
            ("What would you monitor after deploying a model?", "Discuss service health, data drift, model quality, latency and rollback."),
            ("Explain a model project you built and one trade-off you made.", "Describe your role, method, evaluation, limitations and what you would improve."),
        ]
    return [
        ("How would you design a reliable API or application feature?", "Cover requirements, interfaces, validation, errors, tests and observability."),
        ("Tell me about a technical problem you debugged.", "Walk through evidence gathering, root cause, fix and prevention."),
        ("How do you collaborate when a requirement is unclear?", "Explain how you ask focused questions, agree on behavior and communicate progress."),
    ]

if page == "How it works":
    hero("Methodology", "A transparent path from resume to roles.", "See which signals contribute to each recommendation.")
    cols = st.columns(3)
    cards = [("01 · EXTRACT", "Resume text", "Read PDF, DOCX or TXT content in memory. Scanned PDFs need OCR, which is not included."),
             ("02 · UNDERSTAND", "Skills and language", "Normalize text and detect configured skills with boundary-aware aliases. TF-IDF represents role and resume text."),
             ("03 · EXPLAIN", "Matches and gaps", "Cosine similarity ranks language fit. Listed skill coverage reveals strengths and next skills to build.")]
    for col, (k, t, d) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="card"><div class="eyebrow">{k}</div><h3>{t}</h3><p style="color:#72827b">{d}</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">How the score is calculated</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><b>70% text similarity</b> from TF-IDF vectors and cosine similarity + <b>30% skill coverage</b> from the role’s listed skills. If no role shares text vocabulary with the resume, the app uses skill coverage alone. The score is a relative match to this sample dataset, not a hiring probability.</div>', unsafe_allow_html=True)
    st.info("Skill extraction uses a curated English dictionary. It may miss synonyms or infer a listed skill from context incorrectly; review the results.")
elif page == "Project details":
    hero("Semester project", "NLP-Based Resume Analyzer", "Project overview and implementation details for your report.")
    st.markdown('<div class="card"><div class="eyebrow">OBJECTIVE</div><p>Build an explainable local application that reads resumes, identifies configured skills, recommends relevant sample job roles, and highlights skill gaps.</p><div class="eyebrow">TECHNOLOGY</div><p>Python · Streamlit · pandas · scikit-learn TF-IDF · cosine similarity · Plotly · pypdf · python-docx</p><div class="eyebrow">LIMITATIONS</div><p>Role records are illustrative, scores are not calibrated probabilities, extraction is limited to configured English skill aliases, and scanned PDFs require OCR.</p></div>', unsafe_allow_html=True)
else:
    hero("CareerLens · Resume intelligence", "Turn your resume into a career action plan.", "Discover matching roles, understand the score, and see what skill to strengthen next.")
    upload_col, note_col = st.columns([1.15, .85], gap="medium")
    with upload_col:
        uploaded = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"], help="PDF, DOCX or TXT · Maximum 10 MB")
        st.caption("Your document is read in memory by this local app.")
    with note_col:
        st.markdown('<div class="card"><div class="eyebrow">YOUR ANALYSIS INCLUDES</div><h3>More than a match score</h3><p style="color:#72827b">Role comparisons · skill strengths · prioritized gaps · interview practice · CSV export</p></div>', unsafe_allow_html=True)
    if uploaded:
        if uploaded.size > 10 * 1024 * 1024:
            st.error("This file exceeds the 10 MB limit. Please choose a smaller file.")
            st.stop()
        try:
            text = extract_resume_text(uploaded.name, uploaded.getvalue())
        except ResumeParseError as exc:
            st.error(str(exc))
            st.stop()
        if len(text.strip()) < 40:
            st.warning("Very little text was extracted. This may be a scanned PDF; OCR is not included.")
        elif st.button("Analyze my resume", type="primary", use_container_width=True):
            st.session_state["careerlens_analysis"] = {
                "result": analyze_resume(text, JOBS), "name": uploaded.name
            }

    data = st.session_state.get("careerlens_analysis")
    if data:
        result = data["result"]
        matches = result["matches"]
        best = matches[0]
        st.markdown(f'<div class="eyebrow">ANALYSIS · {html.escape(data["name"])}</div><div class="section-title">Your career snapshot</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        for col, label, value, note in [
            (m1, "Skills detected", str(len(result["skills"])), "from the skill dictionary"),
            (m2, "Roles compared", str(len(matches)), "sample profiles"),
            (m3, "Top role", best["title"], best["category"]),
            (m4, "Relative match", f'{best["score"]:.0f}%', "not an employment probability"),
        ]:
            with col:
                st.markdown(f'<div class="card"><div class="metric-label">{label}</div><div class="metric-value" style="font-size:{"18px" if label=="Top role" else "27px"}">{html.escape(value)}</div><div class="metric-note">{html.escape(note)}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Your skill profile</div>', unsafe_allow_html=True)
        if result["skills"]:
            st.markdown(chips(result["skills"]), unsafe_allow_html=True)
        else:
            st.info("No configured skills were detected. Text-based role matching is still available.")

        st.markdown('<div class="section-title">Explore role matches</div>', unsafe_allow_html=True)
        f1, f2 = st.columns([1, 1])
        categories = ["All categories"] + sorted({m["category"] for m in matches})
        selected_category = f1.selectbox("Filter by career area", categories)
        limit = f2.select_slider("Roles to show", options=[3, 5, 8, 10], value=5)
        filtered = [m for m in matches if selected_category == "All categories" or m["category"] == selected_category][:limit]
        chart_data = pd.DataFrame([{"Role": m["title"], "Match": m["score"]} for m in filtered])
        fig = px.bar(chart_data.sort_values("Match"), x="Match", y="Role", orientation="h", range_x=[0, 100],
                     color="Match", color_continuous_scale=["#dceee4", "#176b50"])
        fig.update_layout(height=max(260, 48 * len(filtered)), margin=dict(l=0, r=12, t=10, b=5),
                          coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Relative match score (%)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
        for role in filtered:
            with st.expander(f'{role["title"]}  ·  {role["score"]:.0f}% relative match'):
                st.write(role["description"])
                left, right = st.columns(2)
                with left:
                    st.markdown("**Score breakdown**")
                    st.progress(min(role["text_similarity"] / 100, 1.0), text=f'Text similarity · {role["text_similarity"]:.0f}%')
                    st.progress(min(role["skill_coverage"] / 100, 1.0), text=f'Listed skill coverage · {role["skill_coverage"]:.0f}%')
                with right:
                    st.markdown("**Skills found**")
                    st.markdown(chips(role["matched_skills"]) or '<span style="color:#72827b">No direct skill matches</span>', unsafe_allow_html=True)
                    st.markdown("**Suggested skills**")
                    st.markdown(chips(role["missing_skills"], missing=True) or '<span style="color:#176b50">No listed gaps</span>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Your next-step skill plan</div>', unsafe_allow_html=True)
        top_gaps = best["missing_skills"][:5]
        gap_col, plan_col = st.columns([1, 1], gap="medium")
        with gap_col:
            st.markdown('<div class="card"><div class="eyebrow">TOP ROLE · '+html.escape(best["title"].upper())+'</div><h3>Skills to strengthen</h3>', unsafe_allow_html=True)
            if top_gaps:
                for skill in top_gaps:
                    st.markdown(f'<div style="display:flex;justify-content:space-between;margin:11px 0 3px"><b>{html.escape(skill)}</b><span style="color:#a35326;font-size:12px">Suggested</span></div>', unsafe_allow_html=True)
                    st.progress(0.0)
            else:
                st.success("Your resume includes every skill listed for this sample role.")
            st.markdown('</div>', unsafe_allow_html=True)
        with plan_col:
            st.markdown(f'<div class="card"><div class="eyebrow">PRACTICE IDEA</div><h3>Build evidence for your next skill</h3><p style="color:#72827b">Choose one gap, build a small project that uses it, and add a clear result and link to your resume. For {html.escape(best["title"])}, explain what you built, why you chose the method, and how you evaluated it.</p></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Interview warm-up</div>', unsafe_allow_html=True)
        st.caption(f"Practice prompts for the top suggested role: {best['title']}. These are prompts, not generated answers.")
        for question, focus in interview_prompts(best):
            with st.expander(question):
                st.write("In your answer, try to cover:")
                st.write(focus)

        export = pd.DataFrame([{
            "Role": m["title"], "Category": m["category"], "Relative match (%)": m["score"],
            "Text similarity (%)": m["text_similarity"], "Skill coverage (%)": m["skill_coverage"],
            "Matched skills": ", ".join(m["matched_skills"]), "Suggested skills": ", ".join(m["missing_skills"])
        } for m in matches])
        st.download_button("Download full role comparison (CSV)", export.to_csv(index=False).encode("utf-8"),
                           "careerlens_role_comparison.csv", "text/csv")
        st.caption("Scores compare resume content with this illustrative dataset. They are not hiring probabilities.")
