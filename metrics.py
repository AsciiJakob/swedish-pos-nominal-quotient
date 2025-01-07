def check_tokens(taggedSentence, base, *args):
    for i, _ in enumerate(args):
        if taggedSentence[base+i]["word"] != args[i]:
            return False
    return True

def remove_words_in_quote(tags):
    # return tags
    output = []
    inQuote = False
    for i, taggedSentence in enumerate(tags):
        outputSentence = [] 
        for token in taggedSentence:
            if (token["word"] == '"'):
                inQuote = not inQuote
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
            elif (token["word"] == ')'):
                parenthesisDepth -= 1
            elif (parenthesisDepth == 0):
                outputSentence.append(token)
            else:
                print("ignoring: ", token["word"])
            assert parenthesisDepth >= 0, "Fatal error: parenthesisdepth should never be < 0"
        output.append(outputSentence)
    return output

def remove_words_in_italics(tags):
    output = []
    italicsdepth = 0
    skipTokens = 0
    for i, taggedSentence in enumerate(tags):
        outputSentence = [] 
        for i, token in enumerate(taggedSentence):
            if (skipTokens > 0):
                skipTokens = skipTokens-1
                print("skipping extra token: ", token["word"])
                continue

            if (check_tokens(taggedSentence, i, '<', "italics", '>')):
                italicsdepth += 1
            elif (check_tokens(taggedSentence, i, '<', '\\', "italics", '>')):
                italicsdepth -= 1
                skipTokens = 3
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
    if (True):
        posTags = remove_words_in_italics(posTags)

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