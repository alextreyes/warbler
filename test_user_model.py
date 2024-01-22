"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work? and repr"""

        u = User(
            id = 1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()
        expected_repr = f"<User #{u.id}: {u.username}, {u.email}>"

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(repr(u),expected_repr)

    def test_user_model_following(self):
        """test following uses"""
        u1 = User(
            id = 1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            id = 2,
            email="2test@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        u3 = User(
            id = 3,
            email="3test@test.com",
            username="testuser3",
            password="HASHED_PASSWORD3"
        )
        
        db.session.add_all([u1,u2,u3])
        db.session.commit()

        f=Follows(user_being_followed_id= 1, user_following_id= 2)

        

        db.session.add(f)
        db.session.commit()
        self.assertIs(u2.is_following(u1),True)
        self.assertIs(u2.is_following(u3),False)

    def test_user_model_followers(self):
        """test followers uses"""
        u1 = User(
            id = 1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            id = 2,
            email="2test@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        u3 = User(
            id = 3,
            email="3test@test.com",
            username="testuser3",
            password="HASHED_PASSWORD3"
        )
        
        db.session.add_all([u1,u2,u3])
        db.session.commit()

        f=Follows(user_being_followed_id= 1, user_following_id= 2)
        db.session.add(f)
        db.session.commit()

        self.assertIs(u1.is_followed_by(u2),True)
        self.assertIs(u2.is_followed_by(u3),False)

    def test_user_model_signup(self):
        """test signup"""

        a = User.signup( username="testuser" , email= "test@test.com", password="HASHED_PASSWORD",image_url="ola") 
        db.session.commit() 

        b = User.signup(username='testuser', email='test@test.com', password='HASHED_PASSWORD',image_url="ola")
        db.session.commit()
        
        

        self.assertIsInstance(a,User)
        self.assertIsNone(b)
        db.session.rollback()

    def test_user_model_authenticate(self):
        """test authentication"""
        u1 = User.signup(
            email="test@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            image_url='ola'
        )
        db.session.add(u1)
        db.session.commit()

        self.assertIs(User.authenticate(username='testuser1', password='HASHED_PASSWORD'), u1)

        self.assertIs(User.authenticate(username='testuser1', password='HASHED_PASS'), False)

        self.assertIs(User.authenticate(username='test', password='HASHED_PASS'), False)




