from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

vowels = ('A', 'E', 'I', 'O', 'U')
import string
alphabet = [letter for letter in string.ascii_uppercase]
boy = 'boy'
girl = 'girl'

def gather_names(gender):
  filename = "%s_names.html" % gender
  names = []
  with open(filename, 'r') as file:
    page = file.read()
    html = BeautifulSoup(page.replace('\n',''), 'html.parser')
    #remove tags with class=tm-embedded-post-container
    #so the ad isn't included in text
    for tag in html.find_all('div', class_="tm-embedded-post-container"):
      tag.decompose()
    for name_link in html.find_all("li", class_="p1"):
      name = name_link.text.upper()
      names.append(name)
  return names

boy_names = gather_names(boy)
girl_names = gather_names(girl)

def gender_names(gender):
  if gender == boy:
    return boy_names
  elif gender == girl:
    return girl_names

def calculate_replace_letter_matches(name_set, first_letter, exchange_letter):
  '''
  Returns list of sets with name matches
  '''
  name_matches = []
  for name in name_set:
    if first_letter in name:
      exchange_name = name.replace(first_letter, exchange_letter)
      temp_name_matches = [name]
      if exchange_name in name_set:
        temp_name_matches.append(exchange_name)
      if len(set(temp_name_matches)) > 1:
        name_matches.append(set(temp_name_matches))

  return name_matches

def replace_single_letter(first_letter='I', exchange_letter='Y', show_matches=True):
  boy_name_set = set(boy_names)
  boy_name_matches = calculate_replace_letter_matches(boy_name_set, first_letter, exchange_letter)
  print 'Boy name matches: %s' % len(boy_name_matches)
  if show_matches:
    print boy_name_matches

  girl_name_set = set(girl_names)
  girl_name_matches = calculate_replace_letter_matches(girl_name_set, first_letter, exchange_letter)
  print 'Girl name matches: %s' % len(girl_name_matches)
  if show_matches:
    print girl_name_matches

def npr_solver(gender):
  print "Vowel Consonant Consonant Starting names for %ss" % gender
  names = gender_names(gender)
  vowel_starters = []
  consonant_starters = []
  for name in names:
    first_letter = name[0]
    if first_letter in vowels:
      vowel_starters.append(name)
    else:
      consonant_starters.append(name)

  for vname in vowel_starters:
    cname_same = []
    for cname in consonant_starters:
      if vname[1:] == cname[1:]:
        cname_same.append(cname)
    if cname_same:
      print vname
      for match in cname_same:
        print match

def rhyming_names(gender):
  print "Rhyming for %ss" % gender
  total_matches = []
  names = gender_names(gender)
  for name in names:
    name_same = []
    for name2 in names:
      if name[1:] == name2[1:] and name != name2:
        name_same.append(name2)
    if name_same:
      name_same.append(name)
      if set(name_same) not in total_matches:
        total_matches.append(set(name_same))
  print "Total %s matches: %s" % (gender, len(total_matches))
  for matches in total_matches:
    print list(matches),
  print #actual new line

def vowel_consonant_beginning_proportion(gender):
  print "Vowel Consonant Beginning Ratio for %ss" % gender
  names = gender_names(gender)
  vowel_starters = []
  consonant_starters = []

  for name in names:
    first_letter = name[0]
    if first_letter in vowels:
      vowel_starters.append(name)
    else:
      consonant_starters.append(name)

  vowel_len = float(len(vowel_starters))
  consonant_len = float(len(consonant_starters))
  print vowel_len / (vowel_len + consonant_len)

def name_letter_begin_or_end(gender, index='beginning'):
  if index is 'beginning':
    asdf = 1
  elif index is 'end':
    asdf = -1
  else:
    print 'fail'
    return
  print "Name letter %s for %ss" % (index, gender)
  names = gender_names(gender)

  cnt = Counter()
  for name in names:
    letter = name[asdf]
    cnt[letter] += 1
  return cnt

def name_lengths_counter(gender):
  names = gender_names(gender)

  cnt = Counter()
  for name in names:
    cnt[len(name)] += 1
  return cnt

def name_lengths(gender):
  names = gender_names(gender)
  return [len(name) for name in names]

