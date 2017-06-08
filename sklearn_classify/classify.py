import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from pandas import DataFrame
import numpy
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score


def print_confusion_matrix(matrix, class_labels):
  lines = ["" for i in range(len(class_labels)+1)]
  for index, c in enumerate(class_labels):
    lines[0] += "\t"
    lines[0] += c
    lines[index+1] += c
  for index, result in enumerate(matrix):
    for amount in result:
      lines[index+1] += "\t"
      lines[index+1] += str(amount)
  for line in lines:
    print line

def initialize_conversion_matrix(num_labels):
  return [[0 for i in range(num_labels)] for y in range(num_labels)]


'''
counts = count_vectorizer.fit_transform(data['text'].values)
bigram_counts = bigram_vectorizer.fit_transform(data['text'].values)
tfidf_counts = tfidf_vectorizer.fit_transform(data['text'].values)
'''

labels = ["baby", "tool", "home", "pet", "food"]

count_vectorizer = CountVectorizer(min_df=1)
bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=1)
tfidf_vectorizer = TfidfVectorizer(min_df=1)

classifier = MultinomialNB()

pipeline = Pipeline([
  ('count_vectorizer', bigram_vectorizer),
  ('classifier',       classifier)
])

reviews = []
for label in labels:
  filename = "train_%s.json" % label
  with open(filename, 'r') as f:
    for line in f:
      reviews.append({'text': json.loads(line)["reviewText"], 'class': label})

data = DataFrame(reviews)
data = data.reindex(numpy.random.permutation(data.index))

pipeline.fit(data['text'].values, data['class'].values)

test_reviews = []
for index, label in enumerate(labels):
  filename = "test_%s.json" % label
  with open(filename, 'r') as f:
    for line in f:
      test_reviews.append({'text': json.loads(line)["reviewText"], 'class': label})

test_examples = [review['text'] for review in test_reviews]
test_labels = [review['class'] for review in test_reviews]

#print pipeline.score(test_examples)
guesses = pipeline.predict(test_examples)

print accuracy_score(test_labels, guesses)
print confusion_matrix(test_labels, guesses, labels=labels)

