
import cv2
import pytesseract
import numpy as np


path_to_tesseract = r'C:/Users/raove\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
image_path = 'text1.png'

# Opening the image & storing it in an image object
img = cv2.imread(image_path)

# Applies smoothing and sharpening
# Sharpening kernel
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Sharpen the image
blur = cv2.GaussianBlur(img, (3, 3), 0)

contrast_image = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 4)

kernel = np.array([[-1, -1, -1],
                   [-1, 9, -1],
                   [-1, -1, -1]])

simpleKernel = np.ones((3, 3), np.uint8)
sharpened_image = cv2.filter2D(contrast_image, -1, kernel)
#simplified = cv2.erode(sharpened_image, kernel, iterations=1)

# Providing the tesseract executable
# location to pytesseract library
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(sharpened_image)
print(text)
cv2.imwrite("sharpened_image.png", sharpened_image)