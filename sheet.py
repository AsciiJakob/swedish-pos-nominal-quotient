import json
import csv
import locale
from os import listdir
from os.path import isfile, join

# since spreadsheets expect "," instead of "." as a decimal indicator in Sweden.
locale.setlocale(locale.LC_NUMERIC, "sv_SE.UTF-8")

def comma(value):
    return locale.format_string("%.12f", value)

def generate_sheets():
        folderPath = "output/"
        only_files = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
        for file in only_files:
            if (file.startswith("computed_") and file.endswith(".json")):
                model = file.split("computed_")[1].split(".json")[0]
                with open("output/"+model+".csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile, delimiter=";")
                    writer.writerow(["Fil", "ID", "Nominalkvot", "Enkel nominalkvot", "Antal ord", "Genomsnittlig meningslängd", "Antal citattecken", "Citatkvot", "LIX", model])

                    try:
                        with open("output/computed_"+model+".json") as f:
                            computedData = json.load(f)
                    except:
                        print("missing file for model", model)
                        exit(1)
                    
                    for file_data in computedData:
                        filename = file_data["filename"]
                        for text_data in file_data["texts"]:
                            writer.writerow([
                                filename,
                                text_data["id"],
                                comma(text_data["full_nominal_quotient"]),
                                comma(text_data["simple_nominal_quotient"]),
                                text_data["word_count"],
                                comma(text_data["mean_sentence_length"]),
                                text_data["quote_char_count"],
                                comma(text_data["quote_ratio"]),
                                comma(text_data["LIX"])
                            ])
                        writer.writerow([]) # we'll have one empty row between each file
        print("Generated sheets")
