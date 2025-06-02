import textract

def extract_text_from_file(filename, content):
    with open(f"/tmp/{filename}", "wb") as f:
        f.write(content)
    return textract.process(f"/tmp/{filename}").decode("utf-8")
