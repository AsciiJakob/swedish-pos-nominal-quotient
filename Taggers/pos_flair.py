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
        # print("word: ", token.text)
        word_class = token.tag.split('.')[0]
        # print("tag: ", word_class)
        output.append({"entity_group": word_class, "word": token.text})

    # print("labels:", sentence.get_labels("pos"))
    # for word in sentence:
    #     print("Word: ", word.tag, "POS value: ", word.get_label("pos").value)
    # return ["entity_group": sentence.tag]
    return output 