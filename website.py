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
            print("got some files")

            print(files)

            # np_images = [np.fromfile(file, np.uint8) for file in files]

            images = [cv.imdecode(np.fromfile(file, np.uint8), cv.IMREAD_COLOR) for file in files]

            # Process the uploaded image
            images = [scannerize_image(image) for image in images]
            pdf_buf = convert_to_pdf(images)

            download_id = str(uuid.uuid4())

            with open(f"{download_id}.pdf","wb") as f:
                f.write(pdf_buf.getvalue())

            print("done")

            print(type(pdf_buf))

            # return redirect(f'/download/{download_id}')
            return send_file(f"C:\\Users\\kenji\\Documents\\Code\\scanner\\{download_id}.pdf", 
                     download_name=download_id, mimetype='application/pdf', as_attachment=True)

    return render_template('scanner.html')

if __name__ == '__main__':
    app.run(debug=True)