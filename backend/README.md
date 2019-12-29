# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.
### Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable
- 500: Internal server error

### Endpoints

#### GET/questions
- General:
  - Returns a list of question objects, total number of questions, current categories of selected questions, and all categories.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions`

#### GET/categories
- General:
  - Returns a list of categories objects.
- Sample: `curl http://127.0.0.1:5000/categories`

#### GET/categories/{category_id}/questions
- General:
  - Returns a list of question objects belonging to `category_id`. Returns questions, total number of questions and current categories of selected  questions.
- Sample: `curl http://127.0.0.1:5000/categories`


#### POST/questions
- General:
    - Creates a new question using the submitted question, answer, difficulty and category. Returns success value.
- Sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d {
            'question': 'is this a test question?',
            'answer': 'yes',
            'difficulty': 5,
            'category': 1,
        }`
        
#### POST/search
- General:
    - search for questions based on submitted search term and returns questions, total questions, and current categories of returned questions.
- Sample `curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d {
            'searchTerm': 'Novel'}`
    
#### POST/quizzes
- General: 
     - Returns a random question that user has not seen yet from the selected category that user has chosen. Frontend needs to submit `previous_questions` and `quiz_category`.
- Sample  `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d {"previous_questions": [15, 16, 17], "quiz_category": {'id': 1, 'type': 'Science'}}`

#### DELETE/questions/{questions_id}
- General:
  - Deletes the question bu using the passed `question_id` and returns the `question_id` and success value.
- Sample: `curl -X DELETE http://127.0.0.1:5000/categores/1/questions`