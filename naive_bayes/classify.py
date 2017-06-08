import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from pandas import DataFrame
import numpy
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
from sklearn.cross_validation import KFold
from sklearn.svm import SVC


LABELS = []
LABELS.append("baby")
LABELS.append("tool")
LABELS.append("home")
LABELS.append("pet")
LABELS.append("food")
LABELS.append("automotive")
LABELS.append("instant_video")
LABELS.append("beauty")
LABELS.append("cds_vinyl")
LABELS.append("clothes")
LABELS.append("digital_music")
LABELS.append("cell_phones")
LABELS.append("electronics")
LABELS.append("kindle")
LABELS.append("movies_tv")
LABELS.append("instruments")
LABELS.append("office")
LABELS.append("patio")
LABELS.append("health")
LABELS.append("sports")
LABELS.append("toys")
LABELS.append("video_games")
LABELS.append("books")

def read_review_data(num_classes):
  print "Begin reading in data"
  labels = LABELS[:num_classes]
  reviews = []
  for label in labels:
    train_filename = "train_%s.json" % label
    test_filename = "train_%s.json" % label
    filenames = [train_filename, test_filename]
    for filename in filenames:
      with open(filename, 'r') as f:
        for line in f:
          text = json.loads(line)["reviewText"]
          reviews.append({'text': text, 'class': label})

  data = DataFrame(reviews)
  data = data.reindex(numpy.random.permutation(data.index))

  #to evaluate the length of review
  data["word_count"] = [len(text.split(" ")) for text in data["text"]]

  NUM_TRAIN_SAMPLES = int(len(data) * 0.8)

  train_data = data[:NUM_TRAIN_SAMPLES]
  test_data = data[NUM_TRAIN_SAMPLES:]
  print "End reading in data"

  return (train_data, test_data, labels)

def test_fitted_pipeline(fitted_pipeline, test_data, labels, description=""):
  actual = test_data['class'].values
  print "Predicting %s" % description
  predictions = fitted_pipeline.predict(test_data['text'].values)
  score = accuracy_score(actual, predictions)
  cmat = confusion_matrix(actual, predictions, labels)
  print
  print description or "Results"
  print score
  print labels
  print cmat

def fit_pipeline(pipeline, train_data, description=""):
  print "Training %s Classifier" % description
  pipeline.fit(train_data['text'].values, train_data['class'].values)
  return pipeline

def test_pipeline(pipeline, train_data, test_data, labels, description=""):
  fitted_pipeline = fit_pipeline(pipeline, train_data, description=description)
  test_fitted_pipeline(fitted_pipeline, test_data, labels, description=description)

def evalutate_n_grams(num_classes=5):
  train_data, test_data, labels = read_review_data(num_classes)
  classifier = MultinomialNB()

  unigram_vectorizer = CountVectorizer(stop_words='english')
  bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words='english')
  trigram_vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words='english')
  fourgram_vectorizer = CountVectorizer(ngram_range=(1, 4), stop_words='english')


  unigram_pipeline = Pipeline([
    ('count_vectorizer', unigram_vectorizer),
    ('classifier'      , classifier)
  ])

  bigram_pipeline = Pipeline([
    ('count_vectorizer', bigram_vectorizer),
    ('classifier'      , classifier)
  ])

  trigram_pipeline = Pipeline([
    ('count_vectorizer', trigram_vectorizer),
    ('classifier'      , classifier)
  ])

  fourgram_pipeline = Pipeline([
    ('count_vectorizer', fourgram_vectorizer),
    ('classifier'      , classifier)
  ])

  test_pipeline(unigram_pipeline, train_data, test_data, labels, description="TFIDF Transformer")
  test_pipeline(bigram_pipeline, train_data, test_data, labels, description="TFIDF Transformer")
  test_pipeline(trigram_pipeline, train_data, test_data, labels, description="TFIDF Transformer")
  test_pipeline(fourgram_pipeline, train_data, test_data, labels, description="TFIDF Transformer")

