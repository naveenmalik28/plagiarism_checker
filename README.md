# Flask Plagiarism Checker

The Flask Plagiarism Checker is a web application that detects plagiarism between two uploaded articles (PDF or Word documents). It compares a published article with a new submission and provides a detailed report highlighting any plagiarized sections. If plagiarism exceeds 10%, the manuscript is rejected.

## Features
- Upload two documents: one published and one new submission.
- Compare the documents for plagiarism.
- If plagiarism exceeds 10%, the new submission is rejected.
- Detailed report showing plagiarized sections.

## Technology Stack
-Backend: Python, Flask
-Frontend: HTML, CSS (for styling)
-Libraries: 
PyPDF2 for PDF extraction.
python-docx for DOCX extraction.
difflib for text comparison.
Other: Virtual environment (venv), file upload handling.

## Setup
pip install Flask sklearn PyPDF2 python-docx

### 1. Clone the repository:

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd plagiarism_checker
Run: python app.py
