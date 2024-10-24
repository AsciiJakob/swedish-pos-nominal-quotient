import re
from docx import Document
import json
from os import listdir
from os.path import isfile, join
stripParanthesis = False 

# remove everything within paranthesis
def removeParanthesis(text, textobj):
    leftParantCount = text.count("(")
    if (stripParanthesis and leftParantCount > 0):
        if (leftParantCount == text.count(")")):
            pattern = r'\([^()]*\)' 
            while re.search(pattern, text):
                text = re.sub(pattern, '', text) # remove everything everything between paranthesis
        else:
            print("Note: found unclosed paranthesis in text ", textobj["id"])
            print("[\n", text, "\n]")
    return text

def checkUnclosedQuote(text):
    if (text.count('"') % 2 != 0):
        print("Found unclosed quote in:", text)
        # exit(1)

def checkUnclosedParanthesis(text):
    if (text.count("(") != text.count(")")):
        print("Found unclosed paranthesis in:", text)
        # exit(1)
        
# def removeQuotes(text, textobj):
#     leftQuoteCount = text.count("(")
#     if (stripParanthesis and leftParantCount > 0):
#         if (leftParantCount == text.count(")")):
#             pattern = r'\([^()]*\)' 
#             while re.search(pattern, text):
#                 text = re.sub(pattern, '', text) # remove everything everything between paranthesis
#         else:
#             print("Note: found unclosed paranthesis in text ", textobj["id"])
#             print("[\n", text, "\n]")
#     return text


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
    document = Document(filePath)

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
                "text": ""
            })
        else:
            if (textIndx > -1):
                currentText = output[textIndx]

                checkUnclosedQuote()
                checkUnclosedParanthesis()

                # paragraph.text = removeParanthesis(paragraph.text, output[textIndx])

                currentText["text"] += paragraph.text

                currentText["text"] += "\n"


    # print("OUTPUT:\n", output)

    
    if (writeDebugFile):
        with open("DEBUG_PARSE.json", "w") as json_file:
            json.dump(output, json_file, indent=4)  # "indent" for pretty-printing
    return output