import os
import unittest

from project import app, db
from project._config import BASE_DIR
from project.models import User

TEST_DB = 'test.db'


class MainTests(unittest.TestCase):
    # Setup and teardown
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(BASE_DIR, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # helper method
    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)

    # tests
    def test_404_error(self):
        response = self.app.get('/this-route-doesnt-exists/')
        self.assertEquals(response.status_code, 404)

    def test_500_error(self):
        bad_user = User(
            name='Random',
            email='Random@random.com',
            password='randomize'
        )
        db.session.add(bad_user)
        db.session.commit()
        response = self.login('Random', 'randomize')
        self.assertEquals(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
