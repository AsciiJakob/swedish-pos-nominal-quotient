import re
from docx import Document
import json
from os import listdir
from os.path import isfile, join

def check_unclosed_quote(text):
    if (text.count('"') % 2 != 0):
        print("\nFound unclosed quote in:\n", text)
        exit(1)

def check_unclosed_parenthesis(text):
    if (text.count("(") != text.count(")")):
        print("\nFound unclosed paranthesis in:\n", text)
        exit(1)


# Regex pattern. 11 segments of data seperated by space and starting/ending with < and >
metadata_pattern = re.compile(r"<(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w)\s+(\w)\s+(\w+)\s+(\w+)\s+(\w)\s+(\w)\s+(\w)>")

def get_folder_docx_files(folder_path):
    only_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    output = []
    for file in only_files:
        if (file.endswith(".docx")):
            if (not folder_path.endswith("/")):
                folder_path += "/"
            output.append({"fullPath": folder_path+file, "filename": file.replace(".docx", "")})
    return output

def extract_metadata(metadata_line):
    match = metadata_pattern.match(metadata_line)
    if match:
        # Extract metadata into a dictionary
        fields = match.groups()
        metadata = {
            "löpnr": fields[0], #ID
            "prov": fields[1], #Provtyp
            "termin_år": fields[2], # termin/år
            "genre": fields[3], 
            "betyg": fields[4],
            "sex": fields[5], # K=kvinna, M=man. Skrivits på engelska eftersom åäö (ordet "kön") skapar problem när de outputtas
            "ämne": fields[6], # SV=svenska 
            "et_t": fields[7], #ET=ej tillstånd, T=tillstånd finns. Irrelevant eftersom de inte kommer publiceras
            "program": fields[8], # _ (saknas)
            "ort": fields[9], # _ (saknas)
            "format": fields[10] # H=hand, D=dataskriven
        }
        return metadata

def parse_file(file_path):
    try:
        document = Document(file_path)
    except:
        print("failed to parse file path:", file_path)
        exit(1)

    text_index = -1 # start at -1 so that it becomes 0 for the first actual text after it gets incremented for the first metadata
    output = []
    for paragraph in document.paragraphs:
        stripped = paragraph.text.strip() # strip trailing whitespace
        if (stripped.startswith("<") and stripped.endswith(">")):
            text_index+=1 

            metadata = extract_metadata(paragraph.text)
            if (metadata == None):
                print("Failed to parse metadata in file", file_path ,"for paragraph:", paragraph.text)
                exit(1)
            output.append({
                "id": metadata["löpnr"],
                "sex": metadata["sex"],
                "betyg": metadata["betyg"],
                "format": metadata["format"],
                "text_marked_italics": "",
                "text_raw": ""
            })
        else:
            if (text_index > -1):
                current_text = output[text_index]

                check_unclosed_quote(paragraph.text)
                check_unclosed_parenthesis(paragraph.text)

                current_text["text_raw"] += paragraph.text+"\n"


                for run in paragraph.runs:
                    if (run.italic and not run.text.isspace()):
                        run.text = "{ITALICS}"+run.text+"{\\ITALICS}"

                current_text["text_marked_italics"] += paragraph.text+"\n"
    
    return output
