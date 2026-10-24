import unittest
from io import BytesIO
from pathlib import Path
from docx import Document
from src.resume_matcher import analyze_resume,extract_skills,load_jobs
from src.resume_parser import extract_resume_text,ResumeParseError
ROOT=Path(__file__).resolve().parents[1]
class MatcherTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.jobs=load_jobs(ROOT/"data"/"jobs.csv")
 def test_txt_parse(self): self.assertEqual(extract_resume_text("a.txt",b"Python SQL"),"Python SQL")
 def test_docx_parse(self):
  d=Document();d.add_paragraph("Python and SQL");buf=BytesIO();d.save(buf)
  self.assertIn("Python and SQL",extract_resume_text("resume.docx",buf.getvalue()))
 def test_unsupported_type(self):
  with self.assertRaises(ResumeParseError):extract_resume_text("resume.rtf",b"text")
 def test_aliases(self):
  got=extract_skills("natural language processing, Python, Power BI")
  self.assertIn("NLP",got);self.assertIn("Python",got);self.assertIn("Power BI",got)
 def test_ranked_and_explained(self):
  x=analyze_resume("Python SQL machine learning pandas statistics scikit-learn data visualization",self.jobs);s=[a["score"] for a in x["matches"]]
  self.assertEqual(s,sorted(s,reverse=True));self.assertIn("missing_skills",x["matches"][0])
 def test_zero_overlap(self):
  x=analyze_resume("xyzzy quux foobar",self.jobs);self.assertTrue(all(0<=a["score"]<=100 for a in x["matches"]))
if __name__=="__main__":unittest.main()
