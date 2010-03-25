from unittest import TestCase

from common.models import *

class TestModelVariables(TestCase):

    def setUp(self):
        self.user_var = UserVariable("john.doe", "foo")
        self.admin_var = AdminVariable("bar")

    def tearDown(self):
        self.user_var.delete()
        self.admin_var.delete()

    def _testDeleteNonExistingVariable(self, var):
        self.assertEqual(var.get(), None)
        self.user_var.delete()
        self.assertEqual(var.get(), None)

    def testDeleteNonExistingUserVariable(self):
        self._testDeleteNonExistingVariable(self.user_var)

    def testDeleteNonExistingAdminVariable(self):
        self._testDeleteNonExistingVariable(self.admin_var)

    def _testDeleteExistingVariable(self, var):
        var.set("plop")
        var.delete()
        self.assertEqual(var.get(), None)

    def testDeleteExistingUserVariable(self):
        self._testDeleteExistingVariable(self.user_var)

    def testDeleteExistingAdminVariable(self):
        self._testDeleteExistingVariable(self.admin_var)

    def _testGetVariable(self, var):
        ref_value = "plop"
        var.set(ref_value)
        self.assertEqual(var.get(), ref_value)

    def testGetUserVariable(self):
        self._testGetVariable(self.user_var)

    def testGetAdminVariable(self):
        self._testGetVariable(self.admin_var)

    def _testGetVariableDefault(self, var):
        ref_value = "plopi"
        self.assertEqual(var.get(ref_value), ref_value)
        self.assertEqual(var.get(), None)

    def testGetUserVariableDefault(self):
        self._testGetVariableDefault(self.user_var)

    def testGetAdminVariableDefault(self):
        self._testGetVariableDefault(self.admin_var)

    def _testGetVariableSet(self, var):
        ref_value = "plopi"
        self.assertEqual(var.get(ref_value, create=True), ref_value)
        self.assertEqual(var.get(), ref_value)

    def testGetUserVariableSet(self):
        self._testGetVariableSet(self.user_var)

    def testGetAdminVariableSet(self):
        self._testGetVariableSet(self.admin_var)

    def _testSetVariableNoCreate(self, var):
        ref_value = "plopi"
        self.assertRaises(NoSuchVariable, var.set, ref_value, create=False)

    def testSetUserVariableNoCreate(self):
        self._testSetVariableNoCreate(self.user_var)

    def testSetAdminVariableNoCreate(self):
        self._testSetVariableNoCreate(self.admin_var)

TestModelVariables.status = "stable"
TestModelVariables.component = "model"
