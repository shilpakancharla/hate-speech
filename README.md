# Hate Speech Classifier

### Warning: the contents of the data and project contain many offensive slurs, including but not limited to, racist, sexist, homophobic, transphobic, etc. offenses.

## I. Goal

Hate speech, aggressive language, and cyberbullying on social platforms can make the experience of being digitally immersed very difficult. While the argument of having the freedom of speech continually persist, the lines between true freedom and offensiveness become blurred. Freedom of speech can easily be warped into offensive, hateful, and unconstructive words online, particularly towards people who belong to marginalized communities. Formally, hate speech can be defined as *abusive or threatening speech or writing that expresses prejudice against a particular group, especially on the basis of race, religion, or sexual orientation* (as defined by Oxford Languages).

As citizens, how can we keep track of hate speech online that's affecting our fellow peers and neighbors? While I believe there are myriad solutions
to helping each other out, I wanted to try a solution using machine learning models. Machine learning classifiers, alongside a vast amount of data 
gathered through API calls, can offer valid solutions to organizations and companies attempting to monitoring content on their platforms.

## II. Data

The tweets themselves, in total 40,000 of them, were labeled as negative (offensive) or positive (non-offensive). One of the datasets was taken from an <a href="https://datahack.analyticsvidhya.com/contest/practice-problem-twitter-sentiment-analysis/">Analytics Vidhaya competition</a>, while another one was taken from a collection found on this <a href="https://github.com/t-davidson/hate-speech-and-offensive-language/tree/master/data">Github repository</a>.

## III. Model

The main goal of this project is to build a model that discern hate speech on Twitter, a platform that rapidly lets your thoughts out with a simple click. I have tried to follow a typical machine learning cycle in order to generate my model. 
            </p>
            <p>
                There are six parts to this project:
            </p>
            <ol>
                <li>Data preprocessing and cleaning</li>
                <li>Exploratory data analysis</li>
                <li>Training models</li>
                <li>Fetch tweets using Twitter API and store in local MySQL base</li>
                <li>Make predictions on new Tweets with the offline model</li>
                <li>Deploy machine learning model</li>
            </ol>
            <h4>Data preprocessing and cleaning</h4>
            <p>
                Even when there is so much data available to us online, there is always some prelimary work we have to do before feeding data into 
                a model, or even doing some exploratory data analysis. In this context of this project, there are two datasets, and ideally they should
                be merged so that we can feed one cohesive set of data into the algorithm. The solution is to merge these datasets using the Pandas library.
                In addition to merging these datasets, it is important to also balance them. There should be a roughly equal split between tweets that could
                are labeled as negative/offensive and positive/non-offensive.
            </p>
            <p>
                In addition, it's important to make sure that model receives data that is clean and relevant. For this reason, it is important to make the following
                modifications:
            </p>
            <ol>
                <li>Lowercase all words in tweets (eliminate any bias that could stem from words being uppercase or lowercase)</li>
                <li>Removing duplicate tweets</li>
                <li>Removing retweets</li>
                <li>Removing Twitter handles</li>
                <li>Removing mentions</li>
                <li>Categorizing the parts of speech (lemmatization)</li>
                <li>Removing excess whitespace</li>
                <li>Removing stop words and words that are two characters or less</li>
            </ol>
            <p>
                Making all these modifications causes extra columns to be added to the data frame as we process through. In the end, we drop the irrelevant columns.
            </p>
            <h4>Exploratory data analysis</h4>
            <p>
                Tweets can be tokenized and we can perform further operations on them, such as changing "n't" to "not". More detail can be find in the
                Exploration.ipynb file in my repository linked below. We can look at the most common negative and positive words in a given dataset as well.
            </p>
            <h4>Training of models</h4>
            <p>
                The only predictor used for the modeling is the pre-processed and lemmatized version of the text. We use a Term Frequency Inverse Document Frequency (TF-IDF) 
                vectorizer to accomplish this. This is a common algorithm used to transform text into a meaningful representation of numbers used to fit machine algorithm 
                for prediction. The TF-IDF object is pickled so that it can be used in the analysis of newer tweets later on. The threshold of the maximum and minimum document 
                frequency has been set at 90 and 20 percent, respectively. The deep learning model also requires different kinds of preprocessing and that will be applied right 
                before the CNN modeling.
            </p>
            <p>
                The TF-IDF matrix was used across all of the models except for the CNN and Naive Bayes. The CNN performance had a very low accuracy (just above 50%) on the 
                validation set. The neural network definitely needs improvement in order for deep learning to be a robust model for this application.
            </p>
            <p>
                The high performance of logistic regression is due to the fact that there is no neutral class of tweets present like there was in the unmodified datasets.
                If we were to introduce a third class of neutral tweets in addition to the positive and negative tweets, the performance of the logistic regression has a 
                definite chance of decreasing in accuracy.
            </p>
            <hr>
            <h2>Prototype/development notes</h2>
            <p>
                The model created is currently offline and has not been deployed yet. Currently, I have applied for Twitter developer access in order
                to secure API keys and create a live feed upon deploying the logistic regression algorithm.
            </p>
            <h4>What would a finished product look like?</h4>
            <p>
                Once the Twitter API is connected, fresh tweets can be collected periodically (perhaps every few hours) on a local MySQL database which
                solely serves the purpose to house an incoming sets of weets. The Python library Tweepy can be used to create a connection to the Twitter API.
                Within my current codeline, I've included a file known as `custom_tweepy_listener.py` that would serve this purpose. It gathers the necessary
                information about an incoming tweet (actual tweet content and time). All text would need to trimmed of emojis in order to be stored in the database.
                It's possible to also filter by topic. Specifically, we can look at topics potentially related to Islamophobia by looking at keywords such as "Islam"
                and "Muslim." We gather this specific information by looking at the hashatgs on tweets.
            </p>
            <p>
                With this pipeline in place, we can pull sets of data from MySQL to a new Jupyter notebook where it can undergo similar preprocessing to the dataset
                we had cleaned before. Ideally, it would be great to derive insights into the top most offensive words being used on the platform, and the ratio of 
                negative to positive/neutral content circulating on the website.
            </p>
            <p>
                Currently, this application was is displayed using Flask and deployed on Heroku. It is possible to deploy the machine learning model via Flask to allow
                a live feed of data analysis being done as new tweets come into the database and go through the preprocessing and algorithm.
            </p>
