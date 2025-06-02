from transformers import BertTokenizerFast, BertForTokenClassification
import torch
import re
from app.utils import extract_text_from_file

model = BertForTokenClassification.from_pretrained("./models/resume-bert")
tokenizer = BertTokenizerFast.from_pretrained("./models/resume-bert")
model.eval()

id2label = model.config.id2label

def parse_resume(filename: str, content: bytes):
    text = extract_text_from_file(filename, content)
    tokens = tokenizer.tokenize(text)
    inputs = tokenizer.encode(text, return_tensors="pt")
    outputs = model(inputs).logits
    predictions = torch.argmax(outputs, dim=2)[0].numpy()
    labels = [id2label[pred] for pred in predictions]

    result = {"name": [], "email": [], "phone": [], "skills": []}
    for token, label in zip(tokenizer.convert_ids_to_tokens(inputs[0]), labels):
        if label.endswith("NAME"):
            result["name"].append(token)
        elif label.endswith("EMAIL"):
            result["email"].append(token)
        elif label.endswith("PHONE"):
            result["phone"].append(token)
        elif label.endswith("SKILL"):
            result["skills"].append(token)
    return result
