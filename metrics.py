# https://sv.wikipedia.org/wiki/Nominalkvot
def nominal_quotient(posTags):
    # for real nominal quotient
    numeratorTags = ["NN", "PM", "PP", "PC"]
    denominatorTags = ["PN", "PS", "VB", "AB"]
    fullNumerator = 0
    fullDenominator = 0

    # for simple nominal quotient
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

def quote_ratio(text):
    charsInQuote = 0
    for i, s in enumerate(text.split('"')):
        if (i % 2 != 0): # 0: start of the text, not in quote. 1: first quote. 2: after the quote ends. etc
            charsInQuote += len(s) 

    return charsInQuote/len(text)


def count_tokens(text):
    return len(text.split())

def count_quote_chars(text):
    return text.count('"')

def LIX(cWords, cSentences, cLongWords):
    return

def mean_sentence_length():
    return