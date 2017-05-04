from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

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
