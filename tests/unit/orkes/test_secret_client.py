import logging
import unittest

from unittest.mock import patch
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.secret_resource_api import SecretResourceApi
from conductor.client.orkes.orkes_secret_client import OrkesSecretClient
from conductor.client.orkes.models.metadata_tag import MetadataTag

SECRET_KEY = 'ut_secret_key'
SECRET_VALUE = 'ut_secret_value'
ERROR_BODY= '{"message":"No such secret found by key"}'

class TestOrkesSecretClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.secret_client = OrkesSecretClient(configuration)
        
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "secretResourceApi is not of type SecretResourceApi"
        self.assertIsInstance(self.secret_client.secretResourceApi, SecretResourceApi, message)

    @patch.object(SecretResourceApi, 'put_secret')
    def test_putSecret(self, mock):
        self.secret_client.putSecret(SECRET_KEY, SECRET_VALUE)
        mock.assert_called_with(SECRET_VALUE, SECRET_KEY)

    @patch.object(SecretResourceApi, 'get_secret')
    def test_getSecret(self, mock):
        mock.return_value = SECRET_VALUE
        secret = self.secret_client.getSecret(SECRET_KEY)
        mock.assert_called_with(SECRET_KEY)
        self.assertEqual(secret, SECRET_VALUE)

    @patch.object(SecretResourceApi, 'list_all_secret_names')
    def test_listAllSecretNames(self, mock):
        secret_list = ["TEST_SECRET_1", "TEST_SECRET_2"]
        mock.return_value = secret_list
        secret_names = self.secret_client.listAllSecretNames()
        self.assertTrue(mock.called)
        self.assertSetEqual(secret_names, set(secret_list))
        
    @patch.object(SecretResourceApi, 'list_secrets_that_user_can_grant_access_to')
    def test_listSecretsThatUserCanGrantAccessTo(self, mock):
        secret_list = ["TEST_SECRET_1", "TEST_SECRET_2"]
        mock.return_value = secret_list
        secret_names = self.secret_client.listSecretsThatUserCanGrantAccessTo()
        self.assertTrue(mock.called)
        self.assertListEqual(secret_names, secret_list)
    
    @patch.object(SecretResourceApi, 'delete_secret')
    def test_deleteSecret(self, mock):
        self.secret_client.deleteSecret(SECRET_KEY)
        mock.assert_called_with(SECRET_KEY)
    
    @patch.object(SecretResourceApi, 'secret_exists')
    def test_secretExists(self, mock):
        mock.return_value = True
        self.assertTrue(self.secret_client.secretExists(SECRET_KEY))
        mock.assert_called_with(SECRET_KEY)
    
    @patch.object(SecretResourceApi, 'put_tag_for_secret')
    def test_setSecretTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag2 = MetadataTag("tag2", "val2")
        tags = [tag1, tag2]
        self.secret_client.setSecretTags(tags, SECRET_KEY)
        mock.assert_called_with(tags, SECRET_KEY)
        
    @patch.object(SecretResourceApi, 'get_tags')
    def test_getSecretTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag1 = MetadataTag("tag2", "val2")
        mock.return_value = [tag1, tag1]
        tags = self.secret_client.getSecretTags(SECRET_KEY)
        mock.assert_called_with(SECRET_KEY)
        self.assertEqual(len(tags), 2)
    
    @patch.object(SecretResourceApi, 'delete_tag_for_secret')
    def test_deleteSecretTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag2 = MetadataTag("tag2", "val2")
        tags = [tag1, tag2]
        self.secret_client.deleteSecretTags(tags, SECRET_KEY)
        mock.assert_called_with(tags, SECRET_KEY)