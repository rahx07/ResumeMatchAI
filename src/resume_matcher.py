import re
from pathlib import Path
import pandas as pd
try:
 from sklearn.feature_extraction.text import TfidfVectorizer
 from sklearn.metrics.pairwise import cosine_similarity
except ImportError: TfidfVectorizer=None;cosine_similarity=None
SKILL_ALIASES={"Python":["python"],"SQL":["sql","structured query language"],"Machine Learning":["machine learning","ml"],"Deep Learning":["deep learning"],"NLP":["nlp","natural language processing"],"PyTorch":["pytorch"],"TensorFlow":["tensorflow"],"Scikit-learn":["scikit-learn","sklearn"],"Pandas":["pandas"],"NumPy":["numpy"],"Data Visualization":["data visualization","visualization"],"Statistics":["statistics","statistical analysis"],"Power BI":["power bi"],"Tableau":["tableau"],"Excel":["excel","microsoft excel"],"Spark":["apache spark","spark"],"Hadoop":["hadoop"],"AWS":["aws","amazon web services"],"Azure":["azure","microsoft azure"],"GCP":["gcp","google cloud"],"Docker":["docker"],"Kubernetes":["kubernetes","k8s"],"Git":["git","github"],"FastAPI":["fastapi"],"Flask":["flask"],"Streamlit":["streamlit"],"React":["react","react.js","reactjs"],"JavaScript":["javascript","js"],"Java":["java"],"C++":["c++"],"C#":["c#"],"REST APIs":["rest api","restful api","apis"],"Linux":["linux"],"ETL":["etl","extract transform load"],"Data Modeling":["data modeling","data modelling"],"MLOps":["mlops","model deployment"],"Generative AI":["generative ai","llm","large language model"]}
def preprocess_text(text: str) -> str:
 text=text.lower().replace("’","'")
 return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9+#.\s]"," ",text)).strip()
def extract_skills(text: str) -> list[str]:
 n=preprocess_text(text);out=[]
 for name,aliases in SKILL_ALIASES.items():
  if any(re.search(rf"(?<![a-z0-9]){re.escape(preprocess_text(a))}(?![a-z0-9])",n) for a in aliases): out.append(name)
 return out
def load_jobs(path: str|Path) -> pd.DataFrame:
 d=pd.read_csv(path).fillna("");required={"role_id","title","category","level","description","skills"}
 if not required.issubset(d.columns) or d.empty: raise ValueError("Job dataset is empty or missing required columns.")
 return d
def _fallback(resume,descriptions):
 words=set(preprocess_text(resume).split());vals=[]
 for d in descriptions:
  other=set(preprocess_text(d).split());vals.append(len(words&other)/max(1,len(words|other)))
 top=max(vals,default=0);return [v/top for v in vals] if top else [0.0]*len(vals)
def analyze_resume(text: str,jobs: pd.DataFrame) -> dict:
 if jobs.empty: raise ValueError("No job profiles are available.")
 clean=preprocess_text(text);skills=extract_skills(text);descs=[f"{x.title} {x.category} {x.description} {x.skills}" for x in jobs.itertuples()]
 if TfidfVectorizer and clean:
  try:
   m=TfidfVectorizer(ngram_range=(1,2),stop_words="english",sublinear_tf=True).fit_transform([clean,*[preprocess_text(d) for d in descs]])
   sims=cosine_similarity(m[:1],m[1:]).ravel().tolist()
  except ValueError: sims=_fallback(clean,descs)
 else:sims=_fallback(clean,descs)
 have=set(skills);matches=[]
 for i,x in enumerate(jobs.itertuples()):
  req=[s.strip() for s in x.skills.split("|") if s.strip()];matched=[s for s in req if s in have];coverage=len(matched)/max(1,len(req));sim=float(sims[i]);score=.7*sim+.3*coverage if sim else coverage
  matches.append({"role_id":x.role_id,"title":x.title,"category":x.category,"level":x.level,"description":x.description,"score":round(score*100,1),"text_similarity":round(sim*100,1),"skill_coverage":round(coverage*100,1),"matched_skills":matched,"missing_skills":[s for s in req if s not in have]})
 matches.sort(key=lambda x:(x["score"],x["text_similarity"],x["title"]),reverse=True)
 return {"skills":skills,"matches":matches,"preprocessed_text":clean}
