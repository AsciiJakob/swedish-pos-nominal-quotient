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

def remove_italics_markings(tags):
    output = []
    skipTokens = 0
    for i, taggedSentence in enumerate(tags):
        outputSentence = [] 
        for i, token in enumerate(taggedSentence):
            if (skipTokens > 0):
                skipTokens = skipTokens-1
                print("skipping extra token: ", token["word"])
                continue

            if (check_tokens(taggedSentence, i, '<', "italics", '>')):
                skipTokens = 2
            elif (check_tokens(taggedSentence, i, '<', '\\', "italics", '>')):
                skipTokens = 3
            else:
                outputSentence.append(token)
        output.append(outputSentence)
    return output



def filter_sentences(posTags, quotes, parenthesis, italics):
    if (quotes):
        posTags = remove_words_in_quote(posTags)
    if (parenthesis):
        posTags = remove_words_in_parenthesis(posTags)
    if (italics):
        posTags = remove_words_in_italics(posTags) # also removes italics markings, but doesn't use the function used below
    else:
        posTags = remove_italics_markings(posTags)
    return posTags