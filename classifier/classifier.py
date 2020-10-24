import re
import pickle
import string
import numpy as np 
import pandas as pd 
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
from nltk.stem.porter import *
from textstat.textstat import *
import sklearn.externals as extjoblib
import joblib
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VS

stopwords = nltk.corpus.stopwords.words("english")
other_exclusions = ["#ff", "ff", "rt"]
stopwords.extend(other_exclusions)
sentiment_analyzer = VS()
stemmer = PorterStemmer()

"""
    Accepts a string and will modify it according to the following criteria:
    1. Replacing a URL with 'URLPRESENT'
    2. Only one whitespace when a long block of whitespace is present
    3. Replacing a Twitter mention with 'MENTIONPRESENT'
"""
def preprocessString(string):
    spaceRegex = '\s+'
    urlRegex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
        '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    mentionRegex = '@[\w\-]+'

    # Shorten whitespace first
    preprocessedText = re.sub(spaceRegex, ' ', string)
    preprocessedText = re.sub(urlRegex, 'URLPRESENT', preprocessedText)
    preprocessedText = re.sub(mentionRegex, 'MENTIONPRESENT', preprocessedText)

    return preprocessedText

"""
    Pass in a tweet and remove long occurrences of whitespace and convert text to all lowercase.
    In addition, the tweet is also stemmed. Stemming is the process of reducing a word to its root. 
"""
def createRootWords(tweet):
    tweets = createTweetTokens(tweet)
    rootWords = []

    for i in tweets:
        i = stemmer.stem(i)
        rootWords.append(i)

    return rootWords

"""
    Pass in a tweet and remove long occurrences of whitespace and convert text to all lowercase.
"""
def createTweetTokens(tweet):
    tweet = " ".join(re.split("[^a-zA-Z]*", tweet)).strip() # Remove excess whitespace
    tweet = tweet.lower() # Convert text to all lowercase

    return tweet.split()

"""
    Accepts a list of tweets and returns of a list of POS (parts of speech) tags. POS tags allow us to 
    classify words into their parts of speech.
"""
def getPOSTags(tweets):
    posTags = []
    for i in tweets:
        tokens = createTweetTokens(preprocessString(i))
        tags = nltk.pos_tag(tokens)
        tagList = [x[1] for x in tags]
        tagString = " ".join(tagList)
        posTags.append(tagString)
    
    return posTags

"""
    Accepts a string and will modify it according to the following criteria:
    1. Replacing a URL with 'URLPRESENT'
    2. Only one whitespace when a long block of whitespace is present
    3. Replacing a Twitter mention with 'MENTIONPRESENT'
    4. Replacing a Twitter hashtag with 'HASHTAGPRESENT'

    Returns the number of URLs, Twitter mentions, and Twitter hashtags present in a string.
"""
def countTwitterObjects(string):
    hashtagRegex = '#[\w\-]+'
    processedText = preprocessString(string) 
    processedText = re.sub(hashtagRegex, 'HASHTAGPRESENT', processedText)

    return processedText.count('URLPRESENT'), processedText.count('MENTIONPRESENT'), processedText.count('HASHTAGPRESENT')

"""
    Features returned include:
    1. FKRA
    2. FRE
    3. Number of characters
    4. Length of tweet
    5. Number of terms
    6. Number of words
    7. Number of unique terms
    8. Sentiment score
    9. Number of hashtags
    10. Number of mentions
"""
def getFeatures(tweet):
    preprocessedText = preprocessString(tweet)
    sentiment = sentimentAnalyzer.polarity_scores(tweet)

    syllables = textstat.syllable_count(preprocessedText) 
    
    charNumber = 0
    for i in preprocessedText:
        charNumber += len(i)
    
    tweetLength = len(tweet)
    termNumber = len(tweet.split())
    wordNumber = len(preprocessedText.split())
    meanSyll = round(float((syllables + 0.001)) / float(wordNumber + 0.001), 4)
    uniqueTermNumber = len(set(preprocessedText.split()))
    
    # Modified FK grade. Average words per sentence is wordNumber / 1
    FKRA = round(float(0.39 * float(wordNumber) + float(11.8 * meanSyll) - 15.59, 1))

    # Modified FRE score. Sentence fixed to 1.
    FRE = round(206.835 - 1.015 * (float(wordNumber)) - (84.6 * float(meanSyll)), 2)

    objectCount = countTwitterObjects(tweet)
    features = [FKRA, FRE, syllables, charNumber, tweetLength, termNumber, wordNumber, uniqueTermNumber, 
            sentiment['compound'], objectCount[2], objectCount[1]]
    
    return features

