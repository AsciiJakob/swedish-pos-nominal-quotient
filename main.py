from segmentation import segmentize_to_sentences
from parsing import parse_file, get_folder_docx_files
from sheet import generate_sheets
from filtering import filter_sentences
import metrics as metrics
import json
import sys
import time
import importlib

available_models = ["flair", "kb_bert", "kb_bert_aggregation", "kb_bert_test"]

selected_model = ["kb_bert"] # set default model
if (len(sys.argv) > 1):
    selected_model = sys.argv[1].split(",")
    if (selected_model[0] == "all"):
        selected_model = available_models

for model_index, current_model in enumerate(selected_model):
    print("Attempting to load model", current_model)
    try:
        POSModule = importlib.import_module("Taggers.pos_"+current_model)
        print("Loaded model "+current_model)
    except:
        print("failed to load POS library called: "+current_model)
        exit(1)
    timestamp_start = time.time()


    docx_files = get_folder_docx_files("input/")
    output = []
    for file_index, texts_file in enumerate(docx_files):
        texts = parse_file(texts_file["fullPath"])
        output.append({"filename": texts_file["filename"], "texts": []})
        for text_index, text in enumerate(texts):
            print(f"Processing, model: [{model_index+1}/{len(selected_model)}] file: {texts_file["filename"]} [{file_index+1}/{len(docx_files)}] text: [{text_index+1}/{len(texts)}]", end='\r')

            sentence_aggregation = []

            sentences = segmentize_to_sentences(text["text_marked_italics"])
            for sentence in sentences:
                sentence_aggregation.append(POSModule.pos_tag(sentence))

            # Apply filtering to remove words in quotes, parenthesis or italics.
            # Also removes <italics> tags from the text so they don't distrub metrics, we only need that information if we're filtering italics out.
            filtered_sentences = filter_sentences(sentence_aggregation, True, True, True)

            nominal_quotient = metrics.nominal_quotient(filtered_sentences)
            word_count = len(text["text_raw"].split())

            output[file_index]["texts"].append({
                "id": text["id"],
                "full_nominal_quotient": nominal_quotient["full"],
                "simple_nominal_quotient": nominal_quotient["simple"],
                "word_count": word_count,
                "mean_sentence_length": word_count/len(sentences),
                "sentences": sentence_aggregation, # this and filtered_sentences are only used for the visualizing tool so you can remove these if don't care about that and want to save storage i suppose
                "filtered_sentences": filtered_sentences,
                "quote_char_count": text["text_raw"].count('"'),
                "quote_ratio": metrics.quote_ratio(text["text_raw"]),
                "LIX": metrics.LIX(word_count, len(sentences), filter_sentences(sentence_aggregation, False, False, False)) # we're using filter_sentences just so "{ITALICS}" things are removed
            })

        print(f"Model {current_model} finished processing file {texts_file["filename"]}.docx in {round(time.time()-timestamp_start, 2)} seconds\n")

    with open("output/computed_"+current_model+".json", "w") as json_file:
        json.dump(output, json_file, indent=4)  # "indent" for pretty-printing

# we can't load .json from web javascript since we're just opening a file without running a webserver, hence we're exporting the json data to a js file.
with open("Visualizer/computed_compilation.js", "w") as js_file:
    js_file.write("const dataFile = {};\n")
    for i, model in enumerate(available_models):
        try:
            with open("output/computed_"+model+".json") as f:
                mode_computed_tags = json.load(f)
        except:
            print("tag compilation ignoring uncomputed tags for model "+model)
            continue

        js_file.write("dataFile[\""+model+"\"] = ")
        json.dump(mode_computed_tags, js_file)
        js_file.write(";\n")

# finally, generate the csv files containing the texts and their metrics
generate_sheets()