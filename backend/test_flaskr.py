import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.dbUSER = os.environ.get('MD')
        self.dbPASS = os.environ.get('Mp')
        self.database_path = "postgres://{}:{}@{}/{}".format(self.dbUSER,self.dbPASS,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
        # add variable to use it in the test
            self.new_question={
      "answer": " Ali Muhammad",
      "category": 4,
      "difficulty": 1,
      "question": "What boxer's original name is  Clay?"
    }    
            self.quiz_send_catogery_prevQ={
    "quiz_category":{
	 "type":"Science",
     "id":1
}, 
"previous_questions":[29,21,22,27]
	
}
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #test_get_paginated_questions 
    def test_get_paginated_questions_(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    #test_404_sent_requesting_beyond_valid_page 
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100',json={'answer':'Maya Angelou'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],' resource not found')
    #test_delete_questions  
    def test_delete_questions(self):
        res = self.client().delete('/questions/24')
        data = json.loads(res.data)
        questions= Question.query.filter(Question.id==24).one_or_none()
        print(data)
        print(questions)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    #test_404_if_question_does_not_exits    
    def test_404_if_question_does_not_exits(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')
    #test_creat_new_question 
    def test_creat_new_question(self):
        res = self.client().post('/questions',json=self.new_question )
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    #test_405_if_question_creation_not_allowed 
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/55',json=self.new_question ) 
        data = json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'method not allowed')
    # test_get_questions_based_on_category
    def test_get_questions_based_on_category(self):  
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['questions'])
    #test_422_sent_requesting_beyond_valid_category 
    def test_422_sent_requesting_beyond_valid_category(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')
    #test_get_question_search_with_results  
    def test_get_question_search_with_results(self):  
        res = self.client().post('/questions/search' , json={'searchTerm':'Giaconda'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        # self.assertEqual(data['sucess'],True)
        self.assertTrue(data['total_questions'],1)
        self.assertEqual(len(data['questions']),1)
        self.assertTrue(data['questions'])

    #test_get_question_search_without_results 
    def test_get_question_search_without_results(self):  
        res = self.client().post('/questions/search' , json={'searchTerm':'122'})
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code,200)
        # self.assertEqual(data['sucess'],True)
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(len(data['questions']),0)
        # self.assertTrue(data['questions'])

    #test_405_method_not_allowed_post__question_search 
    def test_405_method_not_allowed_post__question_search(self):  
        res = self.client().get('/questions/search', json={'searchTerm':'122'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'method not allowed')  
    #test_get_categories_list 
    def test_get_categories_list(self):  
        res = self.client().get('/categories') 
        data = json.loads(res.data)  
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories']) 
    #test_404__with_wrong_in_route_of_categories_list 
    def test_404__with_wrong_in_route_of_categories_list(self):
        res = self.client().get('/categoriess') 
        data = json.loads(res.data)  
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],' resource not found')
    #test_get_quizzes
    def test_get_quizzes(self):  
        res = self.client().post('/quizzes' , json={
"quiz_category":{
	"type":"Science",
     "id":5
}, 
"previous_questions":[2,4]
	
}  )
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code,200)
        if data['question']==False:
           self.assertFalse(data['question'])
         
        self.assertTrue(data['question'])
    #test_400_with_bad_request_to_post_new_quizzes 
    def test_400_with_bad_request_to_post_new_quizzes(self):
        res = self.client().post('/quizzes' , json={
"quiz_category":{
	"type":"Science",
     "id":5
}, 
"previous_questions":'[2,4]'
	
}  )
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'bad request')         
              
      
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()