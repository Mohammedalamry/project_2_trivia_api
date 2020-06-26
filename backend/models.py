import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
dbUSER=os.environ.get('MD')
dbPASS = os.environ.get('Mp')
database_name = "trivia"
database_path = "postgres://{}:{}@{}/{}".format(dbUSER,dbPASS,'localhost:5432',database_name)
# print(database_path)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question 

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type,id):
    self.type = type
    self.id=id
    # self.jionq = db.session.query(Question,Category.type).join(self.id).all()
  def format(self):
    return {
      'id': self.id,
      'type': self.type,
      # 'jionq':self.jionq 
    }
       
  # jionq = db.session.query(Question,Categ
# test =Question.query.join(Category, Category.id==Question.category).all() 
  # print(jionq) 
def join(self): 
    test =Question.query.join(Category, Category.id==Question.category).all() 
    print(test)