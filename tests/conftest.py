
# Builtin imports
import os

# Project specific imports
import pytest
import pytest_asyncio
import httpx
from asgi_lifespan import LifespanManager

# Local imports
from recommend_app.db import create_client, RecommendDB
from recommend_app.db.models.board import NewBoard

from recommend_app.api.app import app, get_db_client
from recommend_app.api.auth import get_authenticated_user, get_user
from recommend_app.api import constants as Key

from . import utils

#-----------------------------------------------------------------------------#
# Session Scoped Fixtures
#
# For async: https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_session_tests_in_same_loop.html
#-----------------------------------------------------------------------------#

@pytest_asyncio.fixture(loop_scope="session")
async def db_client():
    """
    A fixture that yields the DB client
    """
    client = create_client( RecommendDB(os.environ["DB_NAME"]) )
    await client.connect()

    yield client

    await client.disconnect(clear_db=True)


@pytest_asyncio.fixture(loop_scope="session")
async def WrappedApp(db_client):
    """
    App relies on lifespan events and the AsyncClient doesn't trigger them.
    To ensure they are triggered, use LifespanManager from florimondmanca/asgi-lifespan.

    App takes in the db_client as an input and overrides the db dependency with
    this one.
    """
    app.dependency_overrides[get_db_client] = db_client

    async with LifespanManager(app) as manager:
        yield manager.app

@pytest_asyncio.fixture(loop_scope="session")
async def api_client(WrappedApp):
    """
    The test client we will using in the test. It takes in the wrapped app along
    with the db override.
    """
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=WrappedApp), base_url="http://test") as client:
        yield client

#-----------------------------------------------------------------------------#
# Function scoped fixtures: with different users
#-----------------------------------------------------------------------------#

@pytest.fixture()
def with_authenticated_user():
    app.dependency_overrides[get_authenticated_user] = utils.get_fake_user
    app.dependency_overrides[get_user] = utils.get_fake_user
    yield
    del app.dependency_overrides[get_user]
    del app.dependency_overrides[get_authenticated_user]

@pytest.fixture()
def with_no_signed_in_user():
    get_authenticated_user_override = app.dependency_overrides.get(get_authenticated_user)
    get_user_override = app.dependency_overrides.get(get_user)

    app.dependency_overrides[get_authenticated_user] = utils.get_no_user
    app.dependency_overrides[get_user] = utils.get_no_user

    yield

    if get_authenticated_user_override:
        app.dependency_overrides[get_authenticated_user] = get_authenticated_user_override
    else:
        del app.dependency_overrides[get_authenticated_user]

    if get_user_override:
        app.dependency_overrides[get_user] = get_user_override
    else:
        del app.dependency_overrides[get_user]

@pytest.fixture()
def with_different_user():
    get_authenticated_user_override = app.dependency_overrides.get(get_authenticated_user)
    get_user_override = app.dependency_overrides.get(get_user)

    app.dependency_overrides[get_authenticated_user] = utils.get_another_fake_user
    app.dependency_overrides[get_user] = utils.get_another_fake_user

    yield

    if get_authenticated_user_override:
        app.dependency_overrides[get_authenticated_user] = get_authenticated_user_override
    else:
        del app.dependency_overrides[get_authenticated_user]

    if get_user_override:
        app.dependency_overrides[get_user] = get_user_override
    else:
        del app.dependency_overrides[get_user]


#-----------------------------------------------------------------------------#
# Session scoped: Main fixture: Widely used
#-----------------------------------------------------------------------------#
@pytest_asyncio.fixture(loop_scope="session")
async def api_client_with_boards(api_client, with_authenticated_user):
    board1 = NewBoard(name="Public board")
    response = await api_client.post(Key.ROUTES.ADD_BOARD, json=board1.model_dump())
    public_board = response.json()

    board2 = NewBoard(name="Private board", private=True)
    response2 = await api_client.post(Key.ROUTES.ADD_BOARD, json=board2.model_dump())
    private_board = response2.json()

    card1 = utils.create_card()
    response3 = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = public_board['id']), json=card1.model_dump())
    public_card = response3.json()

    card2 = utils.create_card()
    response4 = await api_client.post(Key.ROUTES.ADD_CARD.format(board_id = private_board['id']), json=card2.model_dump())
    private_card = response4.json()

    return {'api_client': api_client,
            'public_board': public_board,
            'private_board': private_board,
            'card_in_public_board': public_card,
            'card_in_private_board': private_card}
