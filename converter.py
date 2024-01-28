import pytesseract
import pdf2image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import argparse
#instalar poppler

def pdf_to_img(pdf_file):
    return pdf2image.convert_from_path(pdf_file)
def txt_to_pdf(txt_file, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=LETTER)
    width, height = LETTER

    with open(txt_file, 'r') as file:
        lines = file.readlines()

    y = height - 40  # Starting Y position

    # Title font settings
    title_font = 'Times-Bold'
    title_font_size = 16  # You can adjust this size

    # Regular font settings
    regular_font = 'Times-Roman'
    regular_font_size = 12  # You can adjust this size

    for i, line in enumerate(lines):
        if i == 0:  # First line is the title
            c.setFont(title_font, title_font_size)
        else:
            c.setFont(regular_font, regular_font_size)

        c.drawString(40, y, line.strip())  # 40 is the left margin
        y -= 20  # Adjust line spacing if needed

        # Move to a new page if the text is too long for one page
        if y < 40:
            c.showPage()
            y = height - 40
            c.setFont(regular_font, regular_font_size)  # Ensure regular font on new page

    c.save()

pdf_file = 'converted_pdf.pdf'

# Convertir el TXT a PDF

def ocr_core(images):
    text = ''
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

# Especificar el path del PDF aquí
parser = argparse.ArgumentParser(description="OCR on PDF and convert text to PDF.")
parser.add_argument("pdf_path", help="Path to the input PDF file")
args = parser.parse_args()
pdf_path = args.pdf_path
# Convert your PDF to images
images = pdf_to_img(pdf_path)


# Hacer el OCR de las imágenes
extracted_text = ocr_core(images)
with open('output_text.txt', 'w') as text_file:
    text_file.write(extracted_text)

# Save the extracted text to a .txt file
txt_to_pdf(text_file.name, pdf_file)


