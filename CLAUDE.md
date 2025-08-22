# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a PDF to DOCX transformation project with multiple conversion approaches:
- Basic PDF conversion using `pdf2docx`
- OCR-based conversion for scanned documents
- LaTeX-aware OCR for mathematical content

## Setup Commands

Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Main Scripts

- **main.py**: Simple PDF to DOCX conversion using pdf2docx library
- **main_scaner.py**: OCR-based conversion for scanned PDFs to DOCX
- **main_latex.py**: Advanced OCR with LaTeX equation recognition for academic documents

## Dependencies

The project uses several specialized libraries:
- `pdf2docx`: Direct PDF conversion
- `pytesseract`: OCR text extraction
- `pix2tex`: LaTeX equation recognition from images
- `pdf2image`: PDF to image conversion
- `python-docx`: DOCX document creation

## External Requirements

- **Tesseract OCR**: Must be installed at `C:\Program Files\Tesseract-OCR\`
- **Poppler**: Required for PDF processing, expected at `C:\poppler\Library\bin`
- **Portuguese OCR data**: `por.traineddata` file in Tesseract's tessdata directory

## Input/Output Files

- Input PDF: `entrada_scaneada.pdf` (for OCR scripts) or `entrada.pdf` (for basic conversion)
- Output: `saida.docx` (Word document) or `saida_com_latex.tex` (LaTeX file)

## Architecture Notes

The OCR scripts use a block-based approach:
1. Convert PDF pages to high-resolution images (300 DPI)
2. Use Tesseract to identify text blocks and confidence scores
3. Low-confidence blocks are processed as potential equations using pix2tex
4. Results are assembled into structured documents

The confidence threshold for equation detection is set to 50 in `main_latex.py`.