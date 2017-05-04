from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://pgatour_user:pgatour_user_password@localhost:5432/pgatour')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Player(Base):
  __tablename__ = 'players'
  id = Column('id', Integer, primary_key=True)
  name = Column('name', String)
  stat_lines = relationship("StatLine")

class Stat(Base):
  __tablename__ = 'stats'
  id = Column('id', Integer, primary_key=True)
  name = Column('name', String)
  stat_lines = relationship("StatLine")

class StatLine(Base):
  __tablename__ = 'stat_lines'
  id = Column('id', Integer, primary_key=True)
  player_id = Column('player_id', Integer, ForeignKey("players.id"))
  player = relationship('Player')
  stat_id = Column('stat_id', Integer, ForeignKey("stats.id"))
  stat = relationship('Stat')
  raw = Column('raw', String)
  events = Column('events', Integer)
  year = Column('year', Integer)

import os
import csv

'''
players = set()
def add_players_from_file(filepath):
  with open(filepath, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      player_name = row[2]
      #some players have an astrisk at the end of their name
      #want to remove this for player insertion
      if len(player_name) > 0 and player_name[-1] == "*":
        player_name = player_name[0:-2]
      players.add(player_name)

for subdir, dirs, files in os.walk('stats_csv'):
  for dir in dirs:
    for subdir, dirs, files in os.walk("stats_csv/%s" % dir):
      for file in files:
        filepath = "stats_csv/%s/%s" % (dir, file)
        add_players_from_file(filepath)

for player_name in players:
  if session.query(Player).filter_by(name=player_name).count() == 0:
    p = Player(name=player_name)
    session.add(p)

for subdir, dirs, files in os.walk('stats_csv'):
  for dir in dirs:
    if session.query(Stat).filter_by(name=dir).count() == 0:
      print dir
      s = Stat(name=dir)
      session.add(s)
session.commit()
session.close() #for good measure



def acknowledge_or_create_stat_line(data, stat, year):
  for row in data:
    if len(row) >= 5:
      player_name = row[2]
      if len(player_name) > 0 and player_name[-1] == "*":
        player_name = player_name[0:-2]
      player = session.query(Player).filter_by(name=player_name).first()
      stat_line = session.query(StatLine).filter_by(player=player, stat=stat, year=year).first()
      if not stat_line:
        try:
          events = int(row[3])
        except ValueError:
          events = 0
        raw = row[4]
        stat_line = StatLine(player=player, stat=stat, year=year, events=events, raw=raw)
        session.add(stat_line)

def process_file(filename, stat, year):
  with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    stat_count = session.query(StatLine).filter_by(stat=stat, year=year).count()
    data = list(reader) #only do this because I know reader is about 200. Bigger data sets can have issues!
    file_stat_count = len(data)
    print "%s, stat_count: %s, file_stat_count: %s" % (filename, stat_count, file_stat_count)
    if stat_count != file_stat_count:
      acknowledge_or_create_stat_line(data, stat, year)
      session.commit()
  return filename

from multiprocessing import Pool
pool = Pool()

for subdir, dirs, files in os.walk('stats_csv'):
  for dir in dirs:
    stat = session.query(Stat).filter_by(name=dir).first()
    for subdir, dirs, files in os.walk("stats_csv/%s" % dir):
      for file in files:
        year = int(file[0:-4]) #chopping off the csv
        filepath = "stats_csv/%s/%s" % (dir, file)
        pool.apply_async(process_file, [filepath, stat, year])

pool.close()
pool.join()
'''

phil = session.query(Player).filter_by(name='Phil Mickelson').first()
stat = session.query(Stat).filter_by(name='Driving Distance').first()
stat_lines = session.query(StatLine).filter_by(player=phil, stat=stat).order_by("year")
for stat_line in stat_lines:
  print "%s: %s" % (stat_line.year, stat_line.raw)
