from segmentation import segmentize_to_sentences
from parsing import parseFile, getFolderDocxFiles
# from pos_kb_bert import pos_tag
# from pos_flair import pos_tag
import json
import sys
import time
import importlib

availableModels = ["flair", "kb_bert", "kb_bert_aggregation", "kb_bert_test"]

selectedModels = ["flair"] # set default model
if (len(sys.argv) > 1):
    selectedModels = sys.argv[1].split(",")
    if (selectedModels[0] == "all"):
        selectedModels = availableModels

# Model loop 
for modelIndx, currentModel in enumerate(selectedModels):
    try:
        POSModule = importlib.import_module("Taggers.pos_"+currentModel)
        print("Using model "+currentModel)
    except:
        print("failed to load POS library called: "+currentModel)
        exit(1)
    beginTimestamp = time.time()


    # # load text 
    # with open("14 A.json") as f:
    #     textsFile = json.load(f)
    

    #loop through files
    # loop through texts thing  
    docxFiles = getFolderDocxFiles("input/")
    print("docxfiles: ", docxFiles)

    outputData = []
    for fileIndx, textsfile in enumerate(docxFiles):
        texts = parseFile(textsfile["fullPath"], True)
        outputData.append({"filename": textsfile["filename"], "texts": []})
        for textI, text in enumerate(texts):
            sentenceAggregation = []

            sentences = segmentize_to_sentences(text["text"])
            for sentenceI, sentence in enumerate(sentences):
                sentenceAggregation.append(POSModule.pos_tag(sentence))
                print(f"Processing, model: [{modelIndx+1}/{len(selectedModels)}] file: {textsfile["filename"]} [{fileIndx+1}/{len(docxFiles)}] text: [{textI+1}/{len(texts)}] sentence: [{sentenceI + 1}/{len(sentences)}]", end='\r')
                #wclass = result["entity_group"]

            outputData[fileIndx]["texts"].append({"id": text["id"], "sentences": sentenceAggregation})

        print(f"Model {currentModel} finished processing file {textsfile["filename"]}.docx in {round(time.time()-beginTimestamp, 2)} seconds\n")

    with open("output/computed_tags_"+currentModel+".json", "w") as json_file:
        json.dump(outputData, json_file, indent=4)  # "indent" for pretty-printing

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

