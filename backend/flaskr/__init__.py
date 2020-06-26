import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
import random

from models import setup_db, Question, Category,join,db
 
# QUESTIONS_PER_PAGE = 10
 
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  @app.route("/")
  def home():
    return  jsonify({'message':'HellloAPi'})
   
  # '''
  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  # '''
  cors = CORS(app,resources={r"api/*":{"origins":"*"}})
  # '''
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  # '''
  @app.after_request
  def after_request(response):
    query= Question.query.filter(Question.id==2).all()
    # print(query[0].answer)
    response.headers.add('Access-Control-Allow-Headers','Content-Type')
    response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
    return response
  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests 
  # for all available categories.
  # '''
  @app.route('/categories')
  def get_categories_list():
    query = Category.query.all() 
    cat_list= { cat.id:cat.type for cat in query }
    print(cat_list)
    return jsonify({
          'success':True,
           'categories':cat_list
    })
    
  # '''Category
  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 
  #add for the lengh abort (404) to lengh of currentbooks
  @app.route('/questions')
  def get_P_questions():  
    queryl = Question.query.filter(Question.category==Category.id).all()
    query = Category.query.all() 
      
    # test =Category.query.join(Question).filter(Question.id==Category.id).all()
    # print(test)
    # print(join) 
    page = request.args.get('page',1,type=int)
    strt=(page-1)*10
    end= strt+10
    # print(query[0].format())
    # cat={**query[0].format(),**query[1].format()}
    # print(cat)
     
    cat_list={cat.id:cat.type  for cat in query }
      
    # for cat in query:
    #     # cat_list.append(cat.type.format())
    #     cat_lis= cat_lis.items()

    #     return jsonify({ 
    #       'categorie':cat_lis})
    # [cat_lis["type"].append(cat.type.format()) for cat in query ] 
    # ser=set(cat_list) 
        # cat_list={'typ':cat.format()}
    # for cat in query:
    #   cat_list ={cat.id:cat.type} 
    # cat1= dict (cat_list )
     
    qu_list= [cat.format() for cat in queryl ]
    list_Q_page=qu_list[strt:end]
    if len(list_Q_page)==0:
       abort(404)
    return jsonify({ 
      'success':True,
       'questions':list_Q_page,
       'total_questions':len(qu_list), 
        'categories' :cat_list,
        'current_category':None
         
    })

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 
  # '''

  # '''
  # @TODO: 
  # Create an endpoint to DELETE question using a question ID. 
  @app.route('/questions/<int:id>', methods=['DELETE'] )
  def delet_Qubyid(id):
    #  id = request.args.get('id',1,type=int)
    #  print(id)
    errord=False
    try:
      
      questions= Question.query.filter(Question.id==id).one_or_none()
     
      if questions is None:
         abort(404)
      questions.delete()
      # return jsonify({'status_code':200,'success':True  })
    except: 
      errord=True
      db.session.rollback()
      # abort_m=422
      abort(422)
      
      
    # else:
    #   questions.delete()
    finally: 
     db.session.close() 
     if errord== False :  
      return jsonify({'status_code':200,'success':True  })
    #  elif  abort_m==422:
    #      abort(422)

       
  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page. 
  # '''

  # '''
  # @TODO: 
  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.
  @app.route('/questions', methods=['POST'])
  def create_questions():
    #  data = request.args.get('data')
   try: 
     data= request.get_json()
     new_question= data.get('question',None)
     new_answer=data.get('answer',None)
     new_difficulty=data.get('difficulty',None)
     new_category=data.get('category',None)
   except:
     abort(405)
   else:
     
     question= Question(question=new_question,answer=new_answer,difficulty=new_difficulty,category=new_category)
     question.insert()
     print(new_question) 
     return jsonify({'success':True})
     
  #  finally:
    #  print(data['question'], data.answer,data.difficulty, data.category ,sep='\n')
    #  return jsonify({'success':True})
 

  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  
  # '''

  # '''
  # @TODO: 
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 
  @app.route('/questions/search' ,methods=['POST'])
  def Search_questions():
    try:
      search_data = request.get_json()
      searchTerm = search_data.get('searchTerm',None)
      print(searchTerm)
      query_searchTerm=Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
      searchTerm_list= [cat.format() for cat in query_searchTerm ]
      print(query_searchTerm)
      return jsonify({
        'questions':searchTerm_list ,
         'total_questions':len(searchTerm_list),
         'current_category':'Sports',
        'succse':'search'  })
    except:
      abort(405)
    finally:
      db.session.close()
  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 
  # '''

  # '''
  # @TODO: 
  # Create a GET endpoint to get questions based on category. 
  @app.route('/categories/<int:id_cat>/questions')
  def questions_based_on_category(id_cat):
    try:  
       print(id_cat)
       questionscat= Question.query.filter(id_cat == Question.category).all()
       if len(questionscat)==0:
         abort(404)
            
       print(questionscat)
       questions_list= [cat.format() for cat in questionscat]
    except:
       abort(422)
    else:
      
       return jsonify({
       'questions':questions_list,
       'total_questions':len(questions_list),
       'current_category':'Sports',
       'sucess':True })
  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 
  # '''


  # '''
  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 
  @app.route('/quizzes',methods=['POST'])
  def playquizzes():
    body = request.get_json()
    quiz_category = body.get('quiz_category')
    quiz_category_id= quiz_category['id'] 
    # query_quizzes=''
    # quiz_category_id= quiz_category.get('id') 
    print(quiz_category_id)
    print(quiz_category)
    previousQuestions = body.get('previous_questions')
    print(len(previousQuestions))
    query_quizzes=[]
    x='mmmmm'
    currentQ=[]
    try:
     if quiz_category_id ==0:
       query_quizzes = (Question.query.filter(~Question.id.in_(previousQuestions)).all())
       for li in query_quizzes:
           x= random.choice(query_quizzes)
           print(x) 
        
       print(len(query_quizzes))
       if len(query_quizzes)==0: 
          print(x)
          return jsonify({'question':False       })
       else:
          currentQ = x.format()
          return jsonify({'question':currentQ    
              })
      
     else:
        
       query_quizzes = Question.query.filter(Question.category==quiz_category_id ).filter(~Question.id.in_(previousQuestions)).all()
      #  print(query_quizzes)
      #  if query_quizzes==[]:
      #      abort(404) 
      #  currentQ = query_quizzes[0].format() 
       for li in query_quizzes:
         x= random.choice(query_quizzes)
         print(x) 
       if len(query_quizzes)==0:
          # x=''
          print(x) 
          return jsonify({'question':False       })
       else:
          currentQ = x.format()
          return jsonify({'question':currentQ    
    
              })
    
     
    except: 
          abort(400)

    finally:
      db.session.close()
      
    # for target_list in query_quizzes:
    #     # if  target_list.id in  previousQuestions:
    #     #     query_quizzes.remove(target_list) 
    #     # else: 
    #      if query_quizzes==None:
    #       return jsonify({'question':False       })
    #      else:
    #       currentQ = query_quizzes[0].format()
    #       return jsonify({'question':currentQ    
    #           })
       
        
       
   
   
   
   
   
  # return jsonify({'f':quiz_category_id})
  #   x=0
  #   x +=1
  #   print(x)
  #   previosQu=[]
  #   query_quizzes=''
  #   if quiz_category_id ==0:
  #      query_quizzes = Question.query.filter(~Question.id.in_(previousQuestions)).all()
       
  #      queryquizzes= random.choice(query_quizzes)
  #      if len(list(query_quizzes))!=0:
  #          return jsonify({
  #        'question':queryquizzes[0].format() 
  #         })
  #      else:
  #        return jsonify({
  #        'question': True})
  #   elif quiz_category_id !=0:
       
      #  query_quizzes = Question.query.filter(Question.category==quiz_category_id ).filter(~Question.id.in_(previousQuestions)).all()
  #      if len(query_quizzes)!=0:
  #          return jsonify({
  #        'question':query_quizzes[0].format() 
  #         })
  #      else:
  #        return jsonify({
  #        'question':False})
  #   # for i in  query_quizzes:

    
  #   # if previousQuestions != []:
  #   #    query_previosQu = Question.query.filter(Question.id.in_(previousQuestions)).all()
  #   #    previosQu= [q.format() for q in query_previosQu]
  #   #  random.choice(query_quizzes)     
  #   # query_quizzes = Question.query.filter(Question.category==quiz_category_id).all()
  #   # current_question = {question.id:question.format() for  question in  query_quizzes  }
  #   # print (current_question)
  #   # current_question={ 'id': query_quizzes[0].id,'question': query_quizzes[0].question,
  #   #  'answer': query_quizzes[0].answer, 'category': query_quizzes[0].category, 'difficulty':query_quizzes[0].difficulty}
   
  #   print(quiz_category,previousQuestions ,quiz_category_id,sep='\n' )
  #   # print(query_quizzes[0].format())
  #   # query_quizzes=  random.choice(query_quizzes)
  #   # print(len(list(query_quizzes))
  #   # previosQu.append(query_quizzes[0])
 
  #   # if len(query_quizzes)!=0:
  #   #   return jsonify({
  #   #    'question':query_quizzes[0].format() 
  #   #      })
  #   # else:
  #   #    return jsonify({
  #   #   'question':False})
  #   # L=len(query_quizzes)
  #   # print(L)
  # # TEST: In the "Play" tab, after a user selects "All" or a category,
  # # one question at a time is displayed, the user is allowed to answer
  # # and shown whether they were correct or not. 
  # # '''

  # '''
  # @TODO: 
  # Create error handlers for all expected errors 
  # including 404 and 422. 
  # '''
  @app.errorhandler(404)
  def not_found(error):
   return jsonify({
     'success':False,
     'error':404,
     'message':" resource not found"
   }),404
   
  @app.errorhandler(422)
  def unprocessable(error):
   return jsonify({
     'success':False,
     'error':422,
     'message':"unprocessable"
   }),422
  
  @app.errorhandler(405)
  def not_found(error):
   return jsonify({
     'success':False,
     'error':405,
     'message':"method not allowed"
   }),405
  
  @app.errorhandler(400)
  def not_found(error):
   return jsonify({
     'success':False,
     'error':400,
     'message':"bad request"
   }),400

  @app.errorhandler(500)
  def not_found(error):
   return jsonify({
     'success':False,
     'error':500,
     'message':"bad request"
   }),500
  @app.errorhandler(500)
  def not_found(error):
   return jsonify({
     'success':False,
     'error':500,
     'message':"bad request"
   }),500
  return app 

    