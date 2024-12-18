def remove_words_in_quote(tags):
    # return tags
    output = []
    inQuote = False
    for i, taggedSentence in enumerate(tags):
        outputSentence = [] 
        for token in taggedSentence:
            if (token["word"] == '"'):
                inQuote = not inQuote
                continue
            elif (not inQuote):
                outputSentence.append(token)
            # else:
                # print("ignoring: ", token["word"])
        output.append(outputSentence)
    return output

def remove_words_in_parenthesis(tags):
    output = []
    parenthesisDepth = 0
    for i, taggedSentence in enumerate(tags):
        outputSentence = [] 
        for token in taggedSentence:
            if (token["word"] == '('):
                parenthesisDepth += 1
                continue
            elif (token["word"] == ')'):
                parenthesisDepth -= 1
                outputSentence.append(token)
            elif (parenthesisDepth == 0):
                outputSentence.append(token)
            # else:
            #     print("ignoring: ", token["word"])
        output.append(outputSentence)
    return output

def remove_words_in_italics(tags):
    output = []
    italicsdepth = 0
    for i, taggedSentence in enumerate(tags):
        outputSentence = [] 
        for i, token in enumerate(taggedSentence):
            if (token["word"] == '<'):
                print("next thing:" + taggedSentence[i+1]["word"])
                if (taggedSentence[i+1]["word"] == '\\'):
                    print("end thing")

            if (token["word"] == '<' and taggedSentence[i+1]["word"] == "italics" and taggedSentence[i+2]["word"] == '>'):
                print("depth!")
                italicsdepth += 1
                continue
            elif (token["word"] == '<' and taggedSentence[i+1]["word"] == "\\" and taggedSentence[i+2]["word"] == "italics" and taggedSentence[i+3]["word"] == '>'):
                print("not depth!")
                italicsdepth -= 1
                outputSentence.append(token)
            elif (italicsdepth == 0):
                outputSentence.append(token)
            else:
                print("ignoring: ", token["word"])
        output.append(outputSentence)
    return output

# https://sv.wikipedia.org/wiki/Nominalkvot
def nominal_quotient(posTags, countQuotedWords, countParenthesisWords):
    # for real nominal quotient
    numeratorTags = ["NN", "PM", "PP", "PC"]
    denominatorTags = ["PN", "PS", "VB", "AB"]
    fullNumerator = 0
    fullDenominator = 0

    # for simple nominal quotient
    simpleNouns = 0
    simpleVerbs = 0

    if (not countQuotedWords):
        posTags = remove_words_in_quote(posTags)
    if (not countParenthesisWords):
        posTags = remove_words_in_parenthesis(posTags)
    # if (True):
    #     posTags = remove_words_in_italics(posTags)

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


def count_words(text):
    return len(text.split())

def count_quote_chars(text):
    return text.count('"')

def LIX(cWords, cSentences, cLongWords):
    return

def mean_sentence_length():
    return