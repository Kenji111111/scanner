<<<<<<< HEAD
from flask import Flask, render_template, request, send_file
import cv2 as cv
import numpy as np
from scanner import scannerize_image, convert_to_pdf
# from io import BytesIO
import uuid
=======
from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
>>>>>>> 82b66bd (Initial commit.)

app = Flask(__name__)

# Configure upload folder
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
<<<<<<< HEAD
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

            with open(f"{uuid.uuid4()}.pdf","wb") as f:
                f.write(pdf_buf.getvalue())

            print("done")

            print(type(pdf_buf))

            # return send_file(
            #     pdf_buf,
            #     as_attachment=True,
            #     download_name='name.pdf',
            #     mimetype='application/pdf'
            #     )

    return render_template('scanner.html')

# create download function for download files
@app.route('/download/<upload_id>')
def download(upload_id):
    return send_file(f"C:\\Users\\kenji\\Documents\\Code\\scanner\\{upload_id}.pdf", 
                     download_name=upload_id, mimetype='application/pdf', as_attachment=True)
=======
    # if request.method == 'POST':
    #     # Handle file upload
    #     file = request.files['file']
    #     if file:
    #         # Save the uploaded file
    #         filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #         file.save(filename)

    #         # Process the uploaded image
    #         corners = detect_corners(filename)

    #         # Pass the corner coordinates to the scanner template
    #         return render_template('scanner.html', filename=file.filename, corners=corners)

    return render_template('scanner.html')

# def detect_corners(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Use OpenCV's corner detection algorithm
#     corners = cv2.goodFeaturesToTrack(gray, 4, 0.01, 10)
#     corners = np.int0(corners)
    
#     # Extract corner coordinates
#     corner_coords = []
#     for corner in corners:
#         x, y = corner.ravel()
#         corner_coords.append((x, y))
    
#     return corner_coords
>>>>>>> 82b66bd (Initial commit.)

if __name__ == '__main__':
    app.run(debug=True)