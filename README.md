# Recommend

## _Organize, Share, and Inspire: Your Favorites, Simplified._

Recommend is a platform that allows users to organize and share their favorite items across various categories, such as movies, books, hotels, recipes, and more.

Users can create customizable boards, where each board holds multiple cards representing individual items. Boards can be shared with other users, enabling collaborative recommendations and discovery of new content on specific topics. The app fosters a community of sharing and personalized recommendations.

- **Github repository**: <https://github.com/praveen-ilangovan/recommend-app/>

## Tech

 - Python
 - Poetry
 - MongoDB
 - Beanie ODM
 - FastAPI
 - Jinja2

## Quickstart

 - Clone the repo
 - CD into it.

### Running locally

 - Create a .env file inside the repo.
 - It must have the keys listed in [env_example.txt](env_example.txt)
 - Make sure the values are wrapped within double quotes

```sh
DB_URL=""
DB_USER_ID=""
DB_PASSWORD=""
DB_NAME="RecommendDB"
PORT="8000"
```

 - Install the application and run it.

```sh
make install
poetry run app
```

### Running inside a container

 - Create a .env_docker file inside the repo.
 - It must have the keys listed in [.env_docker_example](.env_docker_example)
 - Make sure the values are not wrapped within quotes

```sh
DB_URL=
DB_USER_ID=
DB_PASSWORD=
DB_NAME=RecommendDB
PORT=8000
```

 - Run these commands

```sh
make dbuild
make drun

(or)

docker build -t praveen/recommend-app .
docker run --rm -it --env-file=.env_docker -p 8000:8000 praveen/recommend-app
```

Application should start running @ http://127.0.0.1:8000/

### API Endpoints

 * ME
    - [[GET] /me/](http://127.0.0.1:8000/me/) : Returns the signed in user data and their boards

 * Users
    - [[POST] /users/](http://127.0.0.1:8000/users) : Create a new user in the database
    - [[GET] /users/{user_id}](http://127.0.0.1:8000/users/{id}) : Returns the public boards of the user
    - [[PUT] /users/{user_id}](http://127.0.0.1:8000/users/{id}) : Update user info like first and last name and password

 * Session
    - [[POST] /session/](http://127.0.0.1:8000/session) : Create a new session using the login details of the user. An access token is created.
    - [[DELETE] /session/](http://127.0.0.1:8000/session/logout) : Ends the current session

 * Boards
    - [[POST] /boards/](http://127.0.0.1:8000/boards) : Creates a new board in the database
    - [[GET] /boards/{board_id}](http://127.0.0.1:8000/boards/{id}) : Returns the board data
    - [[PUT] /boards/{board_id}](http://127.0.0.1:8000/boards/{id}) : Updates the board data. Again, only the owner can update.
    - [[DELETE] /boards/{board_id}](http://127.0.0.1:8000/boards/{id}) : Deletes the board. Only the owner can delete the board.

 * Cards
    - [[POST] /boards/{board_id}/cards](http://127.0.0.1:8000/boards/{id}/cards) : Creates a new card
    - [[GET] /cards/{card_id}](http://127.0.0.1:8000/cards/{id}) : Returns the card
    - [[PUT] /cards/{card_id}](http://127.0.0.1:8000/cards/{id}) : Update the card
    - [[DELETE] /cards/{card_id}](http://127.0.0.1:8000/cards/{id}) : Delete the card

 * Scrapper
    - [[GET] /scrapper/?url={url}](http://127.0.0.1:8000/scrapper/?url={url}) : Scraps the data from the URL

 * Internal [For internal dev purposes. Renders using jinja template]
    - [[GET] /internal/](http://127.0.0.1:8000/internal) : Landing page
    - [[GET] /internal/health](http://127.0.0.1:8000/internal/health) : Health page
    - [[GET] /internal/users/new](http://127.0.0.1:8000/internal/users/new) : User registration page
    - [[GET] /internal/users/{id}](http://127.0.0.1:8000/internal/users/{id}) : User page
    - [[GET] /internal/session/new](http://127.0.0.1:8000/internal/session/new) : Login page
    - [[GET] /internal/boards/new](http://127.0.0.1:8000/internal/boards/new) : Create a board page
    - [[GET] /internal/boards/{board_id}](http://127.0.0.1:8000/internal/boards/new) : Board page
    - [[GET] /internal/boards/{board_id}/cards/new](http://127.0.0.1:8000/internal/boards/{id}/cards/new) : Create card page
    - [[GET] /internal/cards/{card_id}](http://127.0.0.1:8000/internal/cards/{id}) : Card page


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

    await client.disconnect()

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

## Chrome Extension

To add the url of the curret tab in your chrome browser as a card to a board, you could use this [extension](https://github.com/praveen-ilangovan/recommend-app-chrome-extension). You should have the app running locally for the extension to work.

## Next steps

 - Redesign UI with React
 - Deploy the code
