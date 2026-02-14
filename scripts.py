import pdfplumber
import spacy 

import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:              # 🔐 important
                text += page_text + "\n"
    return text                       
#htis is a commentsfas
#htis is a comment
