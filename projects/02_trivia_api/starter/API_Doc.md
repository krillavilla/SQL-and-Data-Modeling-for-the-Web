# Trivia API Backend Documentation

## Introduction
The Trivia API Backend allows you to manage trivia questions and categories, and play quizzes. The API provides endpoints to fetch categories, retrieve questions, add new questions, delete questions, and play quizzes by fetching random questions.

## Endpoints

### GET /categories

**URL:** `/categories`

**Method:** `GET`

**Description:** Fetches a dictionary of categories where the keys are the ids and the values are the corresponding category strings.

**Request Parameters:** None

**Response Body:**
```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```
**Response Codes:**
- `200`: Categories retrieved successfully.
- `404`: No categories found.

### GET /questions

**URL:** `/questions`

**Method:** `GET`

**Description:** Retrieves a paginated list of questions along with the total number of questions and a dictionary of categories.

**Request Parameters:**
- `page` (integer, optional): The page number for pagination. Default is 1.

**Response Body:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the largest planet in our solar system?",
      "answer": "Jupiter",
      "category": "1",
      "difficulty": 3
    },
    {
      "id": 2,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 2
    }
  ],
  "total_questions": 20,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

**Response Codes:**
- `200`: Questions retrieved successfully.
- `404`: No questions found.

### GET /categories/{category_id}/questions

**URL:** `/categories/<int:category_id>/questions`

**Method:** `GET`

**Description:** Retrieves a list of questions for a specific category.

**Request Parameters:**
- `category_id` (integer): The ID of the category for which to retrieve questions.

**Response Body:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the largest planet in our solar system?",
      "answer": "Jupiter",
      "category": "1",
      "difficulty": 3
    }
  ],
  "total_questions": 1,
  "current_category": "Science"
}
```

**Response Codes:**
- `200`: Questions retrieved successfully.
- `404`: No questions found for the specified category.

### POST /questions

**URL:** `/questions`

**Method:** `POST`

**Description:** Adds a new question to the database.

**Request Body:**
```json
{
  "question": "What is the capital of Japan?",
  "answer": "Tokyo",
  "difficulty": 2,
  "category": "3"
}
```

**Response Body:**
```json
{
  "success": true,
  "created": 2
}
```

**Response Codes:**
- `201`: Question created successfully.
- `400`: Bad request. The request body is missing or malformed.

### DELETE /questions/{question_id}

**URL:** `/questions/<int:question_id>`

**Method:** `DELETE`

**Description:** Deletes a specific question from the database.

**Request Parameters:**
- `question_id` (integer): The ID of the question to delete.

**Response Body:**
```json
{
  "success": true,
  "deleted": 1
}
```

**Response Codes:**
- `200`: Question deleted successfully.
- `404`: Question not found.

### POST /quizzes

**URL:** `/quizzes`

**Method:** `POST`

**Description:** Fetches a random question to be used in a quiz.

**Request Body:**
```json
{
  "previous_questions": [1, 4, 20, 15],
  "quiz_category": {
    "id": "2",
    "type": "Art"
  }
}
```

**Response Body:**
```json
{
  "success": true,
  "question": {
    "id": 5,
    "question": "Who painted the Mona Lisa?",
    "answer": "Leonardo da Vinci",
    "category": "2",
    "difficulty": 3
  }
}
```

**Response Codes:**
- `200`: Question retrieved successfully.
- `404`: No questions found for the specified category.

## Setup

To run the API locally, follow these steps:

### Installing Dependencies

```sh
pip install -r requirements.txt
```

### Setting Up the Database

1. Create a PostgreSQL database:

```sh
createdb trivia
```

2. Run the database migrations:

```sh
flask db upgrade
```

### Running the Flask Application

```sh
flask run
```

## Running Tests

To run the tests, use the following command:

```sh
python -m unittest discover -s tests
```

## Author

Krillavilla

## License

This project is licensed under the MIT License.
```
This `README.md` clearly specifies that it is for the backend of the Trivia API project, 
fulfilling all the requirements for documenting the endpoints, request parameters, 
and response bodies. It also includes instructions for setting up the database, 
running the Flask application,
```
--------------------------------------------------------------------------------------------

# Trivia API Frontend Documentation

## Introduction
The Trivia API Frontend is a web application that allows users to play quizzes based on trivia questions. The frontend communicates with the Trivia API Backend to fetch questions and categories, add new questions, delete questions, and play quizzes.

