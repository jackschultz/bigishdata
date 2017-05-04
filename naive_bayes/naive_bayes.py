import json
import math
from collections import Counter
import string
from nltk.corpus import stopwords
import nltk

STOP_WORDS = set(stopwords.words('english'))
STOP_WORDS.add('')

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

def read_reviews(filename):
  reviews = []
  with open(filename, 'r') as f:
    for line in f:
      reviews.append(json.loads(line))
  return reviews

def review_texts_from_reviews(reviews):
  return [review["reviewText"] for review in reviews]

def get_review_texts(filename):
  reviews = read_reviews(filename)
  return review_texts_from_reviews(reviews)

def clean_review(review):
  exclude = set(string.punctuation)
  review = ''.join(ch for ch in review if ch not in exclude)
  split_sentence = review.lower().split(" ")
  clean = [word for word in split_sentence if word not in STOP_WORDS]
  return clean

def counters_from_file(filename):
  reviews = read_reviews(filename)
  texts = [review["reviewText"] for review in reviews]
  tokens = [clean_review(review_text) for review_text in texts]
  flattened_tokens = [val for sublist in tokens for val in sublist]
  counter = Counter(flattened_tokens)
  return counter

def line_count_from_file(filename):
  return sum(1 for line in open(filename))

def naive_bayes(class_labels, nltk=False):
  if nltk:
    confusion_matrix = naive_bayes_nltk(class_labels)
  else:
    confusion_matrix = naive_bayes_self(class_labels)
  return confusion_matrix

def conditional_prob(word, counters, total_vocab_count):
  word_count = counters[word]
  class_total_word_count = sum(counters.values())
  cond_prob = float((word_count + 1)) / (class_total_word_count + total_vocab_count)
  return cond_prob

def naive_bayes_self(class_labels):
  counters = []
  doc_counts = []
  for label in class_labels:
    filename = "train_%s.json" % label
    doc_counts.append(line_count_from_file(filename))
    counter = counters_from_file(filename)
    counters.append(counter)

  combined_bag = Counter()
  for counter in counters:
    combined_bag += counter
  combined_vocab_count = len(combined_bag.keys())

  probabilities = [float(doc_count) / sum(doc_counts) for doc_count in doc_counts]
  correct = 0
  incorrect = 0
  confusion_matrix = initialize_conversion_matrix(len(class_labels))

  for index, class_name in enumerate(class_labels):
    filename = "test_%s.json" % class_name
    texts = get_review_texts(filename)
    for text in texts:
      tokens = clean_review(text)
      scores = []
      for cindex, bag in enumerate(counters): #for each class
        score = math.log1p(probabilities[cindex])
        for word in tokens:
          #for each word, we need the probablity that word given the class / bag
          cond_prob = conditional_prob(word, bag, combined_vocab_count)
          score += math.log(cond_prob)
        scores.append(score)
      max_index, max_value = max(enumerate(scores), key=lambda p: p[1])
      confusion_matrix[index][max_index] += 1

      if index == max_index:
        correct += 1
      else:
        incorrect += 1

  print (correct / float(correct + incorrect))
  return confusion_matrix

def naive_bayes_nltk(class_labels):
  #note, training set needs to be in form of
  #train_set = [
  #({'I': 3, 'like': 1, 'this': 1, 'product': 2}, 'class_name_1')
  #({'This': 2, 'is': 1, 'really': 1, 'great': 2}, 'class_name_1')
  #...
  #({'Big': 1, 'fan': 1, 'of': 1, 'this': 1}, 'class_name_X')
  #]
  train_set = []
  for class_name in class_labels:
    filename = "train_%s.json" % class_name
    texts = get_review_texts(filename)
    for text in texts:
      tokens = clean_review(text)
      counter = Counter(tokens)
      train_set.append((dict(counter), class_name))

  classifier = nltk.NaiveBayesClassifier.train(train_set)

  correct = 0
  incorrect = 0
  confusion_matrix = initialize_conversion_matrix(len(class_labels))

  for index, class_name in enumerate(class_labels):
    filename = "test_%s.json" % class_name
    reviews = read_reviews(filename)
    texts = [review["reviewText"] for review in reviews]
    for text in texts:
      tokens = clean_review(text)
      counter = dict(Counter(tokens))
      guess = classifier.classify(counter)
      lindex = class_labels.index(guess)
      confusion_matrix[index][lindex] += 1

      if guess == class_name:
        correct += 1
      else:
        incorrect += 1

  print (correct / float(correct + incorrect))
  classifier.show_most_informative_features()
  return confusion_matrix

if __name__ == "__main__":

  class_labels = ['baby', 'tool']

  confusion_matrix = naive_bayes(class_labels)#, nltk=True)
  print_confusion_matrix(confusion_matrix, class_labels)