def evaluate_classifier_type(num_classes=5):
  train_data, test_data, labels = read_review_data(num_classes)

  bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words='english')

  mn_classifier = MultinomialNB(fit_prior=False)
  b_classifier = BernoulliNB()

  mn_pipeline = Pipeline([
    ('count_vectorizer', bigram_vectorizer),
    ('classifier'      , mn_classifier)
  ])

  b_pipeline = Pipeline([
    ('count_vectorizer', bigram_vectorizer),
    ('classifier'      , b_classifier)
  ])

  test_pipeline(mn_pipeline, train_data, test_data, labels, description="Multinomial")
  test_pipeline(b_pipeline, train_data, test_data, labels, description="Bernoulli")

def evaluate_tfidf(num_classes=5):
  train_data, test_data, labels = read_review_data(num_classes)
  labels = labels[:num_classes]
  classifier = MultinomialNB()

  bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words='english')
  tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words='english')
  tfidf_transformer = TfidfTransformer()

  no_tfidf_pipeline = Pipeline([
    ('count_vectorizer', bigram_vectorizer),
    ('classifier'      , classifier)
  ])

  tfidf_vectorizer_pipeline = Pipeline([
    ('count_vectorizer', tfidf_vectorizer),
    ('classifier'      , classifier)
  ])

  tfidf_transformer_pipeline = Pipeline([
    ('count_vectorizer', bigram_vectorizer),
    ('tfidf_transformer' , tfidf_transformer),
    ('classifier'      , classifier)
  ])

  test_pipeline(no_tfidf_pipeline, train_data, test_data, labels, description="No TFIDF")

  test_pipeline(tfidf_vectorizer_pipeline, train_data, test_data, labels, description="TFIDF Vectorizer")

  test_pipeline(tfidf_transformer_pipeline, train_data, test_data, labels, description="TFIDF Transformer")

def evaluate_training_counts(train_data, test_data, num_classes=5):
  pass

def evaluate_standard(num_classes=5):
  train_data, test_data, labels = read_review_data(num_classes)

  four_gram_vectorizer = CountVectorizer(ngram_range=(1, 4), stop_words='english')
  classifier = MultinomialNB(fit_prior=False)

  pipeline = Pipeline([
    ('count_vectorizer', four_gram_vectorizer),
    ('classifier'      , classifier)
    ])

  test_pipeline(pipeline, train_data, test_data, labels, description="Standard")

def evaluate_lengths(num_classes=5):
  train_data, test_data, labels = read_review_data(num_classes)

  vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words='english')
  classifier = MultinomialNB(fit_prior=False)

  pipeline = Pipeline([
    ('count_vectorizer', vectorizer),
    ('classifier'      , classifier)
  ])

  shortest_test_data = test_data[test_data["word_count"] < 20]
  short_test_data = test_data[(test_data["word_count"] > 20) & (test_data["word_count"] <= 50)]
  med_test_data = test_data[(test_data["word_count"] > 50) & (test_data["word_count"] <= 100)]
  long_test_data = test_data[test_data["word_count"] > 100]

  fitted_pipeline = fit_pipeline(pipeline, train_data)

  test_fitted_pipeline(pipeline, test_data, labels, description="Standard")
  print
  print "Num shortest data: %s" % str(len(shortest_test_data))
  test_fitted_pipeline(pipeline, shortest_test_data, labels, description="20 Word Max")
  print
  print "Num shortest data: %s" % str(len(short_test_data))
  test_fitted_pipeline(pipeline, short_test_data, labels, description="Between 25 and 50 Words")
  print
  print "Num shortest data: %s" % str(len(med_test_data))
  test_fitted_pipeline(pipeline, med_test_data, labels, description="Between 50 and 100 Words")
  print
  print "Num shortest data: %s" % str(len(long_test_data))
  test_fitted_pipeline(pipeline, long_test_data, labels, description="100 Word Min")


def pickle_pipeline(pipeline, num_classes=5):
  train_data, test_data, labels = read_review_data(num_classes)
  from sklearn.externals import joblib
  fitted_pipeline = fit_pipeline(pipeline, train_data)
  print "Pickling Pipeline"
  joblib.dump(fitted_pipeline, 'classifier.pkl')


