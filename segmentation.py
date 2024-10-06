import pickle
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

# Load PunktParameters from the pickle file
with open('punkt-nltk-svenska.pickle', 'rb') as f:
    punkt_params = pickle.load(f, encoding='utf-8')

# Initialize the tokenizer with the parameters
tokenizer = PunktSentenceTokenizer(punkt_params)

# Test text

def segmentize_to_sentences(text):
    sentences = []
    for paragraph in text.split('\n'):
        sentences.extend(tokenizer.tokenize(paragraph))
    return sentences