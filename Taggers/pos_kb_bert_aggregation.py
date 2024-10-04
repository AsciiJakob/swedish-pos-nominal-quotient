from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("KB/bert-base-swedish-cased-pos")
model = AutoModelForTokenClassification.from_pretrained("KB/bert-base-swedish-cased-pos")

# Create the pipeline for POS tagging
pos_pipeline = pipeline("token-classification", model=model, tokenizer=tokenizer, aggregation_strategy="first")



def pos_tag(sentence):
    posTags = pos_pipeline(sentence)

    output = []
    for token in posTags:
        output.append({"entity_group": token["entity_group"], "word": token["word"]})
        # print(token)
    return output
