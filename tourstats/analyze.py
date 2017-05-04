import csv
import numpy as np
from sklearn import linear_model
import os
from bokeh.plotting import figure, output_file, show,vplot
from collections import Iterable, Sequence

stat = 'Driving Distance'
folder_path = 'stats_csv/%s' % (stat)

key = 'AVG.'

years = []
yearly_data = []
year_hash = {}
for filename in os.listdir(folder_path):
  with open(folder_path + '/' + filename, 'rb') as csvfile:
    year = filename.split('.')[0]
    years.append(year)
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames

    avgs = [float(row[key]) for row in reader]
    year_hash[year] = avgs
    yearly_data.append(avgs)

int_years = [int(year) for year in years]

yda = np.array(yearly_data)

p = figure(tools="save", title="Max, Avg, Min Driving Distance Over Time")
p.line(int_years, [np.average(asdf) for asdf in yda], line_color="red")#, fill_color="red", line_color="green", line_width=3, )
p.line(int_years, [np.min(asdf) for asdf in yda], line_color="blue")#, fill_color="red", line_color="green", line_width=3, )
p.line(int_years, [np.max(asdf) for asdf in yda], line_color="green")#, fill_color="red", line_color="green", line_width=3, )
output_file("driving_distance.html", title="Max, Avg, Min Driving Distance Over Time")
show(vplot(p))

'''
filename = '2015.csv'
ind = []
dep = []
names = []
with open(filename, 'rb') as csvfile:
  reader = csv.reader(csvfile)
  headings = reader.next()[1:-1] #headings
  for row in reader:
    names.append(row[0])
    ind.append(map(float, row[1:-3]))
    dep.append(float(row[-2]))

npind = np.array(ind)
npdep = np.array(dep)

regr = linear_model.LinearRegression(normalize=True)

regr.fit(npind, npdep)

for name, coeff in zip(headings, regr.coef_):
  print "%s: %s" % (name, coeff)

print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(npind) - npdep) ** 2))

for name, stats, money in zip(names, ind, dep):
  predicted = '{:20,.2f}'.format(np.dot(stats, regr.coef_))
  print "%s: %s, %s" % (name, predicted, '{:20,.2f}'.format(money))

import csv
from bokeh.plotting import figure, output_file, show, vplot
years = range(2002,2016)
years = [2002, 2015]
for year in years:
  filename = "%s.csv" % year
  with open(filename, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    distances = [float(row['driving_distance']) for row in reader if row['percentage_of_yardage_covered_by_tee_shots']]
    a = np.array(distances)

    hist, edges = np.histogram(a, density=True, bins=100)

    x = np.linspace(np.amin(a)-5, np.amax(a)+5, 1000)
    mu = np.mean(a)
    sigma = np.std(a)
    pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))

    p1 = figure(title="%s Driving Distance" % (year),tools="save", background_fill_color="#E8DDCB")
    p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="#036564", line_color="#033649")
    p1.line(x, pdf, line_color="#D95B43", line_width=8, alpha=0.7, legend="PDF")

    p1.legend.location = "top_left"
    p1.xaxis.axis_label = 'Driving Distance'
    p1.yaxis.axis_label = 'Pr(x)'

    output_file("%s_driving_distance.html" % (year), title="%s Driving Distance" % (year))
    show(vplot(p1))


'''