def use_pickled_pipeline(num_classes=26):
  _, test_data, labels = read_review_data(num_classes)
  from sklearn.externals import joblib
  print "Loading Pickled Pipeline"
  fitted_pipeline = joblib.load('classifier.pkl')

  test_fitted_pipeline(fitted_pipeline, test_data, labels, description="From Pickle")

  pass
'''



import matplotlib.pyplot as plt

bins = [10 * (i) for i in range(50)]
percents = [0.5506607929515418, 0.8571428571428571, 0.89151434091246839, 0.92522522522522521, 0.92804878048780493, 0.9469924812030075, 0.95398230088495573, 0.9448568398727466, 0.95388502842703726, 0.95697329376854601, 0.96498719043552517, 0.96037735849056605, 0.96003996003996006, 0.96465222348916757, 0.96681096681096679, 0.95469798657718119, 0.94086021505376349, 0.94837476099426388, 0.95259593679458243, 0.95022624434389136, 0.94750000000000001, 0.96625766871165641, 0.96491228070175439, 0.96180555555555558, 0.98084291187739459, 0.96442687747035571, 1.0, 0.95979899497487442, 0.90217391304347827, 0.96575342465753422, 0.93442622950819676, 0.94244604316546765, 0.97058823529411764, 0.94444444444444442, 0.98019801980198018, 0.91752577319587625, 0.95652173913043481, 0.98913043478260865, 1.0, 0.93670886075949367, 0.93333333333333335, 0.94805194805194803, 0.9642857142857143, 1.0, 0.98148148148148151, 0.92500000000000004, 0.90697674418604646, 0.93877551020408168, 1.0, 1.0]


'''

'''
import matplotlib.pyplot as plt

plt.figure()
plt.title('Correct Max Probabilities')
plt.hist(correct, 100)
plt.show()
plt.figure()
plt.title('Incorrect Max Probabilities')
plt.hist(incorrect, 100)
plt.show()

#quit()
'''

'''
count_vectorizer = CountVectorizer(min_df=1, stop_words='english')
bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=1, stop_words='english')
trigram_vectorizer = CountVectorizer(ngram_range=(1, 3), min_df=1, stop_words='english')
fourgram_vectorizer = CountVectorizer(ngram_range=(1, 4), min_df=1, stop_words='english')

tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words='english')
#hashing_vectorizer = HashingVectorizer(n_features=100, non_negative=True)
classifier = MultinomialNB()
g_classifier = GaussianNB()
b_classifier = BernoulliNB()

pipeline = Pipeline([
  ('count_vectorizer', count_vectorizer),
  ('classifier'      , classifier)
])

bigram_pipeline = Pipeline([
  ('count_vectorizer', bigram_vectorizer),
  ('tfidf_transformer',  TfidfTransformer()),
  ('classifier'      , classifier)
])

trigram_pipeline = Pipeline([
  ('count_vectorizer', trigram_vectorizer),
  ('classifier'      , classifier)
])

fourgram_pipeline = Pipeline([
  ('count_vectorizer', fourgram_vectorizer),
  ('classifier'      , classifier)
])


g_pipeline = Pipeline([
  ('count_vectorizer', bigram_vectorizer),
  ('classifier'      , g_classifier)
])

b_pipeline = Pipeline([
  ('count_vectorizer', bigram_vectorizer),
  ('classifier'      , b_classifier)
])


bigram_pipeline.fit(train_data['text'].values, train_data['class'].values)


bigram_predictions = bigram_pipeline.predict(test_data['text'].values)
bigram_score = accuracy_score(actual, bigram_predictions)
bigram_cmat = confusion_matrix(actual, bigram_predictions, labels)

incorrect_indicies = []
correct_indicies = []
for index, (act, pred) in enumerate(zip(actual, bigram_predictions)):
  if act != pred:
    incorrect_indicies.append(index)
  else:
    correct_indicies.append(index)

incorrect = test_data.iloc[incorrect_indicies]
correct = test_data.iloc[correct_indicies]

for index, ic in incorrect.iterrows():
  text = ic["text"]
  c = ic["class"]
  probs = bigram_pipeline.predict_proba([text])[0]
  if max(probs) > 0.5:
    guessed = bigram_pipeline.predict([text])
    print text
    print "Actual: %s, Guessed: %s" % (c, guessed)

import pdb;pdb.set_trace()
asdf = bigram_pipeline.predict_proba(incorrect["text"].values)
qwer = bigram_pipeline.predict_proba(correct["text"].values)
zxcv = [float("%.3f" % max(arr)) for arr in qwer]


print
print bigram_score
print labels
print bigram_cmat


#test_data = test_data[test_data["lengths"] > 1000]

#train_data = train_data[train_data["lengths"] > 100]

quit()

bins = [10 * (i) for i in range(50)]
scores = []
for b in bins:
  td = test_data[(test_data["lengths"] > b) & (test_data["lengths"] < (b+10)) ]
  actual = td['class'].values
  predictions = pipeline.predict(td['text'].values)

  score = accuracy_score(actual, predictions)
  scores.append(score)
  #cmat = confusion_matrix(actual, predictions, labels)
  print "Word Count: %s, Doc Count: %s, Score: %s" % (str(b), str(len(td)), '%.5f' % score)

print bins
print scores


'''

