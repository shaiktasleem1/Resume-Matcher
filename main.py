from flask import Flask, request, render_template
import os
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
import logging
import suggestions

app = Flask(__name__, template_folder='../templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

@app.route("/")
def matchresume():
    return render_template('matchresume.html')

@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form.get('job_description', '').strip()
        resume_files = request.files.getlist('resumes')

        # Validate job description
        if not job_description:
            return render_template('matchresume.html', message="Please enter a job description.")

        # Validate minimum number of uploaded files
        if len(resume_files) < 1: 
            return render_template('matchresume.html', message="Please upload at least 1 resume.")

        # Validate maximum number of uploaded files
        if len(resume_files) > 50:
            return render_template('matchresume.html', message="You can upload a maximum of 50 resumes at a time.")

        # Validate file types and prepare resumes text list
        resumes = []
        for resume_file in resume_files:
            filename = resume_file.filename
            if filename == '' or not allowed_file(filename):
                return render_template('matchresume.html', message=f"Unsupported file type: {filename}")
        
        for resume_file in resume_files:
            try:
                filename = secure_filename(resume_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                resume_file.save(file_path)
                text = extract_text(file_path)
                resumes.append(text)
            except Exception as e:
                logger.error(f"Error processing file {filename}: {e}")
                return render_template('matchresume.html', message=f"Failed to process file: {filename}")

        if not resumes:
            return render_template('matchresume.html', message="No valid resumes uploaded.")

        # Vectorize job description and resumes
        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()

        # Calculate cosine similarities
        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        # Get top 5 resumes and their similarity scores
        top_indices = similarities.argsort()[-5:][::-1]
        top_resumes = [resume_files[i].filename for i in top_indices]
        similarity_scores = [round(similarities[i], 2) for i in top_indices]

        # Generate suggestions for resumes with low similarity
        threshold = 0.3
        suggestions_dict = {}
        for i, score in enumerate(similarities):
            if score < threshold:
                resume_text = resumes[i]
                resume_filename = resume_files[i].filename
                suggestion_msgs = suggestions.generate_suggestions(job_description, resume_text)
                suggestions_dict[resume_filename] = suggestion_msgs

        return render_template(
            'matchresume.html',
            message="Top matching resumes:",
            top_resumes=top_resumes,
            similarity_scores=similarity_scores,
            suggestions=suggestions_dict
        )


    return render_template('matchresume.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
