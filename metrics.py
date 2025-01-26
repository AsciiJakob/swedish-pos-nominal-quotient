import math

# https://sv.wikipedia.org/wiki/Nominalkvot
def nominal_quotient(pos_tags):
    # for real nominal quotient
    numerator_tags = ["NN", "PM", "PP", "PC"]
    # numerator_tags = ["NN", "PP", "PC"]
    denominator_tags = ["PN", "PS", "VB", "AB"]
    # denominator_tags = ["PN", "VB", "AB"]
    full_numerator = 0
    full_denominator = 0

    # for simple nominal quotient
    simple_nouns = 0
    simple_verbs = 0

    for tagged_sentence in pos_tags:
        for word in tagged_sentence:
            word = word["pos"]
            if (word in numerator_tags):
                full_numerator += 1
                if (word == "NN"):
                    simple_nouns += 1
            elif (word in denominator_tags):
                full_denominator += 1
                if (word == "VB"):
                    simple_verbs += 1
    
    if (full_denominator == 0):
        full_nominal_quotient = 0
    else:
        full_nominal_quotient = full_numerator/full_denominator

    if (simple_verbs == 0):
        simple_nominal_quotient = 0
    else:
        simple_nominal_quotient = simple_nouns/simple_verbs

    return {"full": full_nominal_quotient, "simple": simple_nominal_quotient}

def quote_ratio(text):
    charsInQuote = 0
    for i, s in enumerate(text.split('"')):
        if (i % 2 != 0): # 0: start of the text, not in quote. 1: first quote. 2: after the quote ends. etc
            charsInQuote += len(s) 

    return charsInQuote/len(text)

def LIX(word_count, sentence_count, sentences):
    long_words = 0
    for sentence in sentences:
        for token in sentence:
            if (len(token["word"]) > 6):
                long_words += 1

    # print("long words:", long_words)
    # print("word_count:", word_count)
    # print("sentence count:", sentence_count)
    assert word_count > 0, print("Error: text with no words.")
    return word_count/sentence_count+(long_words*100)/word_count


def OVIX(word_count, sentences):
    types = 0
    unique_word_encounters = []
    for sentence in sentences:
        for token in sentence:
            if (not token["word"] in unique_word_encounters):
                types += 1
                unique_word_encounters.append(token["word"])
            
    
    
    # print("tokens:", token_count)
    # print("types:", types)
    
    numerator = math.log(word_count)
    denominator = math.log(2-(math.log(types)/math.log(word_count))) 
    if (denominator == 0):
        denominator = 1
        numerator = 0

    return numerator/denominator
