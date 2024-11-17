from pdfminer.high_level import extract_text 

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Parameters
    ----------
    pdf_path : str
        Path to the PDF file

    Returns
    -------
    str
        Extracted text
    """
    
    return extract_text(pdf_path)