import nltk
import _pickle as pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from nltk.corpus import stopwords

class Classifier:

    def __init__(self, model=None, data=None):
        """
        :param data: path of pickle object consisting of data
        """
        if model != None:
            self.best_esti = pickle.load(open(model, "rb"))
        else:
            if data == None:
                data = 'data.p'
            self.data = pickle.load(open(data, "rb"))

            x_text = [x[1] for x in self.data]
            y_response = [x[0] for x in self.data]
            x_train, x_test, y_train, y_test = train_test_split(x_text, y_response, test_size = 0.2, stratify = y_response)

            # Create Pipeline
            text_clf = Pipeline([
                # Convert a collection of text documents to a matrix of token counts so as to create feature vectors
                ('vect', CountVectorizer()),
                # Term Frequency times inverse document frequency to get real keywords
                ('tfidf', TfidfTransformer(norm='l2')),
                # Set up MNB algorithm
                ('clf', MultinomialNB())
            ])

            # Create GridSearchCV params
            grid_params = ({
                'vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'tfidf__norm': ('l1', 'l2', None),
                'tfidf__use_idf': (True, False),
                'tfidf__smooth_idf': (True, False),
                'clf__alpha': (1e-0, 1e-1, 1e-2, 1e-3, 1e-4)
            })

            gs_clf = GridSearchCV(text_clf, grid_params, cv=5, n_jobs=-1)
            gs_clf = gs_clf.fit(x_train, y_train)

            gs_clf.best_score_
            gs_clf.best_params_

            self.best_esti = gs_clf.best_estimator_
            self.best_esti.fit(x_train, y_train)

            self.best_esti.score(x_train, y_train)

    def _stemString(self, line):
        stopWords = set(stopwords.words('english'))
        ps = nltk.PorterStemmer()
        str = ""
        regExpTokenizer = nltk.RegexpTokenizer(r'\w+')
        for sentence in regExpTokenizer.tokenize(line):
            tokens = nltk.word_tokenize(sentence)
            for t in tokens:
                t = t.lower()
                if t not in stopWords:
                    t = ps.stem(t)
                    str = str + t + " "
        return str


    def predict(self, line):
        """
        :param line: the message : it is one single string
        :return: string
        """
        tokenized = self._stemString(line)
        string = [line]
        out = self.best_esti.predict(string)
        return out[0]

# Usage:
# classifier = Classifier(path of pickle object data)
# print (classifier.predict('I have ptsd'))
