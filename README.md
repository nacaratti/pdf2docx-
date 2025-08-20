# PDF to DOCX Transformation

This repository contains scripts to convert PDF files, including scanned documents and those with LaTeX content, into DOCX format.

To convert text .pdf documents in .docx >> main.py
To convert scanned .pdf documents in .docx >> main_scaner.py
To convert text/scanned .pdf documents in Latex >> main_latex.py

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
2.  **Activate the virtual environment:**
    -   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file is not yet present in this repository. It should be created based on the libraries in the `venv` directory.)*

4.   ** Tesseract Settings**
      You need to install Tesseract on your PC >> https://github.com/UB-Mannheim/tesseract/wiki
      After installation, point to the file https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata in the tessdata folder where the program was installed on your PC
     
6.   **Poppler**
      Caminho do Poppler >> https://github.com/oschwartz10612/poppler-windows/releases/


## Usage

1.  Place your input PDF file in the root directory and name it `entrada_scaneada.pdf`.
2.  Run the main script:
    ```bash
    python main.py
    ```
3.  The output will be saved as `saida.docx`.
