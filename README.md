# PDF to DOCX Transformation

Coleção de scripts Python para converter arquivos PDF em documentos Word (DOCX) ou LaTeX, cobrindo diferentes tipos de PDFs: nativos, escaneados e com equações matemáticas.

---

## Requisitos externos (instalar manualmente)

Antes de rodar qualquer script, instale as ferramentas abaixo no sistema:

- **Tesseract OCR**: instale em `C:\Program Files\Tesseract-OCR\`
  - Download: https://github.com/UB-Mannheim/tesseract/wiki
  - Para PDFs em português, adicione o arquivo `por.traineddata` na pasta `tessdata`

- **Poppler**: instale em `C:\poppler\Library\bin`
  - Download: https://github.com/oschwartz10612/poppler-windows/releases

---

## Configuração do ambiente Python

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (macOS/Linux)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

## Scripts disponíveis

### `main.py` — Conversão direta de PDF nativo

Converte PDFs com texto digital (não escaneados) para DOCX usando a biblioteca `pdf2docx`.

**Quando usar:** PDF gerado por computador (Word, LibreOffice, exportado digitalmente).

**Entrada:** `entrada.pdf`
**Saída:** `saida.docx`

```bash
python main.py
```

---

### `main2.py` — Conversão avançada com PyMuPDF

Converte PDFs nativos para DOCX usando `PyMuPDF (fitz)` para extração de conteúdo e `python-docx` para construção do documento. Preserva formatação (negrito, itálico, tamanho de fonte) e extrai imagens embutidas no PDF.

**Quando usar:** PDFs digitais com formatação rica ou imagens que o `main.py` não converte bem.

**Entrada:** `entrada.pdf`
**Saída:** `saida_pymupdf.docx`

```bash
python main2.py
```

---

### `main_scaner.py` — OCR para PDFs escaneados

Converte PDFs escaneados (imagens digitalizadas) para DOCX usando OCR (Tesseract). Cada página do PDF é convertida em imagem a 300 DPI e o texto é extraído via reconhecimento óptico de caracteres em português.

**Quando usar:** PDF resultante de scanner ou fotografia de documento físico.

**Dependências externas:** Tesseract OCR + Poppler

**Entrada:** `entrada_scaneada.pdf` (ou `entrada.pdf` como fallback)
**Saída:** `saida.docx`

```bash
python main_scaner.py
```

> Os caminhos do Tesseract e do Poppler são detectados automaticamente. Caso necessário, defina as variáveis de ambiente `TESSERACT_PATH` e `POPPLER_PATH`.

---

### `main_latex.py` — OCR com reconhecimento de equações matemáticas

Versão avançada para documentos acadêmicos escaneados que contêm fórmulas matemáticas. Usa Tesseract para extrair texto e `pix2tex` (LatexOCR) para converter regiões de baixa confiança em código LaTeX. Gera um arquivo `.tex` compilável.

**Quando usar:** PDFs escaneados de artigos, provas ou livros com equações matemáticas.

**Dependências externas:** Tesseract OCR + Poppler + modelo pix2tex (baixado automaticamente na primeira execução)

**Entrada:** `entrada_scaneada.pdf`
**Saída:** `saida_com_latex.tex`

```bash
python main_latex.py
```

Para compilar o arquivo LaTeX gerado em PDF:

```bash
pdflatex saida_com_latex.tex
```

> O limiar de confiança para detecção de equações é 50 (ajustável pela constante `CONFIDENCE_THRESHOLD` no arquivo).

---

## Qual script usar?

| Tipo de PDF | Script recomendado |
|---|---|
| PDF digital simples | `main.py` |
| PDF digital com imagens/formatação | `main2.py` |
| PDF escaneado (texto simples) | `main_scaner.py` |
| PDF escaneado com fórmulas matemáticas | `main_latex.py` |
