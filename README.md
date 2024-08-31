# Movie Listing API

## Overview

This project is a movie listing API built using FastAPI. It allows users to list movies, view listed movies, rate them, and add comments. The API is secured using JWT (JSON Web Tokens), ensuring that only the user who listed a movie can edit it. The application is deployed on a cloud platform.

## Features

- **User Authentication:**
  - User registration
  - User login
  - JWT token generation

- **Movie Listing:**
  - View a movie (public access)
  - Add a movie (authenticated access)
  - View all movies (public access)
  - Edit a movie (only by the user who listed it)
  - Delete a movie (only by the user who listed it)

- **Movie Rating:**
  - Rate a movie (authenticated access)
  - Get ratings for a movie (public access)

- **Comments:**
  - Add a comment to a movie (authenticated access)
  - View comments for a movie (public access)
  - Add comment to a comment (nested comments, authenticated access)

## Project Structure
```bash

app/
├── alembic/
│ ├── versions/
│ ├── env.py
│ └── alembic.ini
├── models.py
├── database.py
├── main.py
├── routers/
│ ├── users.py
│ ├── movies.py
│ ├── ratings.py
│ └── comments.py
├── schemas.py
├── logging_config.py
└── tests/
├── test_users.py
├── test_movies.py
├── test_ratings.py
└── test_comments.py

```


## Getting Started

### Prerequisites

- Python 3.11
- PostgreSQL
- Render account for deployment

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    ```bash
    export DATABASE_URL="postgresql://username:password@host:port/dbname"
    export SECRET_KEY="your-secret-key"
    ```

5. Initialize the database:

    ```bash
    alembic upgrade head
    ```

6. Run the application:

    ```bash
    uvicorn app.main:app --reload
    ```