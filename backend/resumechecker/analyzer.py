import re
import spacy
import pdfplumber

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load NLP model
nlp = None

def get_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")
    return nlp



# ---------------------------------------------------
# TECHNICAL SKILL MASTER LIST
# ---------------------------------------------------
TECH_SKILLS = {
    # Languages
    "python", "java", "javascript", "typescript",
    "c", "c++", "c#", "go", "rust", "kotlin", "swift", "php", "ruby",
    # Web frameworks
    "django", "flask", "fastapi",
    "react", "angular", "vue", "next.js", "nuxt",
    "node", "express", "spring boot",
    # Databases
    "sql", "mysql", "postgresql", "sqlite",
    "mongodb", "nosql", "redis", "elasticsearch",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes",
    "ci/cd", "terraform", "ansible",
    # Tools & protocols
    "git", "rest", "graphql", "grpc",
    "html", "css",
    # CS fundamentals
    "oop", "data structures", "algorithms",
    "system design", "microservices",
    # ML / Data
    "machine learning", "deep learning", "pandas",
    "numpy", "scikit-learn", "tensorflow", "pytorch",
    "backend", "frontend",
}

# Skills whose special characters must survive cleaning
# Map: canonical name → regex pattern to match in raw (lowercased) text
_SPECIAL_SKILL_PATTERNS = {
    "c++":  r"c\+\+",
    "c#":   r"c#",
}


# ---------------------------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ---------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------
def clean_text(text: str) -> str:
    """Lower-case and normalise whitespace.
    Keeps alphanumeric, space, forward-slash, plus, hash so that
    skills like c++, c#, ci/cd survive intact.
    """
    text = text.lower()
    text = text.replace("\r", " ").replace("\n", " ")
    # BUG FIX: keep +  and  # so c++ / c# are not destroyed
    text = re.sub(r"[^a-z0-9\s/+#.]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------------------------------------------
# EXTRACT TECH SKILLS FROM TEXT
# ---------------------------------------------------
def extract_tech_skills(text: str) -> list:
    lower_raw = text.lower()             # for special-char skills
    cleaned   = clean_text(text)         # for normal skills

    # Common aliases
    cleaned = cleaned.replace("sql/nosql", "sql nosql")
    cleaned = cleaned.replace("restful",   "rest")
    cleaned = cleaned.replace("node.js",   "node")
    cleaned = cleaned.replace("react.js",  "react")

    found = set()

    # Special-character skills: match against raw lowercased text
    for skill, pattern in _SPECIAL_SKILL_PATTERNS.items():
        if re.search(pattern, lower_raw):
            found.add(skill)

    # All other skills: match against cleaned text
    normal_skills = TECH_SKILLS - set(_SPECIAL_SKILL_PATTERNS.keys())
    for skill in normal_skills:
        # Both single-word and multi-word use the same boundary logic;
        # the dead duplicate branch has been removed.
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, cleaned):
            found.add(skill)

    return sorted(found)


# ---------------------------------------------------
# PREPROCESS FOR TF-IDF
# ---------------------------------------------------
def preprocess_text(text: str) -> str:
    text = clean_text(text)
    nlp_model = get_nlp()
    doc = nlp_model(text)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and token.lemma_.strip()
    ]
    return " ".join(tokens)


# ---------------------------------------------------
# SIMILARITY CALCULATION
# ---------------------------------------------------
def calculate_similarity(resume_text: str, job_text: str) -> dict:

    # ---- TF-IDF ----
    resume_clean = preprocess_text(resume_text)
    job_clean    = preprocess_text(job_text)

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors    = vectorizer.fit_transform([resume_clean, job_clean])

    tfidf_score = float(
        cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    ) * 100

    # ---- Skill match ----
    resume_skills = set(extract_tech_skills(resume_text))
    job_skills    = set(extract_tech_skills(job_text))

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    skill_score = (len(matched) / len(job_skills) * 100) if job_skills else 0.0

    # ---- Weighted final score ----
    final_score = round(0.4 * tfidf_score + 0.6 * skill_score, 2)

    return {
        "score":            final_score,
        "tfidf_score":      round(tfidf_score, 2),
        "skill_score":      round(skill_score, 2),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "suggestions":      generate_suggestions(missing),
    }


# ---------------------------------------------------
# SUGGESTION ENGINE
# ---------------------------------------------------
def generate_suggestions(missing_skills: list) -> list:
    suggestions = [
        f"Consider adding hands-on experience with {skill}."
        for skill in missing_skills[:5]
    ]
    if len(missing_skills) > 5:
        suggestions.append(
            "Your resume is missing several key technologies from the job "
            "description. Review the full list above and prioritise the most "
            "common ones first."
        )
    return suggestions