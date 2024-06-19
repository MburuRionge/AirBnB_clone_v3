#!/usr/bin/python3
"""
Unit Test for DBStorage Class
"""
import unittest
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place


class TestDBStorage(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Tear down test environment"""
        self.storage.close()

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_new(self):
        """Tests that new adds an object to the session"""
        user = User(email="test@example.com", password="password")
        self.storage.new(user)
        self.assertIn(user, self.storage._DBStorage__session)

    def test_save(self):
        """Test that save properly commits to the database"""
        user = User(email="test@example.com", password="password")
        self.storage.new(user)
        self.storage.save()
        self.assertIn(user, self.storage.all().values())


class TestDBStorageDocs(unittest.TestCase):
    """Class for testing DBStorage docs"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For DBStorage Class .....')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = ' Database engine '
        actual = DBStorage.__doc__
        self.assertEqual(expected.strip(), actual.strip())

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'handles long term storage of all class instances'
        actual = DBStorage.__doc__
        self.assertEqual(expected.strip(), actual.strip())

    def test_doc_all(self):
        """... documentation for all function"""
        expected = ' returns a dictionary of all objects '
        actual = DBStorage.all.__doc__
        self.assertEqual(expected.strip(), actual.strip())

    def test_doc_new(self):
        """... documentation for new function"""
        expected = ' adds objects to current database session '
        actual = DBStorage.new.__doc__
        self.assertEqual(expected.strip(), actual.strip())

    def test_doc_save(self):
        """... documentation for save function"""
        expected = ' commits all changes of current database session '
        actual = DBStorage.save.__doc__
        self.assertEqual(expected.strip(), actual.strip())

    def test_doc_reload(self):
        """... documentation for reload function"""
        expected = ' creates all tables in database & session from engine '
        actual = DBStorage.reload.__doc__
        self.assertEqual(expected.strip(), actual.strip())

    def test_doc_delete(self):
        """... documentation for delete function"""
        expected = ' deletes obj from current database session if not None '
        actual = DBStorage.delete.__doc__
        self.assertEqual(expected.strip(), actual.strip())


class TestStateDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('......... Testing DBStorage ....')
        print('........ For State Class ........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new State object for testing"""
        self.storage = DBStorage()
        self.storage.reload()
        self.state = State()
        self.state.name = 'California'
        self.state.save()

    def tearDown(self):
        """Tear down test environment"""
        self.state.delete()
        self.storage.close()

    def test_state_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = self.storage.all()
        all_state_objs = self.storage.all('State')

        exist_in_all = False
        for k in all_objs.keys():
            if self.state.id in k:
                exist_in_all = True
        exist_in_all_states = False
        for k in all_state_objs.keys():
            if self.state.id in k:
                exist_in_all_states = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_states)

    def test_state_delete(self):
        state_id = self.state.id
        self.storage.delete(self.state)
        self.state = None
        self.storage.save()
        exist_in_all = False
        for k in self.storage.all().keys():
            if state_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


class TestUserDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new user for testing"""
        self.storage = DBStorage()
        self.storage.reload()
        self.user = User()
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()

    def tearDown(self):
        """Tear down test environment"""
        self.user.delete()
        self.storage.close()

    def test_user_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = self.storage.all()
        all_user_objs = self.storage.all('User')

        exist_in_all = False
        for k in all_objs.keys():
            if self.user.id in k:
                exist_in_all = True
        exist_in_all_users = False
        for k in all_user_objs.keys():
            if self.user.id in k:
                exist_in_all_users = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_users)

    def test_user_delete(self):
        user_id = self.user.id
        self.storage.delete(self.user)
        self.user = None
        self.storage.save()
        exist_in_all = False
        for k in self.storage.all().keys():
            if user_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


class TestCityDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... City  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new user for testing"""
        self.storage = DBStorage()
        self.storage.reload()
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'Fremont'
        self.city.state_id = self.state.id
        self.city.save()

    def tearDown(self):
        """Tear down test environment"""
        self.city.delete()
        self.state.delete()
        self.storage.close()

    def test_city_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = self.storage.all()
        all_city_objs = self.storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)


class TestCityDBInstancesUnderscore(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... City Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new user for testing"""
        self.storage = DBStorage()
        self.storage.reload()
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'San_Francisco'
        self.city.state_id = self.state.id
        self.city.save()

    def tearDown(self):
        """Tear down test environment"""
        self.city.delete()
        self.state.delete()
        self.storage.close()

    def test_city_underscore_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = self.storage.all()
        all_city_objs = self.storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)
