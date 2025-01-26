import json
from os import listdir
from os.path import isfile, join

output = []
folder_path = "output/"
only_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
for file in only_files:
    if (file.startswith("computed_") and file.endswith(".json")):
        model = file.split("computed_")[1].split(".json")[0]
        with open("output/"+model+".csv", "w", newline="") as csvfile:
            try:
                with open("output/computed_"+model+".json") as f:
                    computed_data = json.load(f)
            except:
                print("missing file for model", model)
                exit(1)
            
            for file_data in computed_data:
                filename = file_data["filename"]
                for text in file_data["texts"]:
                    for sentence in text["filtered_sentences"]:
                        for token in sentence:
                            if token["pos"] == "UO":
                                output.append(f"{token["word"]} [{text["id"]}]\n")

with open(folder_path+"foreign_words.txt", "w", encoding="utf-8") as file:
    for item in output:
        file.write(item)