from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json
import torch

tokenizer = AutoTokenizer.from_pretrained("KB/bert-base-swedish-cased-pos")
model = AutoModelForTokenClassification.from_pretrained("KB/bert-base-swedish-cased-pos")


useDevice = 0 if torch.cuda.is_available() else -1 # Use GPU if available
pos_pipeline = pipeline("token-classification", model=model, tokenizer=tokenizer, device=useDevice, aggregation_strategy="none")

def merge_hyphenated_words(sentence):
    output = []
    skip_tokens = 0

    for i, token in enumerate(sentence):
        if (skip_tokens > 0):
            skip_tokens -= 1
            continue
        if (token["word"] == '-'):
            word_before = sentence[i-1]
            word_after = sentence[i+1]
            if (word_before["pos"] == "NN" and word_after["pos"] == "NN"):
                word_before["word"] += "-"+word_after["word"]
                skip_tokens = 1
                continue
        output.append(token)

    return output

def pos_tag(sentence):
    output = []

    pos_tokens = pos_pipeline(sentence)
    last_added_token = ""

    # merge subwords (tokens that are part of the same word have "##" as a prefix to them)
    for i, token in enumerate(pos_tokens):
        word = token["word"]
        if word.startswith("##") and i != 0:
            last_added_token["word"] += word[2:]
        else:
            output.append({
                "pos": token["entity"],
                "word": word
            })
            last_added_token = output[-1] # last element in array
    

    output = merge_hyphenated_words(output)

    return output