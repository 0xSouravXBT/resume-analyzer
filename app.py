import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import docx
import re

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

RECOMMENDED_SKILLS = [
    "python", "java", "c++", "html", "css", "javascript", "react", "node.js",
    "sql", "aws", "azure", "django", "flask", "machine learning", "data science",
    "problem solving", "project management", "leadership", "tally", "lozics",
    "ms word", "ms excel", "petty cash", "data entry", "accounting", "cash handling",
    "document handling", "teamwork", "communication"
]

def allowed_file(fn):
    return fn and '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(fp):
    ext = fp.rsplit('.', 1)[1].lower()
    text = ""
    try:
        if ext == 'pdf':
            imgs = convert_from_path(fp)
            for img in imgs:
                text += pytesseract.image_to_string(img)
        elif ext in {'jpg', 'jpeg', 'png'}:
            text = pytesseract.image_to_string(Image.open(fp))
        elif ext == 'docx':
            doc = docx.Document(fp)
            text = "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        print("Extraction error:", e)
    return text

def analyze(text):
    low = text.lower()
    words = re.findall(r'\w+', low)
    wc = len(words)
    det = list({skill for skill in RECOMMENDED_SKILLS if skill in low})
    score = int(len(det) / len(RECOMMENDED_SKILLS) * 100)
    level = "High" if score >= 70 else "Medium" if score >= 40 else "Low"
    return wc, det, score, level

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    extracted = ""
    filename = ""
    if request.method == 'POST':
        file = request.files.get('resume')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fp = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fp)
            extracted = extract_text(fp)
            wc, det, score, lvl = analyze(extracted)
            analysis = {
                'word_count': wc,
                'detected_skills': det,
                'recommended_skills': RECOMMENDED_SKILLS,
                'score': score,
                'level': lvl
            }
    return render_template('index.html', filename=filename,
                           extracted_text=extracted, analysis=analysis)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
