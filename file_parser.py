import os
import fitz
import docx


def extract_text_from_pdf(file_path):
    text = ""

    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()

    except:
        return ""

    return text


def extract_text_from_docx(file_path):

    try:
        doc = docx.Document(file_path)

        return "\n".join(
            [para.text for para in doc.paragraphs]
        )

    except:
        return ""


def extract_text_from_txt(file_path):

    try:
        with open(
            file_path,
            'r',
            encoding='utf-8',
            errors='ignore'
        ) as f:

            return f.read()

    except:
        return ""


def parse_file(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        return extract_text_from_pdf(file_path)

    elif ext == '.docx':
        return extract_text_from_docx(file_path)

    elif ext in ['.txt', '.md', '.py', '.csv']:
        return extract_text_from_txt(file_path)

    return ""