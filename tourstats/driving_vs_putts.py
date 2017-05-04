from models import Player, Stat, StatLine

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_

engine = create_engine('postgresql://pgatour_user:pgatour_user_password@localhost:5432/pgatour')
Session = sessionmaker(bind=engine)
session = Session()

stat_names = set([
                  #'Driving Distance',
                  'Putting Average',
                  'Total Putting',
                  'Greens in Regulation Percentage',
                  'Driving Accuracy Percentage',
                  'Proximity to Hole',
                  'Birdie Average',
                  'Scrambling',
                  'Scoring Average'
                 ])

stats = session.query(Stat.id, Stat.name).filter(or_(Stat.name == v for v in stat_names))
stats_info = [(stat.id, stat.name) for stat in stats]

from sqlalchemy import text

sql_text_train = '''
select players.id,
       players.name,
       max(case when stat_lines.stat_id=330 then stat_lines.raw else null end) as putting_average,
       max(case when stat_lines.stat_id=157 then stat_lines.raw else null end) as driving_distance,
       max(case when stat_lines.stat_id=250 then stat_lines.raw else null end) as gir,
       max(case when stat_lines.stat_id=156 then stat_lines.raw else null end) as driving_accuracy,
       max(case when stat_lines.stat_id=382 then stat_lines.raw else null end) as scoring_average
from players
join stat_lines on stat_lines.player_id = players.id
join stats on stat_lines.stat_id=stats.id
where stat_lines.year=2012 and (stats.id=157 or stats.id=330 or stats.id=382 or stats.id=250 or stats.id=156) and stat_lines.raw is not null
group by players.name,players.id;
'''

select_clauses = []
where_clauses = []
for stat_info in stats_info:
  stat_id = stat_info[0]
  stat_name = stat_info[1].lower().replace(' ','_')
  select_string = ", max(case when stat_lines.stat_id=%s then stat_lines.raw else null end) as %s" % (stat_id, stat_name)
  where_string = "stats.id=%s " % (stat_id)
  select_clauses.append(select_string)
  where_clauses.append(where_string)

underscored_stat_names = [stat_name.lower().replace(' ','_') for stat_name in stat_names if stat_name != 'Scoring Average']

sql_text = 'select players.id, players.name'
for select_clause in select_clauses:
  sql_text += select_clause
sql_text += '''
from players
join stat_lines on stat_lines.player_id = players.id
join stats on stat_lines.stat_id=stats.id
where
stat_lines.year=%s
and (
'''
for index, where_clause in enumerate(where_clauses):
  if index != 0:
    sql_text += 'or '
  sql_text += where_clause
sql_text += '''
)
and stat_lines.raw is not null
group by players.name, players.id;
'''

import pandas as pd
import statsmodels.api as sm
from sklearn import linear_model, preprocessing
import numpy as np
import sys
current_module = sys.modules[__name__]

sql_text_train = sql_text % '2012'
sql_text_pred = sql_text % '2013'

driving_accuracy_percentage_clean = lambda x: float(x) * 0.01 * 14
greens_in_regulation_percentage_clean = lambda x: float(x) * 0.01 * 18
greens_or_fringe_in_regulation_clean = lambda x: float(x) * 0.01 * 18
putting_average_clean = lambda x: float(x) * 18

def proximity_to_hole_clean(val):
  distances = str(val).split("'")
  inches = int(distances[0]) * 12 + int(distances[1][1:-1])
  return inches

df = pd.read_sql_query(sql_text_train, engine)
df = df[df.scoring_average.notnull()]
for underscored_stat_name in underscored_stat_names:
  try:
    cleaning_function = getattr(current_module, underscored_stat_name+'_clean')
    df[underscored_stat_name] = df[underscored_stat_name].map(cleaning_function)
  except AttributeError:
    pass

X_train = df[underscored_stat_names].astype(np.float)
X_train = sm.add_constant(X_train)
y = df['scoring_average'].astype(np.float)

res = sm.OLS(y,X_train).fit()
print res.summary()
ytrain = res.predict(X_train)

#prediction time
df_pred = pd.read_sql_query(sql_text_pred, engine)
df_pred = df_pred[df_pred.scoring_average.notnull()]
for underscored_stat_name in underscored_stat_names:
  try:
    cleaning_function = getattr(current_module, underscored_stat_name+'_clean')
    df_pred[underscored_stat_name] = df_pred[underscored_stat_name].map(cleaning_function)
  except AttributeError:
    pass

X_pred = df_pred[underscored_stat_names].astype(np.float)
X_pred = sm.add_constant(X_pred)
y_actual = df_pred['scoring_average'].astype(np.float)

ypred = res.predict(X_pred)

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
#ax.scatter(df['putting_average'].astype(np.float), df['scoring_average'].astype(np.float))
#ax.scatter(y_actual, ypred)
ax.scatter(ytrain, y)

for index, row in df_pred['scoring_average'].iteritems():
  name = df_pred.loc[index]['name']
  if y_actual[index] + 1 < ypred[index] or y_actual[index] - 1 > ypred[index]:
    pass
   # ax.annotate(name, (y_actual[index],ypred[index]))

plt.show()
'''
import csv
import matplotlib.pyplot as plt
filename = "distance_vs_putts.csv"
df = pd.read_csv(filename, index_col=0)

data = {}
names = []
distance = []
putts = []
with open(filename, 'rb') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    data[row[0]] = [row[1:3]]
    names.append(row[0])
    putts.append(row[1])
    distance.append(row[2])

fig, ax = plt.subplots()
ax.scatter(distance, putts)

for i, name in enumerate(names):
  ax.annotate(name, (distance[i],putts[i]))

plt.show()
'''
