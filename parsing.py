import re
from docx import Document
import json
from os import listdir
from os.path import isfile, join

# def checkUnclosedQuotes(text, textobj):
#     leftQuoteCount = text.count('"')
#     if (leftQuoteCount % 2 != 0):
#             print("Note: found unclosed quote in text ", textobj["id"])
#             print("[\n", text, "\n]")
def checkUnclosedQuote(text):
    if (text.count('"') % 2 != 0):
        print("\nFound unclosed quote in:\n", text)
        exit(1)

# def checkUnclosedParenthesis(text, textobj):
#     leftQuoteCount = text.count("(")
#     if (leftQuoteCount != text.count(")")):
#             print("Note: found unclosed paranthesis in text ", textobj["id"])
#             print("[\n", text, "\n]")

def checkUnclosedParanthesis(text):
    if (text.count("(") != text.count(")")):
        print("\nFound unclosed paranthesis in:\n", text)
        exit(1)


# Regex pattern. 11 segments of data seperated by space and start/ending with < and >
metadata_pattern = re.compile(r"<(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w)\s+(\w)\s+(\w+)\s+(\w+)\s+(\w)\s+(\w)\s+(\w)>")

def get_folder_docx_files(folderPath):
    onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
    output = []
    for file in onlyfiles:
        if (file.endswith(".docx")):
            if (not folderPath.endswith("/")):
                folderPath += "/"
            output.append({"fullPath": folderPath+file, "filename": file.replace(".docx", "")})
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
            "sex": fields[5], # K=kvinna, M=man
            "ämne": fields[6], # SV=svenska 
            "et_t": fields[7], #ET=ej tillstånd, T=tillstånd finns. Irrelevant eftersom de inte kommer publiceras
            "program": fields[8], # _ (saknas)
            "ort": fields[9], # _ (saknas)
            "format": fields[10] # H=hand, D=dataskriven
        }
        return metadata

def parse_file(filePath, writeDebugFile):
    try:
        document = Document(filePath)
    except:
        print("failed to parse file path:", filePath)
        exit(1)

    textIndx = -1 # start at -1 so that it becomes 0 for the first actual text after it gets incremented for the first metadata
    output = []
    parsedFirstMetadata = False
    for paragraph in document.paragraphs:
        stripped = paragraph.text.strip() # strip trailing whitespace
        if (stripped.startswith("<") and stripped.endswith(">")):
            textIndx+=1 

            metadata = extract_metadata(paragraph.text)
            if (metadata == None):
                print("Failed to parse metadata in file", filePath ,"for paragraph:", paragraph.text)
                exit(1)
            output.append({
                "id": metadata["löpnr"],
                "sex": metadata["sex"],
                "betyg": metadata["betyg"],
                "format": metadata["format"],
                "text": "",
                "italicsMarkingTokens": 0
            })
        else:
            if (textIndx > -1):
                currentText = output[textIndx]

                checkUnclosedQuote(paragraph.text)
                checkUnclosedParanthesis(paragraph.text)

                for run in paragraph.runs:
                    # print(run.italic)
                    if (run.italic):
                        run.text = "<italics>"+run.text+"<\italics>"
                        currentText["italicsMarkingTokens"] += 7
                        # print(run.text)

                # print(paragraph.text)
                currentText["text"] += paragraph.text

                currentText["text"] += "\n"


    # print("OUTPUT:\n", output)

    
    if (writeDebugFile):
        with open("DEBUG_PARSE.json", "w") as json_file:
            json.dump(output, json_file, indent=4)  # "indent" for pretty-printing
    return output

# parse_file("./input/test.docx", False)