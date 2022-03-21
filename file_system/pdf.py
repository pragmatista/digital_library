import pdfminer.pdfparser
import pdfplumber


def extract_text(path: str):
    try:
        with pdfplumber.open(r'' + path) as pdf:
            # total_pages = pdf.pages.count()
            # print(f"{path} | {total_pages}")

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
    except pdfminer.pdfparser.PDFSyntaxError as e:
        print(f"{path} | Error: {e}")


