def remove_words_in_quote(tags):
    output = []
    inQuote = False
    for i, taggedSentence in enumerate(tags):
        outputSentence = [] 
        for token in taggedSentence:
            if (token["word"] == '"'):
                inQuote = not inQuote
                print('ignoring: "')
                continue
            if (not inQuote):
                outputSentence.append(token)
            else:
                print("ignoring: ", token["word"])
        inQuote = False
        output.append(outputSentence)



# https://sv.wikipedia.org/wiki/Nominalkvot
def nominal_quotient(posTags):
    numeratorTags = ["NN", "PM", "PP", "PC"]
    denominatorTags = ["PN", "PS", "VB", "AB"]
    fullNumerator = 0
    fullDenominator = 0

    simpleNouns = 0
    simpleVerbs = 0
    
    for taggedSentence in remove_words_in_quote(posTags):
        for word in taggedSentence:
            word = word["entity_group"]
            if (word in numeratorTags):
                fullNumerator += 1
                if (word == "NN"):
                    simpleNouns += 1
            elif (word in denominatorTags):
                fullDenominator += 1
                if (word == "VB"):
                    simpleVerbs += 1
    
    return {"full": fullNumerator/fullDenominator, "simple": simpleNouns/simpleVerbs}

def count_words(text):
    return len(text.split())

def LIX(cWords, cSentences, cLongWords):
    return

def mean_sentence_length():
    return