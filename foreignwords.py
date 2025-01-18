import json
from os import listdir
from os.path import isfile, join

output = []
folderPath = "output/"
only_files = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
for file in only_files:
    if (file.startswith("computed_") and file.endswith(".json")):
        model = file.split("computed_")[1].split(".json")[0]
        with open("output/"+model+".csv", "w", newline="") as csvfile:
            try:
                with open("output/computed_"+model+".json") as f:
                    computedData = json.load(f)
            except:
                print("missing file for model", model)
                exit(1)
            
            for file_data in computedData:
                filename = file_data["filename"]
                for text in file_data["texts"]:
                    for sentence in text["sentences"]:
                        for token in sentence:
                            if token["entity_group"] == "UO":
                                output.append(token["word"])

print(output)