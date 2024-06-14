import numpy as np
import cv2 as cv
import img2pdf
from PyPDF2 import PdfMerger
from io import BytesIO
from math import floor, sqrt

def extract_page(image):
    if image.shape[0] / image.shape[1] != 4 / 3:
        raise Exception("cannot do this right now. Need a 4:3 vertical image.")
        return -1
    
    scale = image.shape[1] / 600

    #### Detect shape and transform 
    imS = cv.resize(image, (600, 800))
    blurred_image = cv.GaussianBlur(imS,ksize=(15,15), sigmaX=0)
    gray = cv.cvtColor(blurred_image, cv.COLOR_BGR2GRAY)

    # Canny edge detection
    edged = cv.Canny(gray, 50, 150, apertureSize=5, L2gradient=True) 

    # Contour detect. Need canny edges to get B&W
    contours, _ = cv.findContours(edged,  
        cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 
    
    c = max(contours, key = cv.contourArea)

    # Draw the biggest contour
    # cv.drawContours(imS, [c], -1, (0,255,0), 3)

    epsilon = 0.1*cv.arcLength(c,True)
    pts1 = np.float32(np.squeeze(cv.approxPolyDP(c,epsilon,True)) * scale)
    # cv.drawContours(image, [np.expand_dims(pts1, 0).astype(np.int32)], -1, (255, 0, 0), 3)

    # Corners have to be in the different quadrants of the image. 

    original_shape = (image.shape[0], floor(image.shape[0] * sqrt(2)))

    pts2 = np.float32(np.round(pts1 / original_shape) * original_shape)

    M = cv.getPerspectiveTransform(pts1, pts2)
    warped = cv.warpPerspective(image,M,original_shape)

    return warped

def sharpen(image):
    blurred_image = cv.GaussianBlur(image,ksize=(15,15), sigmaX=0)
    blurred_image = cv.addWeighted(blurred_image, 1.5, blurred_image, -0.5, 0)

    return blurred_image


def convert_to_pdf(images):
    pdf_buffer = BytesIO()
    pdf_merger = PdfMerger()

    for image in images:
        is_success, b = cv.imencode('.png', image)

        if not is_success:
            return -1
        
        buf = BytesIO(b)
        
        a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
        layout_fun = img2pdf.get_layout_fun(a4inpt)
        img_pdf_bytes = img2pdf.convert(buf.getvalue(), layout_fun=layout_fun)

        with open("name.png","wb") as f:
            f.write(buf.getvalue())
        
        pdf_merger.append(BytesIO(img_pdf_bytes))

    pdf_merger.write(pdf_buffer)
    

    return pdf_buffer

def scannerize_image(image):

    warped = extract_page(image)
    # sharpened = sharpen(warped)
    
    #### Sharpen
    
    # imS = cv.resize(image, (600, 800))
    # cv.imshow('Contours', imS) 
    # cv.waitKey(0)

    # imS = cv.resize(warped, (600, 800))
    # cv.imshow('Contours', imS)

    cv.waitKey(0)
    cv.destroyAllWindows()

    return warped

if __name__ =="__main__":
    filenames = ['img_1290.jpg', 'img_1298.jpg']

    images = [cv.imread(filename) for filename in filenames]

    scanned = [scanerize_image(image) for image in images]

    b = convert_to_pdf(scanned)
    
    with open("name.pdf","wb") as f:
        f.write(b.getvalue())