"""
    Accepts a list of tweets, generates features for each tweet using getFeatures() method, and returns
    an array of features for each tweet in the list.
"""
def listOfFeatures(tweets):
    featureList = []
    for i in tweets:
        featureList.append(getFeatures(i))

    return np.array(featureList)

"""
    Accepts a list of tweets and transformers to convert tweet to accepted model. Each tweet is decomposed into:
    1. Array of TF-IDF scores for a set of n-grams in the tweet.
    2. Array of POS tag sequences in the tweet.
    3. Array of features including sentiment, vocabulary, and readability.

    Returns a pandas Dataframe in which each row is the set of features for a tweet. The features are a subset 
    selected using logistic regression and L1-regularization on the training data.
"""
def transformInputs(tweets, tfVectorizer, idfVector, posVectorizer):
    tf = tfVectorizer.fit_transform(tweets).toarray()
    tfidf = tf * idfVector
    print("Built TF-IDF array")

    posTags = getPOSTags(tweets)
    pos = posVectorizer.fit_transform(posTags).toarray()
    print("Built POS array")

    features = listOfFeatures(tweets)
    print("Built feature array")

    X = np.concatenate([tfidf, pos, features], axis = 1)
    
    return pd.Dataframe(X)

"""
    Generates prediction on trained model to generate predicted y values.
"""
def predictModel(X, model):
    yPred = model.predict(X)
    return yPred

"""
    Returns name of class.
"""
def getClass(classLabel):
    if classLabel == 0:
        return "Hate Speech"
    elif classLabel == 1:
        return "Offensive Language"
    elif classLabel == 2:
        return "Neither"
    else:
        return "No Label"

def getTweetPredictions(tweets, perform_prints = True):
    fixedTweets = []
    for i, ori in enumerate(tweets):
        s = ori
        try:
            s = s.encode("latin1")
        except:
            try:
                s = s.encode("utf-8")
            except:
                pass
        if type(s) != str:
            fixedTweets.append(str(s, errors="ignore"))
        fixedTweets.append(s)
    assert len(tweets) == len(fixedTweets), "Do not remove tweets"
    tweets = fixedTweets
    print(len(tweets), " tweets to classify")

    print("Loading trained classifier...")
    model = joblib.load('final_model.pkl')
    
    print("Loading other information")
    tfVectorizer = joblib.load('final_tfidf.pkl')
    idfVector = joblib.load('final_idf.pkl')
    posVectorizer = joblib.load('final_pos.pkl')

    print("Transforming inputs...")

    X = transformInputs(tweets, tfVectorizer, idfVector, posVectorizer)

    print("Running classification model...")
    predictedClass = predictModel(X, model)

    return predictedClass

if __name__ == '__main__':
    print("Loading data to classify...")
    
    df = pd.read_csv('../data/trump_tweets.csv', engine='python')
    trumpTweets = df.Text
    trumpTweets = [x for x in trumpTweets if type(x) == bytes]
    trumpPredictions = getTweetPredictions(trumpTweets)

    print("Predicting predicted values: ")

    for i, t in enumerate(trumpTweets):
        print(t)
        print(classLabel(trumpPredictions[i]))

    print("Calculate accuracy on labeled data")

    df = pd.read_csv('../data/labeled_data.csv', engine='python')
    tweets = df['tweet'].values
    tweets = [x for x in tweets if type(x) == bytes]
    tweetClass = df['class'].values
    predictions = getTweetPredictions(tweets)
    rightCount = 0

    for i, t in enumerate(tweets):
        if tweetClass[i] == predictions[i]:
            rightCount += 1
    
    accuracy = rightCount / float(len(df))
    print("Accuracy ", accuracy)