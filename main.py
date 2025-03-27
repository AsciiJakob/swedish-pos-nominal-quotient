from segmentation import segmentize_to_sentences
from parsing import parse_file, get_folder_docx_files
from sheet import generate_sheets
from filtering import filter_sentences, remove_nonwords
import metrics as metrics
import json
import sys
import time
import importlib

available_models = ["flair", "kb_bert"]

# default options
selected_model = ["kb_bert"]
filter_quotes = True
filter_parenthesis = True
filter_italics = True

if (len(sys.argv) > 1):
    selected_model = sys.argv[1].split(",")
    if (selected_model[0] == "all"):
        selected_model = available_models
    
    if ("--tag-quotes" in sys.argv):
        filter_quotes = False
        print("Nominal quotient will include words in quotes")
    if ("--tag-parenthesis" in sys.argv):
        filter_parenthesis = False
        print("Nominal quotient will include words in parenthesis")
    if ("--tag-italics" in sys.argv):
        filter_italics = False
        print("Nominal quotient will include words in italics")
    if ("--tag-all" in sys.argv):
        filter_quotes = False
        filter_italics = False
        filter_parenthesis = False
        print("Nominal quotient will include all words in quotes, parenthesis and italics.")


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
            # filter_sentences also removes {ITALICS} tags from the text so they don't distrub metrics, we only need that information if we're filtering italics out.
            filtered_sentences = remove_nonwords(filter_sentences(sentence_aggregation, filter_quotes, filter_parenthesis, filter_italics))
            nominal_quotient = metrics.nominal_quotient(filtered_sentences)

            sentences_just_words = remove_nonwords(filter_sentences(sentence_aggregation, False, False, False))
            word_count = 0
            character_count = 0
            for sentence in sentences_just_words:
                word_count += len(sentence)
                character_count += sum(len(token["word"]) for token in sentence)

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
                "LIX": metrics.LIX(word_count, len(sentences), sentences_just_words),
                "OVIX": metrics.OVIX(word_count, sentences_just_words),
                "character_count": character_count,
                "mean_word_length": character_count/word_count
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