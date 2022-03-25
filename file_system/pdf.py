import pdfplumber


def extract_text_from_pdf(path: str):
    try:
        with pdfplumber.open(f'{path}') as pdf:
            results = []

            for idx, page in enumerate(pdf.pages):
                data = {
                    'file': path,
                    'total_pages': len(pdf.pages),
                    'page': idx + 1,
                    'text': page.extract_text()
                }

                results.append(data)

            return results
    except pdfplumber.pdf.PDFParser as e:
        print(f"{path} | Error: {e}")


