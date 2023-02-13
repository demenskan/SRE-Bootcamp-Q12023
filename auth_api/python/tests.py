import unittest
from methods import Token, Restricted
#Probar con esta url: https://j2logo.com/tutorial-flask-leccion-12-tests-con-flask-unittest/

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.convert = Token()
        self.validate = Restricted()

    def test_generate_token_admin(self):
        self.assertEqual('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI', self.convert.generate_token('admin', 'secret'))

    def test_generate_token_noadmin(self):
        self.assertEqual('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiZWRpdG9yIn0.4Km_GrMrTIX2xFMjQcrGP9VDhC9jFsnFCjxvBO8Wgio', self.convert.generate_token('noadmin', 'noPow3r'))

    def test_generate_token_bob(self):
        self.assertEqual('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoidmlld2VyIn0.l7pxJXYHlJdtI9RME2UesMzuVjqf-RtzQeLTHomo_Ic', self.convert.generate_token('bob', 'thisIsNotAPasswordBob'))

    def test_generate_token_incorrect_user (self):
        self.assertEqual('user_not_found', self.convert.generate_token('admin2', 'secret'))

    def test_generate_token_incorrect_pass (self):
        self.assertEqual('X(', self.convert.generate_token('admin', 'incorrectpass'))

    def test_access_data(self):
        self.assertEqual('You are under protected data', self.validate.access_data('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI'))

if __name__ == '__main__':
    unittest.main()
