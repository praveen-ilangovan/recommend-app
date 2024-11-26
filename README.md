# Recommend

## _Organize, Share, and Inspire: Your Favorites, Simplified._

Recommend is a platform that allows users to organize and share their favorite items across various categories, such as movies, books, hotels, recipes, and more.

Users can create customizable boards, where each board holds multiple cards representing individual items. Boards can be shared with other users, enabling collaborative recommendations and discovery of new content on specific topics. The app fosters a community of sharing and personalized recommendations.

- **Github repository**: <https://github.com/praveen-ilangovan/recommend-app/>

## UNDER ACTIVE DEVELOPMENT

![alt text](resources/under_construction.jpg)

Rethinking the whole idea as a Full Stack App. Gonna rebuild it and this time
parallely working on the API and FE too. This attempt, FE is gonna be written
using Jinja templates. But it will eventually be rewritten using a proper 
framework (React probably)

## Tech

 - Python
 - Poetry
 - MongoDB
 - Beanie ODM
 - FastAPI
 - Jinja2 (eventually will be replaced by React)

## Quickstart

 - Clone the repo
 - CD into it.

### Environment

 - Create a .env file inside the repo.
 - It must have the keys listed in [env_example.txt](env_example.txt)

```sh
DB_URL=""
DB_USER_ID=""
DB_PASSWORD=""
DB_NAME=""
PORT="8000"
```

 - Install the application and run it.

```sh
make install
poetry run app
```

Application should start running @ http://127.0.0.1:8000/

### API Endpoints

 - [GET /health](http://127.0.0.1:8000/health) : Displays if a user is authenticated and database is connected.
 - [GET /users/new](http://127.0.0.1:8000/users/new) : Displays the user registration page
 - [POST /users](http://127.0.0.1:8000/users) : Create a new user in the database
 - [GET /session/new](http://127.0.0.1:8000/session/new) : Displays the user login page
 - [POST /session](http://127.0.0.1:8000/session) : User log in using their credentials
 - [GET /session/logout](http://127.0.0.1:8000/session/logout) : User logouts the current session

### DB backend

```python
import asyncio

from dotenv import load_dotenv

from recommend_app import db
from recommend_app.db.models.user import NewUser
from recommend_app.db.hashing import Hasher

load_dotenv()

async def main():
    client = db.create_client()
    await client.connect()

    # Create a new user
    user = NewUser(
        email_address="johnDoe@mail.com",
        user_name="john.doe",
        first_name="John",
        last_name="Doe",
        password="password123",
    )
    created_user = await client.add_user(user)

    # Get the user
    result = await client.get_user(email_address=user.email_address)

    # Verify the user
    print(Hasher.verify_password("password123", result.password))

asyncio.run(main())
```

## Code quality

- Lint and Format (Ruff)
- Static type checking (mypy)
- Testing (pytest)

Runs ruff and mypy as pre-commit hooks. To run them on demand, use the following
commands

```sh
make check
make test
```