def count_name_lengths():
  lengths = np.arange(15)
  boy_lengths = name_lengths_counter(boy)
  girl_lengths = name_lengths_counter(girl)
  boy_lengths_list = [boy_lengths[length] for length in lengths]
  girl_lengths_list = [girl_lengths[length] for length in lengths]

  boy_length_counts = name_lengths(boy)
  girl_length_counts = name_lengths(girl)

  print 'Boy length avg: %s' % np.mean(boy_length_counts)
  print 'Boy length std: %s' % np.std(boy_length_counts)
  print 'Girl length avg: %s' % np.mean(girl_length_counts)
  print 'Girl length std: %s' % np.std(girl_length_counts)

  #time to plot the bars
  fig, ax = plt.subplots()

  opacity = 0.4
  bar_width = 0.35

  rects1 = plt.bar(lengths, boy_lengths_list, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Boys')

  rects2 = plt.bar(lengths + bar_width, girl_lengths_list, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Girls')

  plt.xlabel('Lengths')
  plt.ylabel('Number of names of that length')
  plt.title('Lengths of boy and girl names')
  plt.legend()

  plt.tight_layout()

  plt.savefig('graphs/name_length_bar.png')


def begin_end_names(gender, beginning_letter, ending_letter):
  names = gender_names(gender)
  matching_names = []
  for name in names:
    if name[0] == beginning_letter and name[-1] == ending_letter:
      matching_names.append(name)
  return matching_names





def vowel_consonant_ending_proportion(gender):
  print "Vowel Consonant Ending Ratio for %ss" % gender
  names = gender_names(gender)
  vowel_enders = []
  consonant_enders = []
  for name in names:
    last_letter = name[-1]
    if last_letter in vowels:
      vowel_enders.append(name)
    else:
      consonant_enders.append(name)

  vowel_len = float(len(vowel_enders))
  consonant_len = float(len(consonant_enders))
  print vowel_len / (vowel_len + consonant_len)

def count_vowels_consonants(gender, index):
  '''
  Gives counts for whether the letters at the indicies are vowels or consonants
  index = 1 for first letter, index = -1 for last letter.
  Other indicies work, but might cause error if index is longer than two since
  there are some two letter names!
  '''
  names = gender_names(gender)
  sizes = []
  cnt = Counter()
  for name in names:
    if name[index] in vowels:
      cnt['v'] += 1
    else:
      cnt['c'] += 1
  return cnt

def print_percentages(gender, sizes, title):
  vowel_len = float(sizes[0])
  consonant_len = float(sizes[1])
  vowel_percentage = vowel_len / (vowel_len + consonant_len)
  consonant_percentage = consonant_len / (vowel_len + consonant_len)
  print title % gender
  print 'Vowel percentage: %s' % vowel_percentage
  print 'Consonant percentage: %s' % consonant_percentage
  print #for spacing

def vowels_consonant_starts():
  '''
  Pie graph of the frequency of names that begin with vowels for both genders
  '''
  boy_counts = count_vowels_consonants(boy, 0)
  girl_counts = count_vowels_consonants(girl, 0)

  #graph time for the boys, nothing to do with Saturday being for the boys cause that's a dumb phrase
  title = "Percentage of %s names that start with vowels or consonants"
  labels = 'Vowels', 'Consonants'
  boy_fig, boy_ax = plt.subplots()
  sizes = [boy_counts['v'], boy_counts['c']]
  print_percentages(boy, sizes, title)

  boy_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  plt.title(title % 'boy')
  plt.savefig('graphs/vowel_consonant_start_boy.png')

  sizes = [girl_counts['v'], girl_counts['c']]
  print_percentages(girl, sizes, title)
  girl_fig, girl_ax = plt.subplots()
  girl_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  plt.title(title % 'girl')

  plt.savefig('graphs/vowel_consonant_start_girl.png')

def vowels_consonant_ends():
  '''
  Pie graph of the frequency of names that begin with vowels for both genders
  '''
  boy_counts = count_vowels_consonants(boy, -1)
  girl_counts = count_vowels_consonants(girl, -1)

  #graph time for the boys, nothing to do with Saturday being for the boys cause that's a dumb phrase

  title = "Percentage of %s names that end with vowels or consonants"
  labels = 'Vowels', 'Consonants'
  boy_fig, boy_ax = plt.subplots()

  sizes = [boy_counts['v'], boy_counts['c']]
  print_percentages(girl, sizes, title)
  boy_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  plt.title(title % 'boy')
  plt.savefig('graphs/vowel_consonant_ends_boys.png')

  sizes = [girl_counts['v'], girl_counts['c']]
  print_percentages(girl, sizes, title)
  girl_fig, girl_ax = plt.subplots()
  girl_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  plt.title(title % 'girl')
  plt.savefig('graphs/vowel_consonant_ends_girls.png')

def vowel_endings():
  boy_counts = count_vowel_frequency(boy, -1)
  girl_counts = count_vowel_frequency(girl, -1)

  #graph time for the boys, nothing to do with Saturday being for the boys cause that's a dumb phrase

  title = "Percentage of vowels that %s names end with"
  labels = boy_counts.keys()
  boy_fig, boy_ax = plt.subplots()
  sizes = [boy_counts[vowel] for vowel in labels if vowel in boy_counts.keys()]
  print_percentages(boy, sizes, title)
  boy_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  plt.title(title % 'boy')
  plt.savefig('graphs/vowel_endings_boys.png')

  girl_fig, girl_ax = plt.subplots()
  labels = girl_counts.keys()
  sizes = [girl_counts[vowel] for vowel in labels if vowel in girl_counts.keys()]
  print_percentages(girl, sizes, title)
  girl_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  plt.title(title % 'girl')
  plt.savefig('graphs/vowel_endings_girls.png')

def vowel_beginnings():
  boy_counts = count_vowel_frequency(boy, 0)
  girl_counts = count_vowel_frequency(girl, 0)

  #graph time for the boys, nothing to do with Saturday being for the boys cause that's a dumb phrase

  title = "Percentage of vowels that %s names begin with"
  labels = boy_counts.keys()
  boy_fig, boy_ax = plt.subplots()
  sizes = [boy_counts[vowel] for vowel in labels if vowel in boy_counts.keys()]
  boy_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  plt.title(title % 'boy')
  plt.savefig('graphs/vowel_beginnings_boys.png')

  girl_fig, girl_ax = plt.subplots()
  labels = girl_counts.keys()
  sizes = [girl_counts[vowel] for vowel in labels if vowel in girl_counts.keys()]
  girl_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  plt.title(title % 'girl')
  plt.savefig('graphs/vowel_beginnings_girls.png')

def letter_frequency(index=0):

  boy_name_counter = Counter()
  for name in boy_names:
    beginning_letter = name[0]
    boy_name_counter[beginning_letter] += 1

  print boy_name_counter

  girl_name_counter = Counter()
  for name in girl_names:
    beginning_letter = name[0]
    girl_name_counter[beginning_letter] += 1

  print girl_name_counter

  boy_alphabet_count_list = []
  girl_alphabet_count_list = []
  for letter in alphabet:
    boy_alphabet_count_list.append(float(boy_name_counter[letter]))
    girl_alphabet_count_list.append(float(girl_name_counter[letter]))

  print boy_alphabet_count_list
  print girl_alphabet_count_list

  #time to plot the bars
  fig, ax = plt.subplots()

  opacity = 0.6
  bar_width = 0.35

  num_letters = np.arange(26)
  rects1 = plt.bar(num_letters, boy_alphabet_count_list, bar_width,
                 align='center',
                 alpha=opacity,
                 color='b',
                 label='Boys')

  rects2 = plt.bar(num_letters + bar_width, girl_alphabet_count_list, bar_width,
                 align='center',
                 alpha=0.8,
                 color='palevioletred',
                 label='Girls')

  plot_title = 'Number of names that begin with certain letters'
  xtick_pos = [let + (bar_width / 2) for let in num_letters]
  plt.xticks(xtick_pos, alphabet)
  plt.xlabel('Letters')
  plt.ylabel('Number of names that begin with letter')
  plt.title(plot_title)
  plt.legend()
  plt.tight_layout()
  #plt.show()
  plt.savefig('graphs/letter_frequency.png')


def count_vowel_frequency(gender, index):
  names = gender_names(gender)
  sizes = []
  cnt = Counter()
  for name in names:
    index_letter = name[index]
    if index_letter in vowels:
      cnt[index_letter] += 1
  return cnt

def common_names(gender):
  '''
    Gathers the letters that the names start with, and then count the combos of all the names that begin and end with the matching letters.
  '''
  begin_gender_counts = name_letter_begin_or_end(gender, index='beginning')
  end_gender_counts = name_letter_begin_or_end(gender, index='end')

  for bletter in begin_gender_counts:
    for eletter in end_gender_counts:
      match_names= begin_end_names(gender, bletter, eletter)

  for name in match_names:
    print name


if __name__ == '__main__':
  #npr_solver(boy)
  #npr_solver(girl)
  #vowels_consonant_starts()
  #vowels_consonant_ends()
  #vowel_endings()
  #vowel_beginnings()
  #letter_frequency()
  #letter_frequency(index=0)
  #count_name_lengths()
  #replace_single_letter(first_letter='I', exchange_letter='Y')
  #replace_single_letter(first_letter='IE', exchange_letter='Y')
  #replace_single_letter(first_letter='EE', exchange_letter='Y')
  #replace_single_letter(first_letter='A', exchange_letter='Y')
  #replace_single_letter(first_letter='C', exchange_letter='K')
  #replace_single_letter(first_letter='CK', exchange_letter='K')
  #replace_single_letter(first_letter='HN', exchange_letter='N')
  #replace_single_letter(first_letter='G', exchange_letter='J')
  #rhyming_names(boy)
  #rhyming_names(girl)
  '''
  for index, l1 in enumerate(alphabet):
    for l2 in alphabet[index:]:
      print "Flip %s and %s" % (l1, l2)
      replace_single_letter(first_letter=l1, exchange_letter=l2, show_matches=True)
  for match in alphabet:
    print "Flip %s and %s" % ('K', match)
    replace_single_letter(first_letter='K', exchange_letter=match, show_matches=True)
  '''
  pass # in case you don't uncomment a test you want to run, we need correct syntax
