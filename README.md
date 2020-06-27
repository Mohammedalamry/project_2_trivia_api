# Full Stack API Final Project

## Full Stack Trivia

"Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out"1. 

"That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch.  
Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. "1

# Getting Started
## pre_rquisites & local development 
 Developers should install python3 ,pip, node.js on their local machines
 

### Backend
Form the Backend folder run pip install -r requirements.txt  
will install all of the required packages are include in requirements file.

To run the application run the  the following commands:
``` 
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run  
``` 


### Frontend
  
Form the frontend folder run the following command to start the client
``` 
npm install just once to install the dependencies
npm start 
```
 There is a useful the instructions in the followin link to start in backend part of the
 project  and frontend from Udacity 
1. [`./frontend/`](./frontend/README.md).
2. [`./backend/`](./backend/README.md).  
 
## Testing
 To run the tests, run
 ```
 dropdb trivia_test
 createdb trivia_test
 psql trivia_test < trivia.psql
 python test_flaskr.py 
 ```
 
# API Reference
## Getting Started
* "Base URL At present this app can only be run locally is not hosted as a  base URL. The backend app is hosted at default,`http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API key."1
# Error Handling
 Errors are returned as JSON object  in the following format:
  ```h {
     'success':False,
     'error':404,
     'message':" resource not found"
   }
   ```
The APi will return four error types when requests fail:
* 404:Resource Not Found
* 400: Bad Request
* 405: Method Not Allowed 
* 422:Unprocessable
# Endpoints
# GET /Categories
* General:
   *Returns a list of category objects, success value.
* Sample: `curlhttp://127.0.0.1:5000/categories` 

   ```js  {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
    },
  "success": true
   }```

# GET/Questions
* General:
   * Returns a list of category objects, a list of questions object, success value, total number of questions, and current category.
   * Returns a paginated in groups of 10 questions.
* Sample: ```curlhttp://127.0.0.1:5000/questions?page=1``` 
```js {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 20
  } ````

# DELETE /questions/(id)
* General:
 * Delete a question of list questions object, return success value, and status_code.
* Sample: `curl -x DELETE http://127.0.0.1:5000/questions/15`
 `{'status_code':200,'success':True  }`

# POST/question
* General:
   *   Create a new question using the submitted Question, Answer, Difficulty, Category.   return success value.
* Sample: `curl  http://127.0.0.1:5000/questions/15` -x POST -H "Content-Type: applicaion/json" -d {question: "Which dung beetle was worshipped by the ancient Egyptians?", answer:"Scarab" ,difficulty:4, category:4}
  `{'status_code':200,'success':True}`   
# POST/questions/search
* General:
   *   in this Endpoint, you can use a submitted search. Search by any phrase. will return the search result depending on what you write a. return questions objects,total_questions, and success value.
* Sample: `curl  http://127.0.0.1:5000/questions/search` -x POST -H "Content-Type: applicaion/json" -d {
     "searchTerm":"Taj"
}
```{
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```
      
# GET /categories/id/questions
   
 * General:
   * Returns questions based on the Selected category a list of questions object, success value, the total number of questions, and the current category.   
   
  * Sample: `curl http://127.0.0.1:5000/categories/6/questions` 
  ```{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}```


# POST/quizzes
 
 * General: 
   *  This endpoint to create the quiz based on category or choose all categories and previous question parameters if provided. return one question object of random questions within the given category, if there are previous questions that are not one of the previous questions. 
  * Sample: ```curl  http://localhost:5000/quizzes -x POST -H "Content-Type: applicaion/json" -d  {"quiz_category":{"type":"Sports","id":6},
  "previous_questions":[10]} ```
``` {
  "question": {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }
}
```
 <!-- Refenced:1. uadcity  -->
 # Acknowledgements:
  The awsome team uadcity 
# project_2_trivia_api 
 