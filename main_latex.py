import os
import re
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import numpy as np
from tqdm import tqdm
from pix2tex.cli import LatexOCR

# --- CONFIGURAÇÕES ---
# Caminho para o executável do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Caminho para os dados de treinamento do Tesseract
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"
# Caminho para o binário do Poppler
poppler_path = r"C:\poppler\Library\bin"
# Arquivo PDF de entrada
pdf_file = "entrada_scaneada.pdf"
# Nome do arquivo de saída LaTeX
output_latex_file = "saida_com_latex.tex"
# Limiar de confiança do OCR para decidir se um bloco é texto ou equação
# Blocos com confiança média abaixo deste valor serão tratados como equações.
CONFIDENCE_THRESHOLD = 50

# --- FUNÇÕES AUXILIARES ---

def escape_latex(text):
    """Escapa caracteres especiais do LaTeX em uma string."""
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
        '\n': r'\\',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

# --- LÓGICA PRINCIPAL ---

def main():
    print("Carregando modelo de OCR de equações (pode levar um tempo na primeira vez)...")
    try:
        model = LatexOCR()
    except Exception as e:
        print(f"Falha ao carregar o modelo LatexOCR. Verifique se a instalação do pix2tex foi bem-sucedida.")
        print(f"Detalhes: {e}")
        return

    print("Convertendo PDF para imagens (DPI=300)...")
    try:
        pages = convert_from_path(pdf_file, poppler_path=poppler_path, dpi=300)
    except Exception as e:
        print(f"Erro ao converter PDF. Verifique o caminho do Poppler e do arquivo PDF.")
        print(f"Detalhes: {e}")
        return

    latex_content = [
        r"\documentclass[a4paper,12pt]{article}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage{amsmath}",
        r"\usepackage[left=1in, right=1in, top=1in, bottom=1in]{geometry}",
        r"\begin{document}",
        r"\tolerance=9000",
        r"\hfuzz=2pt",
    ]

    print("Processando páginas e extraindo conteúdo...")
    for i, page in enumerate(tqdm(pages, desc="Páginas")):
        page_num = i + 1
        
        try:
            data = pytesseract.image_to_data(page, lang='por', output_type=pytesseract.Output.DICT)
        except Exception as e:
            print(f"Erro no Tesseract na página {page_num}: {e}")
            continue

        n_items = len(data['level'])
        if n_items == 0:
            continue

        blocks = {}
        for j in range(n_items):
            if int(data['conf'][j]) > -1 and data['text'][j].strip():
                block_num = data['block_num'][j]
                if block_num not in blocks:
                    blocks[block_num] = {'text': [], 'conf': [], 'left': [], 'top': [], 'width': [], 'height': []}
                
                blocks[block_num]['text'].append(data['text'][j])
                blocks[block_num]['conf'].append(int(data['conf'][j]))
                blocks[block_num]['left'].append(data['left'][j])
                blocks[block_num]['top'].append(data['top'][j])
                blocks[block_num]['width'].append(data['width'][j])
                blocks[block_num]['height'].append(data['height'][j])

        latex_content.append(f"\newpage % --- Página {page_num} ---")

        for block_num in sorted(blocks.keys()):
            block = blocks[block_num]
            avg_conf = np.mean(block['conf'])
            full_text = ' '.join(block['text'])

            if avg_conf < CONFIDENCE_THRESHOLD:
                try:
                    x1 = min(block['left'])
                    y1 = min(block['top'])
                    x2 = max(l + w for l, w in zip(block['left'], block['width']))
                    y2 = max(t + h for t, h in zip(block['top'], block['height']))
                    
                    margin = 5
                    bbox = (x1 - margin, y1 - margin, x2 + margin, y2 + margin)
                    cropped_image = page.crop(bbox)
                    
                    # Usar pix2tex para converter a imagem da equação em LaTeX
                    latex_eq = model(cropped_image)
                    latex_content.append(f"$$ {latex_eq} $$")

                except Exception as e:
                    print(f"Falha ao processar bloco {block_num} como equação na página {page_num}: {e}")
                    latex_content.append(escape_latex(full_text) + r"\\")
            else:
                latex_content.append(escape_latex(full_text) + r"\\")

    latex_content.append(r"\end{document}")

    try:
        with open(output_latex_file, "w", encoding="utf-8") as f:
            f.write("\n".join(latex_content))
        print(f"\n✅ Conversão para LaTeX concluída!")
        print(f"   Arquivo salvo como: '{output_latex_file}'")
        print(f"\nPara gerar o PDF, execute um compilador LaTeX, por exemplo:")
        print(f"pdflatex {output_latex_file}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo LaTeX: {e}")

if __name__ == "__main__":
    main()
