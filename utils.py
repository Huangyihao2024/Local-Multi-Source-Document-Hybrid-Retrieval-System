import re



def chunk_text(text, chunk_size=300, overlap=50):
    text = re.sub(r'\s+', ' ', text)

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks



def extract_snippet(content, query, window=120):
    idx = content.find(query)

    if idx == -1:
        return content[:window] + "..."

    start = max(0, idx - window)
    end = min(len(content), idx + window)

    return "..." + content[start:end] + "..."