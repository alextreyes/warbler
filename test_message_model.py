"""message model tests."""

import os
from unittest import TestCase
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class MessageModelTestCase(TestCase):
    """Test views for messages"""

    def setUp(self):
        """create test client, add data"""


        self.client = app.test_client()    
    def test_message_model(self):
        """basic model works?"""
    
        msg = Message(text = "hello", user_id = 1 )

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(msg.text,"hello")
        self.assertEqual(msg.user_id,1)