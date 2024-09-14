import os
import re
import docx
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from difflib import SequenceMatcher

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to calculate plagiarism percentage
def calculate_plagiarism(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio() * 100

# Function to find plagiarized sections
def find_plagiarized_sections(text1, text2):
    matcher = SequenceMatcher(None, text1, text2)
    matching_blocks = matcher.get_matching_blocks()
    
    plagiarized_content = []
    for block in matching_blocks:
        if block.size > 0:
            plagiarized_content.append(text1[block.a:block.a + block.size])
    
    return plagiarized_content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if both files are uploaded
        published_file = request.files.get('published_article')
        new_file = request.files.get('new_submission')

        if published_file and new_file and allowed_file(published_file.filename) and allowed_file(new_file.filename):
            published_filename = secure_filename(published_file.filename)
            new_filename = secure_filename(new_file.filename)

            published_file_path = os.path.join(app.config['UPLOAD_FOLDER'], published_filename)
            new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

            published_file.save(published_file_path)
            new_file.save(new_file_path)

            # Extract text from both files
            if published_file.filename.endswith('.pdf'):
                published_text = extract_text_from_pdf(published_file_path)
            else:
                published_text = extract_text_from_docx(published_file_path)

            if new_file.filename.endswith('.pdf'):
                new_text = extract_text_from_pdf(new_file_path)
            else:
                new_text = extract_text_from_docx(new_file_path)

            # Calculate plagiarism percentage
            plagiarism_percentage = calculate_plagiarism(published_text, new_text)

            # Find plagiarized sections
            plagiarized_content = find_plagiarized_sections(published_text, new_text)

            if plagiarism_percentage > 10:
                flash(f'Rejected: Plagiarism detected ({plagiarism_percentage:.2f}%)')
                return render_template('index.html', plagiarism_percentage=plagiarism_percentage, plagiarized_content=plagiarized_content, rejected=True)
            else:
                flash(f'Accepted: Plagiarism is within limits ({plagiarism_percentage:.2f}%)')
                return render_template('index.html', plagiarism_percentage=plagiarism_percentage, plagiarized_content=None, rejected=False)
        else:
            flash('Please upload both a published article and a new submission in PDF or DOCX format.')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, port=5001)
