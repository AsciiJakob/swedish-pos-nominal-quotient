import json
import csv
import locale

# since spreadsheets expect "," instead of "." as a decimal indicator in Sweden.
locale.setlocale(locale.LC_NUMERIC, "sv_SE.UTF-8")

model = "kb_bert"

def comma(value):
    return locale.format_string("%.12f", value)

def generate_sheet():
    with open("output/sheet.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Fil","ID","Nominalkvot","Enkel nominalkvot", "Antal ord","Genomsnittlig meningslängd"])

        try:
            with open("output/computed_tags_"+model+".json") as f:
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
                    comma(text_data["mean_sentence_length"])
                ])
            writer.writerow([]) # one empty row for new file





generate_sheet()