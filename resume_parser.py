import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

job_roles = {
    "Data Scientist": "python machine learning data analysis pandas sklearn",
    "Web Developer": "html css javascript react flask django web development",
    "Embedded Systems Engineer": "c embedded systems microcontroller iot arduino",
}

def analyze_resume(resume_text):
    doc = nlp(resume_text.lower())
    skills = [token.text for token in doc if token.pos_ == "NOUN" or token.pos_ == "PROPN"]
    resume_keywords = " ".join(skills)

    scores = {}
    for role, keywords in job_roles.items():
        vec = TfidfVectorizer().fit_transform([resume_keywords, keywords])
        sim = cosine_similarity(vec[0:1], vec[1:2])
        scores[role] = round(float(sim[0][0]) * 100, 2)

    best_role = max(scores, key=scores.get)
    return {
        "skills": list(set(skills)),
        "matched_role": best_role,
        "confidence": scores[best_role]
    }
