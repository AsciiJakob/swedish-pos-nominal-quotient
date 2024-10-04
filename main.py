from segmentation import segmentize_to_sentences
# from pos_kb_bert import pos_tag
# from pos_flair import pos_tag
import json
import sys
import time
import importlib

availableModels = ["flair", "kb_bert", "kb_bert_aggregation", "kb_bert_test"]

selectedModels = []
if (len(sys.argv) > 1):
    selectedModels = sys.argv[1].split(",")
    if (selectedModels[0] == "all"):
        selectedModels = availableModels
else:
    selectedModels[0] = "flair"

for modelIndx, currentModel in enumerate(selectedModels):
    try:
        POSModule = importlib.import_module("./Taggers/pos_"+currentModel)
        print("Using model "+currentModel)
    except:
        print("failed to load POS library called: "+currentModel)
        exit(1)
    beginTimestamp = time.time()


    with open("14 A.json") as f:
        textsFile = json.load(f)

    outputTexts = []
    for textI, text in enumerate(textsFile):
        sentenceAggregation = []

        sentences = segmentize_to_sentences(text["text"])
        for sentenceI, sentence in enumerate(sentences):
            sentenceAggregation.append(POSModule.pos_tag(sentence))
            print(f"Processing, model: [{modelIndx+1}/{len(selectedModels)}] text: [{textI+1}/{len(textsFile)}] sentence: [{sentenceI + 1}/{len(sentences)}]", end='\r')
            #wclass = result["entity_group"]

        outputTexts.append({"id": text["id"], "sentences": sentenceAggregation})

    print("Model ", currentModel, " processing completed in ", round(time.time()-beginTimestamp, 2), " seconds.")

    with open("output/computed_tags_"+currentModel+".json", "w") as json_file:
        json.dump(outputTexts, json_file, indent=4)  # "indent" for pretty-printing

with open("Visualizer/compiled_computed_tags.js", "w") as jsFile:
    jsFile.write("const dataFile = {};\n")
    for i, model in enumerate(availableModels):
        try:
            with open("output/computed_tags_"+model+".json") as f:
                modelComputedTags = json.load(f)
        except:
            print("tag compilation ignoring uncomputed tags for model "+model)
            continue
        # for each model ouput file...

        jsFile.write("dataFile[\""+model+"\"] = ")
        json.dump(modelComputedTags, jsFile)
        jsFile.write(";\n")

