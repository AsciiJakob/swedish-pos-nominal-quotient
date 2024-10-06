import json
import csv


model = "kb_bert"

def generate_sheet():
    with open("output/sheet.csv", "w", newline="") as csvfile:
        # writer = csv.writer(csvfile, delimiter=" ",
        #                         quotechar="|", quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(csvfile)
                # Write the header row
        writer.writerow(['filename', 'id', 'full_nominal_quotient', 'simple_nominal_quotient', 'word_count', 'mean_sentence_length'])

        try:
            with open("output/computed_tags_"+model+".json") as f:
                computedData = json.load(f)
        except:
            print("missing file for model", model)
            exit(1)
        
        # Write each row of data
        for file_data in computedData:
            filename = file_data["filename"]
            for text_data in file_data["texts"]:
                if filename == "15 E" and text_data["id"] == "C242":
                    print("quotient: "+ str(text_data["full_nominal_quotient"]))
                writer.writerow([
                    filename,
                    text_data["id"],
                    text_data["full_nominal_quotient"],
                    text_data["simple_nominal_quotient"],
                    text_data["word_count"],
                    text_data["mean_sentence_length"]
                ])





generate_sheet()