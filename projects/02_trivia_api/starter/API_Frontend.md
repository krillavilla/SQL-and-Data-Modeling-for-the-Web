# Trivia API Frontend Documentation

## Introduction
The Trivia API Frontend allows you to interact with the Trivia API Backend to manage trivia questions and categories, and play quizzes. The frontend provides endpoints to fetch categories, retrieve questions, add new questions, delete questions, search for questions, and play quizzes by fetching random questions.

## Endpoints

### GET /api/categories

**URL:** `/api/categories`

**Method:** `GET`

**Description:** Fetches a dictionary of categories where the keys are category IDs and the values are category strings.

**Request Arguments:** None

**Response Body:**
```json
{
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
- `500`: Internal server error.
- `503`: Service unavailable.
- `504`: Gateway timeout.
- `505`: HTTP version not supported.
- `511`: Network authentication required.
- `599`: Network connect timeout error.
- `600`: Unparseable response headers.
- `601`: Network read timeout error.
- `602`: Network connect timeout error.


### GET /api/questions

**URL:** `/api/questions`

**Method:** `GET`

**Description:** Retrieves a paginated list of questions along with the total number of questions, all categories, and the current category string.

**Request Arguments:**
- `page` (integer): The page number for pagination. Default is 1.
- `category` (string, optional): The category to filter questions by.
- `difficulty` (integer, optional): The difficulty level to filter questions by.
- `searchTerm` (string, optional): The search term to filter questions by.
- `previous_questions` (list, optional): The list of previous question IDs for the quiz.
- `quiz_category` (string, optional): The category for the quiz.
- `question` (string, optional): The question to add.
- `answer` (string, optional): The answer to add.
- `difficulty` (integer, optional): The difficulty level to add.
- `category` (integer, optional): The category ID to add.

**Response Body:**
```json
{
  "questions": [
    {
      "id": 1,
      "question": "What is the largest planet in our solar system?",
      "answer": "Jupiter",
      "category": 1,
      "difficulty": 3
    },
    {
      "id": 2,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 3,
      "difficulty": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

**Response Codes:**
- `200`: Questions retrieved successfully.
- `404`: No questions found.
- `500`: Internal server error.
- `503`: Service unavailable.
- `504`: Gateway timeout.
- `505`: HTTP version not supported.
- `511`: Network authentication required.
- `599`: Network connect timeout error.
- `600`: Unparseable response headers.
- `601`: Network read timeout error.
- `602`: Network connect timeout error.


### GET /api/categories/{id}/questions

**URL:** `/api/categories/{id}/questions`

**Method:** `GET`

**Description:** Fetches questions for a category specified by the ID.

**Request Arguments:**
- `id` (integer): The ID of the category for which to retrieve questions.
- `category` (string, optional): The category to filter questions by.
- `difficulty` (integer, optional): The difficulty level to filter questions by.
- `searchTerm` (string, optional): The search term to filter questions by.
- `previous_questions` (list, optional): The list of previous question IDs for the quiz.
- `quiz_category` (string, optional): The category for the quiz.
- `question` (string, optional): The question to add.
- `answer` (string, optional): The answer to add.
- `difficulty` (integer, optional): The difficulty level to add.
- `category` (integer, optional): The category ID to add.

**Response Body:**
```json
{
  "questions": [
    {
      "id": 1,
      "question": "What is the largest planet in our solar system?",
      "answer": "Jupiter",
      "category": 1,
      "difficulty": 3
    }
  ],
  "totalQuestions": 1,
  "currentCategory": "Science"
}
```

**Response Codes:**
- `200`: Questions retrieved successfully.
- `404`: No questions found for the specified category.
- `500`: Internal server error.
- `503`: Service unavailable.
- `504`: Gateway timeout.
- `505`: HTTP version not supported.
- `511`: Network authentication required.
- `599`: Network connect timeout error.
- `600`: Unparseable response headers.
- `601`: Network read timeout error.
- `602`: Network connect timeout error.


### DELETE '/api/questions/${id}'
Deletes a specified question using the ID of the question.

#### Request Arguments:
- `id` (integer)

#### Returns:
- Appropriate HTTP status code. Optionally returns the ID of the deleted question.

### POST '/api/quizzes'
Fetches the next question for a quiz.

#### Request Body:
```json
{
  "previous_questions": [1, 4, 20, 15],
  "quiz_category": "current category"
}
```

#### Returns:
```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

### POST '/api/questions'
Adds a new question.

#### Request Body:
```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

#### Returns:
- Does not return any new data.

### POST '/api/questions'
Searches for a specific question by search term.

#### Request Body:
```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

#### Returns:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```
```
This `README.md` file outlines the expected API endpoint behavior, request arguments, 
and returns based on the provided frontend codebase details.

```

----------------------------------------------------------------------------------------------