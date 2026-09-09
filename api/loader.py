from pathlib import Path
from pypdf import PdfReader

def load_all_pdfs(directory: str):

    output = []

    for pdf_path in Path(directory).glob("*.pdf"):
        
        document = load_pdf(pdf_path)
        
        output.append((
            pdf_path.name,
            document
        ))

    return output

    
def load_pdf(path: Path):

    reader = PdfReader(path)
    document = []

    for page_number, page in enumerate(reader.pages, start=1):
        
        text = page.extract_text() or ""
        
        page = (
        text,
        page_number
        )

        document.append(page)

    return document