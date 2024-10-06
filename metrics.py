


# https://sv.wikipedia.org/wiki/Nominalkvot
def nominal_quotient(posTags):
    numeratorTags = ["NN", "PM", "PP", "PC"]
    denominatorTags = ["PN", "PS", "VB", "AB"]
    fullNumerator = 0
    fullDenominator = 0

    simpleNouns = 0
    simpleVerbs = 0
    
    for taggedSentence in posTags:
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