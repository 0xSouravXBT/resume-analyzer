from flask import Flask, render_template, request
from resume_parser import analyze_resume

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    if request.method == 'POST':
        resume_text = request.form['resume']
        analysis = analyze_resume(resume_text)
    return render_template('index.html', analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)
