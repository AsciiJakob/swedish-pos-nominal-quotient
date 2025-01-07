from flair.data import Sentence, Corpus
from flair.datasets import ColumnCorpus
from flair.models import SequenceTagger
from flair.splitter import SegtokSentenceSplitter
import time

tagger = SequenceTagger.load("Z:/Programming/Phyton/sprakanalys/Flair/flair_full/final-model.pt")
print("loaded tagger!")

# sentence = Sentence("Jag fick en såg i julklapp!")
# sentence = Sentence('George Washington went to Washington.')


def pos_tag(sentence):
    sentence = Sentence(sentence)
    tagger.predict(sentence)

    output = []
    for token in sentence:
        word_class = token.tag.split('.')[0]
        word = token.text

        # Flair groups things like "))" or "<\" into one token instead of two, which is not consistent with KB-bert and will break certain things.
        # This will split it up into two tokens like it should be.
        if (token.text == "))" or token.text == "<\\"): 
            output.append({"entity_group": word_class, "word": token.text[0]})
            word = token.text[1]

        output.append({"entity_group": word_class, "word": word})

    return output 