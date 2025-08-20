import os
from pdf2image import convert_from_path
from docx import Document
from docx.shared import Inches
import pytesseract
from tqdm import tqdm

# -------------------------------
# Configurações do Tesseract >> Precisa instalar o tesseract no pc
# https://github.com/UB-Mannheim/tesseract/wiki
# Depois de instalar, adicinar o arquivo https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata na pasta tessdata onde o programa foi instalado no pc
# -------------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# -------------------------------
# Caminho do Poppler
# https://github.com/oschwartz10612/poppler-windows/releases/
# -------------------------------
poppler_path = r"C:\poppler\Library\bin"  # Ajuste para onde está seu Poppler

# -------------------------------
# PDF de entrada
# -------------------------------
pdf_file = "entrada_scaneada.pdf"

# -------------------------------
# Converter PDF em imagens
# -------------------------------
pages = convert_from_path(pdf_file, poppler_path=poppler_path)

# -------------------------------
# Criar documento Word
# -------------------------------
doc = Document()

for i, page in enumerate(tqdm(pages, desc="Processando páginas")):
    # Fazer OCR da imagem
    text = pytesseract.image_to_string(page, lang="por")
    doc.add_paragraph(f"Página {i+1}")
    doc.add_paragraph(text)
    doc.add_page_break()

# -------------------------------
# Salvar como DOCX
# -------------------------------
doc.save("saida.docx")

print("✅ Conversão concluída! O texto e imagens foram salvos em saida.docx")
