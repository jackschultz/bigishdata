import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import csv
import urllib
import os

import gevent
from gevent import monkey
monkey.patch_all()


url_stub = "http://www.pgatour.com/stats/stat.%s.%s.html" #stat id, year

def feet_string_to_inches(string):
  ''' 29'1" for example, turns it into inches '''
  splits = map(float, string[:-1].split("'"))
  return splits[0] * 12.0 + splits[1]

def to_dollas(string):
  return float(string[1:].replace(',', ''))

category_url_stub = 'http://www.pgatour.com/stats/categories.%s.html'
category_labels = ['RPTS_INQ', 'ROTT_INQ', 'RAPP_INQ', 'RARG_INQ', 'RPUT_INQ', 'RSCR_INQ', 'RSTR_INQ', 'RMNY_INQ']
pga_tour_base_url = "http://www.pgatour.com"
def gather_pages(url, filename):
  print filename
  urllib.urlretrieve(url, filename)

def gather_html():
  stat_ids = []
  for category in category_labels:
    category_url = category_url_stub % (category)
    page = requests.get(category_url)
    html = BeautifulSoup(page.text.replace('\n',''), 'html.parser')
    for table in html.find_all("div", class_="table-content"):
      for link in table.find_all("a"):
        stat_ids.append(link['href'].split('.')[1])
  starting_year = 2015 #page in order to see which years we have info for
  for stat_id in stat_ids:
    url = url_stub % (stat_id, starting_year)
    page = requests.get(url)
    html = BeautifulSoup(page.text.replace('\n',''), 'html.parser')
    stat = html.find("div", class_="parsys mainParsys section").find('h3').text
    print stat
    directory = "stats_html/%s" % stat.replace('/', ' ') #need to replace to avoid
    if not os.path.exists(directory):
      os.makedirs(directory)
    years = []
    for option in html.find("select", class_="statistics-details-select").find_all("option"):
      year = option['value']
      if year not in years:
        years.append(year)
    url_filenames = []
    for year in years:
      url = url_stub % (stat_id, year)
      filename = "%s/%s.html" % (directory, year)
      if not os.path.isfile(filename): #this check saves time if you've already downloaded the page
        url_filenames.append((url, filename))
    jobs = [gevent.spawn(gather_pages, pair[0], pair[1]) for pair in url_filenames]
    gevent.joinall(jobs)


for folder in os.listdir("stats_html"):
  path = "stats_html/%s" % folder
  if os.path.isdir(path):
    for file in os.listdir(path):
      if file[0] == '.':
        continue
      csv_lines = []
      file_path = path + "/" + file
      csv_dir = "stats_csv/" + folder
      if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
      csv_file_path = csv_dir + "/" + file.split('.')[0] + '.csv'
      print csv_file_path
      if os.path.isfile(csv_file_path):
        continue
      with open(file_path, 'r') as ff:
        f = ff.read()
        html = BeautifulSoup(f.replace('\n',''), 'html.parser')
        table = html.find('table', class_='table-styled')
        headings = [t.text for t in table.find('thead').find_all('td')]
        csv_lines.append(headings)
        for tr in table.find('tbody').find_all('tr'):
          info = [td.text.replace(u'\xa0', u' ').strip() for td in tr.find_all('td')]
          csv_lines.append(info)
      #write the array to csv
      with open(csv_file_path, 'wb') as csvfile:
        writer = spamwriter = csv.writer(csvfile, delimiter=',')
        for row in csv_lines:
          writer.writerow(row)



'''
column_keys = ['%', 'AVG']
inputs = [
{'name': 'driving_distance', 'sid': 101, 'conversion': float},
{'name': 'driving_accuracy', 'sid': 102, 'conversion': float},
{'name': 'greens_in_regulation', 'sid': 103, 'conversion': float},
{'name': 'greens_or_fringe_in_regulation', 'sid': '02437', 'conversion': float},
{'name': 'proximity_to_hole', 'sid': 331, 'conversion': feet_string_to_inches},
{'name': 'scrambling', 'sid': 130, 'conversion': float},
{'name': 'putts_per_round', 'sid': 119, 'conversion': float},
{'name': 'percentage_of_yardage_covered_by_tee_shots', 'sid': '02341', 'conversion': float},
{'name': 'strokes_gained_tee_to_green', 'sid': '02674', 'conversion': float},
{'name': 'fairway_proximity', 'sid': 431, 'conversion': feet_string_to_inches},
{'name': 'rough_proximity', 'sid': 437, 'conversion': feet_string_to_inches},
{'name': 'proximity_to_hole_around_green', 'sid': 374, 'conversion': feet_string_to_inches},
{'name': 'three_putt_avoidance', 'sid': 426, 'conversion': float},
{'name': 'one_putt_percentage', 'sid': 413, 'conversion': float},
{'name': 'total_putting', 'sid': '02428', 'conversion': float},

{'name': 'scoring_average', 'sid': 120, 'conversion': float},
{'name': 'scoring_average_actual', 'sid': 108, 'conversion': float},
{'name': 'money_leaders', 'sid': 109, 'conversion': to_dollas}
]

player_stats = defaultdict(dict)
years = range(2014, 1999, -1)
for year in years:
  print year
  for source in inputs:
    print source['name']
    url = url_stub % (source['sid'], year)
    page = requests.get(url)
    html = BeautifulSoup(page.text.replace('\n',''), 'html.parser')
    for row in html.find("table", id="statsTable").find('tbody').find_all('tr'):
      stat_line = [info.text for info in row.find_all('td')]
      player = str(stat_line[2].replace(u'\xa0', u' ').strip())
      stat = source['conversion'](stat_line[4])
      player_stats[player][source['name']] = stat

  filename = "%s.csv" % year
  with open(filename, 'w') as csvfile:
    fieldnames = ['name'] + [s['name'] for s in inputs]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for name, stats in player_stats.iteritems():
      if stats.get('scoring_average') == None:
        continue
      stats['name'] = name
      writer.writerow(stats)

'''
