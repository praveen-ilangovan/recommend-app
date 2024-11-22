"""

"""

# Local imports
from recommend_app.db.models.user import UserInDb
from recommend_app.db.impl.documents.user import UserDocument
from recommend_app.db.hashing import Hasher

from .. import utils

def test_model_to_document(db_client):
    new_user = utils.create_user()
    document = UserDocument.from_model(new_user)
    assert isinstance(document, UserDocument)
    assert document.email_address == new_user.email_address
    assert Hasher.verify_password(new_user.password, document.password)

def test_document_to_model(db_client):
    new_user = utils.create_user()
    document = UserDocument.from_model(new_user)
    user = document.to_model()
    assert isinstance(user, UserInDb)
    assert user.email_address == new_user.email_address
    assert Hasher.verify_password(new_user.password, user.password)
