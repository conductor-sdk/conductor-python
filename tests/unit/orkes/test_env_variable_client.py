import json
import logging
import unittest
from unittest.mock import patch, MagicMock

from conductor.client.http.rest import ApiException
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.environment_resource_api import EnvironmentResourceApi
from conductor.client.orkes.orkes_env_variable_client import OrkesEnvVariableClient

VARIABLE_KEY = 'ut_env_var_key'
VARIABLE_VALUE = 'ut_env_var_value'
ERROR_BODY = '{"message":"No such environment variable found by key"}'


class TestEnvVariableClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.env_variable_client = OrkesEnvVariableClient(configuration)

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "environmentResourceApi is not of type EnvironmentResourceApi"
        self.assertIsInstance(self.env_variable_client.environmentResourceApi, EnvironmentResourceApi, message)

    @patch.object(EnvironmentResourceApi, 'create_or_update_env_variable')
    def test_save_env_variable(self, mock):
        self.env_variable_client.save_env_variable(VARIABLE_KEY, VARIABLE_VALUE)
        mock.assert_called_with(VARIABLE_VALUE, VARIABLE_KEY)

    @patch.object(EnvironmentResourceApi, 'get1')
    def test_get_env_variable(self, mock):
        mock.return_value = VARIABLE_VALUE
        env_var = self.env_variable_client.get_env_variable(VARIABLE_KEY)
        mock.assert_called_with(VARIABLE_KEY)
        self.assertEqual(env_var, VARIABLE_VALUE)

    @patch.object(EnvironmentResourceApi, 'get1')
    def test_get_variable_non_existing(self, mock):
        error_body = {'status': 404, 'message': 'Variable not found'}
        mock.side_effect = MagicMock(side_effect=ApiException(status=404, body=json.dumps(error_body)))
        with self.assertRaises(ApiException):
            self.env_variable_client.get_env_variable("WRONG_ENV_VAR_KEY")
            mock.assert_called_with("WRONG_ENV_VAR_KEY")

    @patch.object(EnvironmentResourceApi, 'get_all')
    def test_get_all_env_variables(self, mock):
        env_var_dict = { "TEST_VARIABLE_1": "v1", "TEST_VARIABLE_2": "v2" }
        mock.return_value = env_var_dict
        env_variables= self.env_variable_client.get_all_env_variables()
        self.assertTrue(mock.called)
        self.assertDictEqual(env_variables, env_var_dict)

    @patch.object(EnvironmentResourceApi, 'delete_env_variable')
    def test_delete_env_variable(self, mock):
        self.env_variable_client.delete_env_variable(VARIABLE_KEY)
        mock.assert_called_with(VARIABLE_KEY)
