# app.py
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pdf_converter import convert_pdf_to_flipbook
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if pdf_file and allowed_file(pdf_file.filename):
            filename = secure_filename(pdf_file.filename)
            output_dir = os.path.join('static', 'flipbook')
            os.makedirs(output_dir, exist_ok=True)
            pdf_file.save(os.path.join(output_dir, filename))
            flipbook_pages = convert_pdf_to_flipbook(os.path.join(output_dir, filename), output_dir)
            return render_template('flipbook.html', flipbook_pages=flipbook_pages)
        else:
            flash('Invalid file type, please upload a PDF file')
            return redirect(request.url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
#flask run --host=0.0.0.0