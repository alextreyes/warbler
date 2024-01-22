"""User View tests."""
import os
from unittest import TestCase
from models import db, connect_db, Message, User, Likes, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser3 = User.signup(username="testuser3",
                                    email="test3@test.com",
                                    password="testuser",
                                    image_url=None)                 

        db.session.commit()


    def test_users_page(self):
        """test users page"""
        with self.client as c:
            resp = c.get("/users")

            self.assertIn("testuser",str(resp.data))
            self.assertIn("testuser2",str(resp.data))

    def test_details_page(self):
        """test details page"""
        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser", str(resp.data))
    
    def test_add_like(self):
        m = Message(id=4, text="test", user_id=self.testuser.id)
        db.session.add(m)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/add_like/4", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            likes = Likes.query.filter(Likes.message_id==4).all()
            self.assertEqual(len(likes), 1)
            self.assertEqual(likes[0].user_id, self.testuser.id)

    def setup_followers(self):
        f1 = Follows(user_being_followed_id=self.testuser.id, user_following_id=self.testuser2.id)
        f2 = Follows(user_being_followed_id=self.testuser.id, user_following_id=self.testuser3.id)
        f3 = Follows(user_being_followed_id=self.testuser2.id, user_following_id=self.testuser.id)

        db.session.add_all([f1,f2,f3])
        db.session.commit()

    def test_show_following(self):

        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/users/{self.testuser.id}/following")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser2", str(resp.data))

    def test_show_followers(self):

        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/users/{self.testuser.id}/followers")

            self.assertIn("@testuser2", str(resp.data))

