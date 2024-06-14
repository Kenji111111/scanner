from flask import Flask, render_template, request, send_file, redirect
import cv2 as cv
import numpy as np
from scanner import scannerize_image, convert_to_pdf
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if request.method == 'POST':
        # Handle file upload
        files = request.files.getlist('file')
        if files:
            images = [cv.imdecode(np.fromfile(file, np.uint8), cv.IMREAD_COLOR) for file in files]

            # Process the uploaded image
            images = [scannerize_image(image) for image in images]
            pdf_buf = convert_to_pdf(images)
            download_id = str(uuid.uuid4())

            download_name = download_id
            if len(request.form.get("output_filename")) > 0:
                download_name = request.form.get("output_filename")

            pdf_buf.seek(0)

            return send_file(pdf_buf, 
                     download_name=download_name, mimetype='application/pdf', as_attachment=True)

    return render_template('scanner.html')

if __name__ == '__main__':
    app.run(debug=True)