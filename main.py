from pdf2docx import Converter

# Caminho do PDF de entrada e do DOCX de saída
pdf_file = "entrada.pdf"
docx_file = "saida.docx"

# Cria o conversor
cv = Converter(pdf_file)

# Converte todo o PDF para DOCX
cv.convert(docx_file, start=0, end=None)  # start=0 (primeira página), end=None (última página)
cv.close()

print("Conversão concluída! O arquivo foi salvo como:", docx_file)