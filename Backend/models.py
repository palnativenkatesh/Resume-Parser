from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments
from datasets import load_dataset, DatasetDict
import torch
import os

LABELS = ["O", "B-NAME", "I-NAME", "B-EMAIL", "I-EMAIL", "B-PHONE", "I-PHONE", "B-SKILL", "I-SKILL"]
label2id = {label: i for i, label in enumerate(LABELS)}
id2label = {i: label for label, i in label2id.items()}

def tokenize_and_align_labels(example):
    tokenized = tokenizer(example['tokens'], truncation=True, is_split_into_words=True)
    labels = []
    word_ids = tokenized.word_ids()
    prev_word_idx = None
    for word_idx in word_ids:
        if word_idx is None:
            labels.append(-100)
        elif word_idx != prev_word_idx:
            labels.append(label2id[example['tags'][word_idx]])
        else:
            labels.append(label2id[example['tags'][word_idx]])
        prev_word_idx = word_idx
    tokenized["labels"] = labels
    return tokenized
