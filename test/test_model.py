from unittest import TestCase

from models import *

class TestModelVariables(TestCase):

    def setUp(self):
        self.user_var = UserVariable("john.doe", "foo")
        self.admin_var = AdminVariable("bar")

    def tearDown(self):
        self.user_var.delete()
        self.admin_var.delete()

    def testGetUserVariable(self):
        ref_value = "plop"
        self.user_var.set(ref_value)
        self.assertEqual(self.user_var.get(), ref_value)

    def testGetUserVariableDefault(self):
        ref_value = "plopi"
        self.assertEqual(self.user_var.get(ref_value), ref_value)
