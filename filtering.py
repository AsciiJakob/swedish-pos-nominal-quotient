def check_tokens(taggedSentence, base, *args):
    for i, _ in enumerate(args):
        if taggedSentence[base+i]["word"] != args[i]:
            return False
    return True

def remove_nonwords(sentences):
    ignore_types = ["MAD", "PAD", "MID"]
    ignore_chars = ['-', '.', ''] # for some reason sometimes these don't fall into the types on the line above
    output = []
    for sentence in sentences:
        outputSentence = []
        for token in sentence:
            if (not token["entity_group"] in ignore_types and not token["word"] in ignore_chars):
                outputSentence.append(token)
            # else:
            #     print(token["word"])
        output.append(outputSentence)
    return output


def filter_sentences(tags, filter_quotes, filter_parenthesis, filter_italics):
    output = []
    skip_tokens = 0

    italics_depth = 0
    parenthesis_depth = 0
    in_quote = False

    for i, taggedSentence in enumerate(tags):
        output_sentence = [] 
        for i, token in enumerate(taggedSentence):
            if (skip_tokens > 0):
                skip_tokens = skip_tokens-1
                continue

            if (token["word"] == '"' and filter_quotes):
                in_quote = not in_quote
            elif (token["word"] == '(' and filter_parenthesis):
                parenthesis_depth += 1
            elif (token["word"] == ')' and filter_parenthesis):
                parenthesis_depth -= 1
            elif (check_tokens(taggedSentence, i, '{', "ITALICS", '}')):
                if (filter_italics):
                    italics_depth += 1
                skip_tokens = 2
            elif (check_tokens(taggedSentence, i, '{', '\\', "ITALICS", '}')):
                if (filter_italics):
                    italics_depth -= 1
                skip_tokens = 3
            elif (not in_quote and parenthesis_depth == 0 and italics_depth == 0):
                output_sentence.append(token)
            
            assert parenthesis_depth >= 0, "Fatal error: parenthesis_depth should never be < 0"
            # else:
                # print("ignoring: ", token["word"])
        if len(output_sentence) > 0:
            output.append(output_sentence)
    assert parenthesis_depth == 0, "Fatal error: text ended without parenthesis being closed off"
    assert italics_depth == 0, "Fatal error: text ended without italics being closed off. This would mean we failed to find at least one ending italics tag."

    return output