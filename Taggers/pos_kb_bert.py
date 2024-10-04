from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("KB/bert-base-swedish-cased-pos")
model = AutoModelForTokenClassification.from_pretrained("KB/bert-base-swedish-cased-pos")

# Create the pipeline for POS tagging
pos_pipeline = pipeline("token-classification", model=model, tokenizer=tokenizer, aggregation_strategy="none")



def pos_tag(sentence):
    output = []
    current_word = ""
    current_entity = ""
    current_start = None
    current_end = None

    for token in pos_pipeline(sentence):
        word = token["word"]
        entity = token["entity"]
        start = token["start"]
        end = token["end"]
        
        # If the word starts with '##', it's a subword and should be appended to the previous word
        if word.startswith("##"):
            current_word += word[2:]  # Add subword part to the current word (excluding '##')
            current_end = end  # Update the end position
        else:
            # If we already have a current word, append it to the output before starting a new one
            if current_word:
                output.append({
                    "entity_group": current_entity,
                    "word": current_word,
                    "start": current_start,
                    "end": current_end
                })
            # Start a new word
            current_word = word
            current_entity = entity
            current_start = start
            current_end = end
    
    # Append the last word after finishing the loop
    if current_word:
        output.append({
            "entity_group": current_entity,
            "word": current_word,
            "start": current_start,
            "end": current_end
        })

    return output