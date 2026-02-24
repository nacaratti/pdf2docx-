import os
import sys
from pathlib import Path
from pdf2image import convert_from_path
from docx import Document
from docx.shared import Inches
import pytesseract
from tqdm import tqdm

def setup_tesseract():
    
    """Configure Tesseract OCR paths with fallback options."""
    tesseract_path = os.environ.get('TESSERACT_PATH')
    if not tesseract_path:
        # Common installation paths
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract"
        ]
        for path in common_paths:
            if os.path.exists(path):
                tesseract_path = path
                break
    
    if not tesseract_path or not os.path.exists(tesseract_path):
        raise FileNotFoundError(
            "Tesseract not found. Install from https://github.com/UB-Mannheim/tesseract/wiki "
            "or set TESSERACT_PATH environment variable"
        )
    
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # Set tessdata path
    tessdata_path = os.environ.get('TESSDATA_PREFIX')
    if not tessdata_path:
        tesseract_dir = os.path.dirname(tesseract_path)
        tessdata_path = os.path.join(tesseract_dir, "tessdata")
    
    if os.path.exists(tessdata_path):
        os.environ["TESSDATA_PREFIX"] = tessdata_path
    
    return tesseract_path

def get_poppler_path():
    """Get Poppler path with fallback options."""
    poppler_path = os.environ.get('POPPLER_PATH')
    if not poppler_path:
        common_paths = [
            r"C:\poppler\Library\bin",
            r"C:\Program Files\poppler\bin",
            "/usr/bin",
            "/usr/local/bin"
        ]
        for path in common_paths:
            if os.path.exists(path):
                poppler_path = path
                break
    
    return poppler_path

def get_input_file():
    """Get input PDF file path with validation."""
    pdf_file = os.environ.get('INPUT_PDF', 'entrada_scaneada.pdf')
    
    if not os.path.exists(pdf_file):
        # Try common variations
        alternatives = ['entrada.pdf', 'input.pdf', 'document.pdf']
        for alt in alternatives:
            if os.path.exists(alt):
                pdf_file = alt
                break
        else:
            raise FileNotFoundError(f"PDF file not found: {pdf_file}")
    
    return pdf_file

def process_pdf_to_docx(pdf_file, output_file="saida.docx", language="por", dpi=300):
    """Convert PDF to DOCX using OCR."""
    poppler_path = get_poppler_path()
    
    print(f"Converting PDF '{pdf_file}' to images (DPI={dpi})...")
    try:
        pages = convert_from_path(pdf_file, poppler_path=poppler_path, dpi=dpi)
    except Exception as e:
        raise RuntimeError(f"Failed to convert PDF to images: {e}")
    
    print("Creating Word document...")
    doc = Document()

    for i, page in enumerate(tqdm(pages, desc="Processing pages")):
        try:
            # OCR with error handling
            text = pytesseract.image_to_string(page, lang=language)

            # Clean up text
            text = text.strip()

            # Add page content
            if text:
                doc.add_paragraph(text)
            
            # Add page break except for last page
            if i < len(pages) - 1:
                doc.add_page_break()
                
        except Exception as e:
            print(f"Warning: Error processing page {i+1}: {e}")
    
    try:
        doc.save(output_file)
        print(f"✅ Conversion completed! Document saved as: {output_file}")
        return output_file
    except Exception as e:
        raise RuntimeError(f"Failed to save document: {e}")

def main():
    """Main execution function."""
    try:
        # Setup
        print("Setting up Tesseract OCR...")
        tesseract_path = setup_tesseract()
        print(f"Using Tesseract: {tesseract_path}")
        
        # Get input file
        pdf_file = get_input_file()
        print(f"Input PDF: {pdf_file}")
        
        # Process
        output_file = process_pdf_to_docx(pdf_file)
        
        # Summary
        file_size = os.path.getsize(output_file) / 1024  # KB
        print(f"\n📄 Output file size: {file_size:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
