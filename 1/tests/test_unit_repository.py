import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from models import Contact, User
from crud import get_contact, create_contact, update_contact
from schemas import ContactCreate

class TestRepository(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(id=1, email="test@example.com", hashed_password="hashedpassword")

    def test_get_contact(self):
        contact = Contact(id=1, first_name="John", last_name="Doe", email="john@example.com", owner_id=self.user.id)
        self.db.query().filter().first.return_value = contact

        result = get_contact(self.db, 1)
        self.assertEqual(result, contact)

    def test_create_contact(self):
        contact_data = {"first_name": "Jane", "last_name": "Doe", "email": "jane@example.com", "phone": "1234567890"}
        contact = Contact(id=1, **contact_data, owner_id=self.user.id)

        result = create_contact(self.db, contact)
        self.db.add.assert_called_once_with(contact)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(contact)

        self.assertEqual(result, contact)

    def test_update_contact(self):
        contact = Contact(id=1, first_name="John", last_name="Doe", email="john@example.com", owner_id=self.user.id)
        self.db.query().filter().first.return_value = contact

        updated_data = {"first_name": "Johnny", "last_name": "Doe", "email": "johnny@example.com", "phone": "0987654321"}
        result = update_contact(self.db, 1, ContactCreate(**updated_data))

        self.assertEqual(result.first_name, updated_data["first_name"])
        self.assertEqual(result.email, updated_data["email"])
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(contact)

if __name__ == '__main__':
    unittest.main()
