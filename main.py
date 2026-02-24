from pdf2docx import Converter
import os

# --- CONFIGURAÇÕES ---
# Caminho do PDF de entrada e do DOCX de saída
pdf_file = "entrada.pdf"
docx_file = "saida.docx"


def convert_pdf_to_docx(pdf_path, docx_path):
    """
    Converte um arquivo PDF para DOCX, com tratamento de erros.
    """
    if not os.path.exists(pdf_path):
        print(f"Erro: O arquivo de entrada '{pdf_path}' não foi encontrado.")
        return

    print(f"Iniciando a conversão de '{pdf_path}' para '{docx_path}'...")

    try:
        # Cria o objeto conversor
        cv = Converter(pdf_path)

        # Converte o PDF para DOCX.
        # start=0 significa que a conversão começa da primeira página.
        # end=None significa que a conversão vai até a última página.
        cv.convert(docx_path, start=0, end=None)

        # Fecha o objeto conversor
        cv.close()

        print(f"✅ Conversão concluída! O arquivo foi salvo como: '{docx_path}'")

    except Exception as e:
        print(f"❌ Ocorreu um erro durante a conversão: {e}")
        print("   - Verifique se o PDF não está corrompido ou protegido por senha.")
        print("   - Para PDFs escaneados, este script não funcionará bem. Veja o 'main_scaner.py'.")
        print("   - Para PDFs com muitas fórmulas, o 'main_latex.py' pode ser uma alternativa.")

if __name__ == "__main__":
    convert_pdf_to_docx(pdf_file, docx_file)

# --- PRÓXIMOS PASSOS ---
# Se o resultado ainda não for o ideal, podemos tentar abordagens mais avançadas:
#
# 1. **PyMuPDF (fitz):** É uma biblioteca mais poderosa para extrair dados de PDFs.
#    Poderíamos usar o PyMuPDF para extrair texto, imagens e tabelas com suas
#    posições exatas na página e então reconstruir o documento DOCX do zero.
#    Isso dá mais controle, mas é um processo bem mais complexo.
#
# 2. **Análise de Layout:** Para PDFs muito complexos, existem algoritmos de
#    análise de layout que podem ser usados para identificar colunas, parágrafos, etc.

