import pandas as pd 
import os 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinaryEncoder
from sklearn.naive_bayes import BernoullilNB


# setting up path to data 
PATH = os.path.abspath('')
PATH = os.path.join(PATH, 'data')
train_names = 'surnames.csv'
predict_names = 'names.csv'

df = pd.read_csv(os.path.join(PATH, train_names))
df_predict = pd.read_csv(os.path.join(PATH, predict_names))

# Initialize and fit CountVectorizer with given data
vectorizer = CountVectorizer().fit(df['name'])

# vectorise names
word_vectors = vectorizer.transform(df['name'])

# creating mapping from unique label texts to unique integers
# 0 if white 1 if non white
encoder = OrdinaryEncoder().fit(df['label'])

# using the encoder to encode the entire dataset
y = encoder.transform(encoder)

#split dataset in train test
x_train, x_test, y_train, y_test = train_test_split(word_mat, y, test_size=0.3)

#initialise model and fit
clf = BernoullilNB()
clf.fit(x_train, y_train)

all_names = predict_names['name'].tolist()

#predict! 
predictions = clf.predict(all_names, label_str = True)

