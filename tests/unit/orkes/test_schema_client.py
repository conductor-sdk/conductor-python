import logging
import unittest
from unittest.mock import patch


from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.schema_resource_api import SchemaResourceApi
from conductor.client.http.models.schema_def import SchemaDef
from conductor.client.orkes.orkes_schema_client import OrkesSchemaClient

SCHEMA_NAME = 'ut_schema'
SCHEMA_VERSION = 1


class TestOrkesSchemaClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.schema_client = OrkesSchemaClient(configuration)

    def setUp(self):
        self.schemaDef = SchemaDef(name=SCHEMA_NAME, version=SCHEMA_VERSION, data={})
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "schemaApi is not of type SchemaApi"
        self.assertIsInstance(self.schema_client.schemaApi, SchemaResourceApi, message)

    @patch.object(SchemaResourceApi, 'save')
    def test_registerSchema(self, mock):
        self.schema_client.register_schema(self.schemaDef)
        self.assertTrue(mock.called)
        mock.assert_called_with(self.schemaDef)

    @patch.object(SchemaResourceApi, 'get_schema_by_name_and_version')
    def test_getSchema(self, mock):
        mock.return_value = self.schemaDef
        schema = self.schema_client.get_schema(SCHEMA_NAME, SCHEMA_VERSION)
        self.assertEqual(schema, self.schemaDef)
        mock.assert_called_with(name=SCHEMA_NAME, version=SCHEMA_VERSION)

    @patch.object(SchemaResourceApi, 'get_all_schemas')
    def test_getAllSchemas(self, mock):
        schemaDef2 = SchemaDef(name='ut_schema_2', version=1)
        mock.return_value = [self.schemaDef, schemaDef2]
        schemas = self.schema_client.get_all_schemas()
        self.assertEqual(len(schemas), 2)

    @patch.object(SchemaResourceApi, 'delete_schema_by_name_and_version')
    def test_deleteSchema(self, mock):
        self.schema_client.delete_schema(SCHEMA_NAME, SCHEMA_VERSION)
        self.assertTrue(mock.called)
        mock.assert_called_with(name=SCHEMA_NAME, version=SCHEMA_VERSION)

    @patch.object(SchemaResourceApi, 'delete_schema_by_name')
    def test_deleteSchemaByName(self, mock):
        self.schema_client.delete_schema_by_name(SCHEMA_NAME)
        self.assertTrue(mock.called)
        mock.assert_called_with(name=SCHEMA_NAME)

