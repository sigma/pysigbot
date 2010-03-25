from unittest import TestCase

from bot.users import User

class TestUser(TestCase):

    def setUp(self):
        self.user = User("john.doe@example.com")

    def tearDown(self):
        self.user.delete()

    def testNonAdmin(self):
        self.assertEqual(self.user.isAdmin(), False)

    def testMakeAdmin(self):
        self.user.makeAdmin()
        self.assertEqual(self.user.isAdmin(), True)

    def testUserVariable(self):
        var = "plop"
        val = "foo"
        self.user.setVariable(var, val)
        self.assertEqual(self.user.getVariable(var), val)
        self.user.deleteVariable(var)
        self.assertEqual(self.user.getVariable(var), None)

TestUser.status = "stable"
TestUser.component = "user"
