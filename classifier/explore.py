import nltk
from nltk.tokenize import TweetTokenizer
from gensim.corpora import Dictionary
import itertools
from collections import defaultdict
import pandas as pd 

t = TweetTokenizer()

def tokenize(tweet):
    tokens = t.tokenize(tweet)
    return [word for word in tokens]

def tokenizeNgrams(string, ngram):
    tokens = ngrams(string, ngram)
    return [word for word in tokens]

def getTokenFreq(series):
    corpusLists = [doc for doc in series.dropna() if doc]
    dictionary = Dictionary(corpusLists)
    corpusBow = [dictionary.doc2bow(doc) for doc in corpusLists]
    tokenFreqBow = defaultdict(int)

    for tokenID, tokenSum in itertools.chain.from_iterable(corpusBow):
        tokenFreqBow[tokenID] += tokenSum
    
    # Create dataframes
    df = pd.DataFrame(list(tokenFreqBow.items()), columns=['tokenID', 'tokencount']).assign(
        token=lambda df1: df1.apply(lambda df2: dictionary.get(df2.tokenID), axis=1),
        docAppeared=lambda df1: df1.apply(lambda df2: dictionary.dfs[df2.tokenID], axis=1)).reindex(
        labels=['tokenID', 'token', 'tokencount', 'docAppeared'], axis=1).set_index('tokenID')

    return df