chunk_size: int = 1000
overlap: int = 200

def chunk_text(text: str):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks

def chunk_doc(document: list):
    overhang = ""
    output = []

    for text, page_nr in document:
        chunks = chunk_text(overhang + text)

        if len(chunks[-1]) < chunk_size:
            overhang = chunks.pop()
        else:
            overhang = ""

        for chunk in chunks:
            output.append((chunk, page_nr))

    if overhang:
        output.append((overhang, document[-1][1]))

    return output