from segmentation import segmentize_to_sentences
from parsing import parse_file, get_folder_docx_files
from sheet import generate_sheets
from filtering import filter_sentences
import metrics as metrics
# from pos_kb_bert import pos_tag
# from pos_flair import pos_tag
import json
import sys
import time
import importlib

availableModels = ["flair", "kb_bert", "kb_bert_aggregation", "kb_bert_test"]

selectedModels = ["kb_bert"] # set default model
if (len(sys.argv) > 1):
    selectedModels = sys.argv[1].split(",")
    if (selectedModels[0] == "all"):
        selectedModels = availableModels
    if (selectedModels[0] == "none"):
        skipProcessing = True

# Model loop 
for modelIndx, currentModel in enumerate(selectedModels):
    print("Attempting to load model", currentModel)
    try:
        POSModule = importlib.import_module("Taggers.pos_"+currentModel)
        print("Loaded model "+currentModel)
    except:
        print("failed to load POS library called: "+currentModel)
        exit(1)
    beginTimestamp = time.time()


    # # load text 
    # with open("14 A.json") as f:
    #     textsFile = json.load(f)
    

    #loop through files
    # loop through texts thing
    docxFiles = get_folder_docx_files("input/")
    print("docxfiles: ", docxFiles)

    outputData = []
    for fileIndx, textsfile in enumerate(docxFiles):
        texts = parse_file(textsfile["fullPath"], False)
        outputData.append({"filename": textsfile["filename"], "texts": []})
        for textI, text in enumerate(texts):
            sentenceAggregation = []

            print(f"Processing, model: [{modelIndx+1}/{len(selectedModels)}] file: {textsfile["filename"]} [{fileIndx+1}/{len(docxFiles)}] text: [{textI+1}/{len(texts)}]", end='\r')

            sentences = segmentize_to_sentences(text["text"])
            for sentenceI, sentence in enumerate(sentences):
                sentenceAggregation.append(POSModule.pos_tag(sentence))

            # Apply filtering to remove words in quotes, parenthesis or italics.
            # Also removes <italics> tags from the text so they don't distrub metrics, we only need that information if we're filtering italics out.
            filtered_sentences = filter_sentences(sentenceAggregation, True, True, True)

            nominalQuotient = metrics.nominal_quotient(filtered_sentences)
            wordCount = metrics.count_tokens(text["text"])-text["italicsMarkingTokens"]

            outputData[fileIndx]["texts"].append({
                "id": text["id"],
                "full_nominal_quotient": nominalQuotient["full"],
                "simple_nominal_quotient": nominalQuotient["simple"],
                "word_count": wordCount,
                "mean_sentence_length": wordCount/len(sentences),
                "sentences": sentenceAggregation, # this and filtered_sentences are only used for the visualizing tool so you can remove these if don't care about that and want to save storage i suppose
                "filtered_sentences": filtered_sentences,
                "quote_char_count": metrics.count_quote_chars(text["text"]),
                "quote_ratio": metrics.quote_ratio(text["text"]),
            })

        print(f"Model {currentModel} finished processing file {textsfile["filename"]}.docx in {round(time.time()-beginTimestamp, 2)} seconds\n")

    with open("output/computed_"+currentModel+".json", "w") as json_file:
        json.dump(outputData, json_file, indent=4)  # "indent" for pretty-printing

# we can't load .json from web javascript since we're just opening a file without running a webserver, hence we're exporting the json data to a js file.
with open("Visualizer/computed_compilation.js", "w") as jsFile:
    jsFile.write("const dataFile = {};\n")
    for i, model in enumerate(availableModels):
        try:
            with open("output/computed_"+model+".json") as f:
                modelComputedTags = json.load(f)
        except:
            print("tag compilation ignoring uncomputed tags for model "+model)
            continue
        # for each model ouput file...

        jsFile.write("dataFile[\""+model+"\"] = ")
        json.dump(modelComputedTags, jsFile)
        jsFile.write(";\n")

# finally, generate the csv files containing the texts and their metrics
generate_sheets()