# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Getting started
- Base URL: At this point our app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error handling
Notic that errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 422,
    "message": "not processable"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal server error

### Endpoints
#### ```GET '/categories'```
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
  - Request Arguments: None
  - Returns: An object with a single key, ``` categories ```, that contains an object of 
  ```id: category_string``` key: value pairs.

``` 
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

#### ```GET '/questions?page=${page_number}'```
  - Returns a list of questions, the total number of questions, the success value, as well as the list of categories. The list of questions are paginated in groups of 10.
  - Request arguments: ```page``` an integer
  - Returns: an object with the success value, the questions for the page, 
  the total number of questions, the categories, and the current category.

```
{
  'success': True,
  'questions': [
    {
      'id': 2,
      'question': "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      'answer': "Apollo 13",
      'category': 5,
      'difficulty': 4
     }
  ],
  'total_questions': 1,
  'categories': [
    {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    }
  ],
  'current_category': None
}
```
#### ```DELETE '/questions/${id}'```
  - Deletes a particular question corresponding to the id shown as a request parameter.
  - Request arguments: ```id``` - integer
  - Returns the success value, the id of the deleted question, the remaining questions and the total number of questions.

```
{
  'success': True,
  'deleted': 3,
  'questions': [
    {
    'id': 2,
    'question': "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
    'answer': "Apollo 13",
    'category': 5,
    'difficulty': 4
    }
  ],
  'total_questions': 2
}
```

#### ```POST '/questions'```
  - posts a new question, using the submitted question, the answer, the category and the difficulty.
  - Request body:
	```
	  {
		  'question':  'Heres a new question string',
		  'answer':  'Heres a new answer string',
		  'difficulty': 1,
		  'category': 3,
	  }
	```
  - Returns: an object with the success value, the list of questions, the 
  total number of questions and the id of the created question.
  
```
{
  'success': True,
  'questions': [
    {
    'id': 2,
    'question': "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
    'answer': "Apollo 13",
    'category': 5,
    'difficulty': 4
    }    
    {
    'id': 3,
    'question': "Which country won the 2017 AFCON in Gabon ?",
    'answer': "Cameroon",
    'category': 6,
    'difficulty': 4
    }
  ],
  'total_questions': 3
  'created': 3
}
```

#### ```POST '/search/questions'```
  - Fetches the list of questions which contain the submitted substring.
  - Request body:
	```
    {
      'searchTerm': 'this is the term the user is looking for'
    }
	```
  - Returns: an object with the success value, the list of questions, the 
  total number of questions

```
{
  'success': True,
  'questions': [
    {
    'id': 2,
    'question': "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
    'answer': "Apollo 13",
    'category': 5,
    'difficulty': 4
    }    
    {
    'id': 3,
    'question': "Which country won the 2017 AFCON in Gabon ?",
    'answer': "Cameroon",
    'category': 6,
    'difficulty': 4
    }
  ],
  'total_questions': 3,
  'current_category': 6
}
```

#### ```GET '/categories/<int:id/questions'```
  - Fetches the list of question related to the given category id.
  - Request arguments:
    - id: the id of the category the questions belong to.
  - Returns: An object with the success value, the list of questions related to that category, the total number of questions, and the urrent category id.

```
{
  'success': True,
  'questions': [
    {
    'id': 2,
    'question': "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
    'answer': "Apollo 13",
    'category': 5,
    'difficulty': 4
    }    
    {
    'id': 3,
    'question': "Which country won the 2017 AFCON in Gabon ?",
    'answer': "Cameroon",
    'category': 6,
    'difficulty': 4
    }
  ],
  'total_questions': 3,
  'current_category': 6
}
```

### ```POST '/quizzes'```
  - Fetches a new question to ask in the quiz with the submitted previous question list and the quiz category from which the question should be related to. Note that the question is different from the previous ones.
  - Request body:
  ```
  {
    'previous_questions': [2, 15],
    'quiz_category': {'type': 'Entertainment', 'id': 5}
  }
  ```
  - Returns: An object with the success value, and the current question object with its id, question, answer category and its difficulty.

```
{
  'success': True,
  'question': {
    'id': 3,
    'question': "Which country won the 2017 AFCON in Gabon ?",
    'answer': "Cameroon",
    'category': 6,
    'difficulty': 4
    }
}
    
```