import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

l = nltk.stem.WordNetLemmatizer()

def posTag(nltkTag):
    if nltkTag.startswith('J'):
        return wordnet.ADJ
    elif nltkTag.startswith('V'):
        return wordnet.VERB
    elif nltkTag.startswith('N'):
        return wordnet.NOUN
    elif nltkTag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def getLemma(sentence):
    # Find all parts of speech for each token
    tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    wordnetTagged = map(lambda x: (x[0], posTag(x[1])), tagged)
    lemmatizedSentence = []
    for word, tag in wordnetTagged:
        if word == 'ass':
            lemmatizedSentence.append(word)
        elif tag is None:
            lemmatizedSentence.append(word)
        else:
            lemmatizedSentence.append(l.lemmatize(word, tag))
    return " ".join(lemmatizedSentence)