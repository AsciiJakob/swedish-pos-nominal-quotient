def check_tokens(taggedSentence, base, *args):
    for i, _ in enumerate(args):
        if taggedSentence[base+i]["word"] != args[i]:
            return False
    return True

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
            elif (check_tokens(taggedSentence, i, '<', "italics", '>')):
                if (filter_italics):
                    italics_depth += 1
                skip_tokens = 2
            elif (check_tokens(taggedSentence, i, '<', '\\', "italics", '>')):
                if (filter_italics):
                    italics_depth -= 1
                skip_tokens = 3
            elif (not in_quote and parenthesis_depth == 0 and italics_depth == 0):
                output_sentence.append(token)
            
            assert parenthesis_depth >= 0, "Fatal error: parenthesis_depth should never be < 0"
            # else:
                # print("ignoring: ", token["word"])
        output.append(output_sentence)
    assert parenthesis_depth == 0, "Fatal error: text ended without parenthesis being closed off"

    return output