'''
import matplotlib.pyplot as plt

incorrect_indicies = []
correct_indicies = []
for index, (act, pred) in enumerate(zip(actual, predictions)):
  if act != pred:
    incorrect_indicies.append(index)
  else:
    correct_indicies.append(index)

incorrect = test_data.iloc[incorrect_indicies]
correct = test_data.iloc[correct_indicies]

print len(correct)
print len(incorrect)

#[len(correct[correct.lengths < bins[i+1] & correct.lengths > bins[i]]) for i in range(len(bins)-1)]
bins = [50 * (i) for i in range(100)]
correct_counts = [len(correct[correct.lengths < i]) for i in bins]
incorrect_counts = [len(incorrect[incorrect.lengths < i]) for i in bins]

print "Correct"
ccounts = [0 if index == 0 else icc - correct_counts[index-1] for index, icc in enumerate(correct_counts)]
print "Incorrect"
iccounts = [0 if index == 0 else icc - incorrect_counts[index-1] for index, icc in enumerate(incorrect_counts)]
plt.figure()
plt.subplot()
plt.plot(bins, ccounts)
plt.subplot()
plt.plot(bins, iccounts)
plt.show()

["{0:.0f}%".format(c / float(sum(ccounts))) for c in ccounts]

import pdb;pdb.set_trace()


fig = plt.figure()
incorrect["lengths"].plot.hist(bins=50)
fig.suptitle('Incorrect text lengths', fontsize=14, fontweight='bold')
plt.show()

fig = plt.figure()
correct["lengths"].plot.hist(bins=50)
fig.suptitle('Incorrect text lengths', fontsize=14, fontweight='bold')
plt.show()

confusion = numpy.array([[0 for i in range(len(labels))] for y in range(len(labels))])

k_fold = KFold(n=len(data), n_folds=6)
scores = []

for train_indices, test_indices in k_fold:
    train_text = data.iloc[train_indices]['text'].values
    train_y = data.iloc[train_indices]['class'].values

    test_text = data.iloc[test_indices]['text'].values
    test_y = data.iloc[test_indices]['class'].values

    pipeline.fit(train_text, train_y)
    predictions = pipeline.predict(test_text)

    confusion += confusion_matrix(test_y, predictions)
    score = accuracy_score(test_y, predictions)
    scores.append(score)
print numpy.average(scores)
print labels
print confusion

'''

if __name__ == "__main__":

  #evaluate_standard(num_classes=26)
  #evaluate_classifier_type(num_classes=26)
  #evalutate_n_grams(num_classes=3)
  #evaluate_tfidf(num_classes=5)
  #evaluate_lengths(num_classes=10)

  #vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words='english')
  #classifier = MultinomialNB(fit_prior=False)

  #pipeline = Pipeline([
  #  ('count_vectorizer', vectorizer),
  #  ('classifier'      , classifier)
  #])
  #pickle_pipeline(pipeline, num_classes=26)
  use_pickled_pipeline()
  pass

