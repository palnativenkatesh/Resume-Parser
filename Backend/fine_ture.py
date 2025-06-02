# backend/fine_tune.py
from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments
from datasets import load_dataset, Dataset
import json
import torch

LABELS = ["O", "B-NAME", "I-NAME", "B-EMAIL", "B-PHONE", "B-SKILL", "I-SKILL"]
label2id = {l: i for i, l in enumerate(LABELS)}
id2label = {i: l for l, i in label2id.items()}

def tokenize_and_align_labels(example):
    tokenized = tokenizer(example["tokens"], is_split_into_words=True, truncation=True)
    tokenized["labels"] = [label2id[tag] for tag in example["tags"]]
    return tokenized

if __name__ == "__main__":
    tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
    model = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=len(LABELS))

    with open("dataset/resume_ner_data.json") as f:
        raw_data = json.load(f)

    dataset = Dataset.from_list(raw_data).map(tokenize_and_align_labels)
    train_test = dataset.train_test_split(test_size=0.2)

    training_args = TrainingArguments(
        output_dir="./models/resume-bert",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        evaluation_strategy="epoch",
        logging_dir="./logs",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_test["train"],
        eval_dataset=train_test["test"]
    )

    trainer.train()
    model.save_pretrained("./models/resume-bert")
    tokenizer.save_pretrained("./models/resume-bert")
