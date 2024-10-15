from PIL import Image
import pytesseract

# Load the image from file

image = Image.open('images/WhatsApp Image 2024-09-27 at 13.27.10.jpeg')

# Use Tesseract to extract text
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)