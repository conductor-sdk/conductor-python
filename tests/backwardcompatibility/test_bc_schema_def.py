import unittest
from conductor.client.http.models.schema_def import SchemaDef, SchemaType


class TestSchemaDefBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for SchemaDef model.

    These tests ensure:
    - All existing fields remain accessible
    - Field types haven't changed
    - Constructor behavior is preserved
    - Existing enum values work
    - Validation rules remain consistent
    """

    def setUp(self):
        """Set up test fixtures with valid data."""
        self.valid_name = "test_schema"
        self.valid_version = 1
        self.valid_type = SchemaType.JSON
        self.valid_data = {"field1": "value1", "field2": 123}
        self.valid_external_ref = "http://example.com/schema"

    def test_constructor_with_no_args(self):
        """Test that constructor works with no arguments (all defaults)."""
        schema = SchemaDef()

        # Verify all fields are accessible and have expected default values
        self.assertIsNone(schema.name)
        self.assertEqual(schema.version, 1)  # version defaults to 1, not None
        self.assertIsNone(schema.type)
        self.assertIsNone(schema.data)
        self.assertIsNone(schema.external_ref)

    def test_constructor_with_all_args(self):
        """Test constructor with all valid arguments."""
        schema = SchemaDef(
            name=self.valid_name,
            version=self.valid_version,
            type=self.valid_type,
            data=self.valid_data,
            external_ref=self.valid_external_ref
        )

        # Verify all fields are set correctly
        self.assertEqual(schema.name, self.valid_name)
        self.assertEqual(schema.version, self.valid_version)
        self.assertEqual(schema.type, self.valid_type)
        self.assertEqual(schema.data, self.valid_data)
        self.assertEqual(schema.external_ref, self.valid_external_ref)

    def test_default_version_value(self):
        """Test that version defaults to 1 when not specified."""
        schema = SchemaDef()
        self.assertEqual(schema.version, 1)

        # Test explicit None sets version to None
        schema = SchemaDef(version=None)
        self.assertIsNone(schema.version)
        """Test constructor with partial arguments."""
        schema = SchemaDef(name=self.valid_name, version=self.valid_version)

        self.assertEqual(schema.name, self.valid_name)
        self.assertEqual(schema.version, self.valid_version)
        self.assertIsNone(schema.type)
        self.assertIsNone(schema.data)
        self.assertIsNone(schema.external_ref)

    def test_field_existence(self):
        """Test that all expected fields exist and are accessible."""
        schema = SchemaDef()

        # Verify all expected fields exist as properties
        self.assertTrue(hasattr(schema, 'name'))
        self.assertTrue(hasattr(schema, 'version'))
        self.assertTrue(hasattr(schema, 'type'))
        self.assertTrue(hasattr(schema, 'data'))
        self.assertTrue(hasattr(schema, 'external_ref'))

        # Verify private attributes exist
        self.assertTrue(hasattr(schema, '_name'))
        self.assertTrue(hasattr(schema, '_version'))
        self.assertTrue(hasattr(schema, '_type'))
        self.assertTrue(hasattr(schema, '_data'))
        self.assertTrue(hasattr(schema, '_external_ref'))

    def test_property_getters_and_setters(self):
        """Test that all properties have working getters and setters."""
        schema = SchemaDef()

        # Test name property
        schema.name = self.valid_name
        self.assertEqual(schema.name, self.valid_name)

        # Test version property
        schema.version = self.valid_version
        self.assertEqual(schema.version, self.valid_version)

        # Test type property
        schema.type = self.valid_type
        self.assertEqual(schema.type, self.valid_type)

        # Test data property
        schema.data = self.valid_data
        self.assertEqual(schema.data, self.valid_data)

        # Test external_ref property
        schema.external_ref = self.valid_external_ref
        self.assertEqual(schema.external_ref, self.valid_external_ref)

    def test_schema_type_enum_values(self):
        """Test that all expected SchemaType enum values exist and work."""
        # Test that all expected enum values exist
        self.assertTrue(hasattr(SchemaType, 'JSON'))
        self.assertTrue(hasattr(SchemaType, 'AVRO'))
        self.assertTrue(hasattr(SchemaType, 'PROTOBUF'))

        # Test enum values work with the model
        schema = SchemaDef()

        schema.type = SchemaType.JSON
        self.assertEqual(schema.type, SchemaType.JSON)

        schema.type = SchemaType.AVRO
        self.assertEqual(schema.type, SchemaType.AVRO)

        schema.type = SchemaType.PROTOBUF
        self.assertEqual(schema.type, SchemaType.PROTOBUF)

    def test_schema_type_enum_string_representation(self):
        """Test SchemaType enum string representation behavior."""
        self.assertEqual(str(SchemaType.JSON), "JSON")
        self.assertEqual(str(SchemaType.AVRO), "AVRO")
        self.assertEqual(str(SchemaType.PROTOBUF), "PROTOBUF")

    def test_field_type_constraints(self):
        """Test that field types work as expected."""
        schema = SchemaDef()

        # Test name accepts string
        schema.name = "test_string"
        self.assertIsInstance(schema.name, str)

        # Test version accepts int
        schema.version = 42
        self.assertIsInstance(schema.version, int)

        # Test type accepts SchemaType enum
        schema.type = SchemaType.JSON
        self.assertIsInstance(schema.type, SchemaType)

        # Test data accepts dict
        test_dict = {"key": "value"}
        schema.data = test_dict
        self.assertIsInstance(schema.data, dict)

        # Test external_ref accepts string
        schema.external_ref = "http://example.com"
        self.assertIsInstance(schema.external_ref, str)

    def test_to_dict_method(self):
        """Test that to_dict method exists and works correctly."""
        schema = SchemaDef(
            name=self.valid_name,
            version=self.valid_version,
            type=self.valid_type,
            data=self.valid_data,
            external_ref=self.valid_external_ref
        )

        result = schema.to_dict()

        # Verify to_dict returns a dictionary
        self.assertIsInstance(result, dict)

        # Verify all fields are in the result
        self.assertIn('name', result)
        self.assertIn('version', result)
        self.assertIn('type', result)
        self.assertIn('data', result)
        self.assertIn('external_ref', result)

        # Verify values are correct
        self.assertEqual(result['name'], self.valid_name)
        self.assertEqual(result['version'], self.valid_version)
        self.assertEqual(result['type'], self.valid_type)
        self.assertEqual(result['data'], self.valid_data)
        self.assertEqual(result['external_ref'], self.valid_external_ref)

    def test_to_str_method(self):
        """Test that to_str method exists and returns string."""
        schema = SchemaDef(name=self.valid_name)
        result = schema.to_str()

        self.assertIsInstance(result, str)
        self.assertIn(self.valid_name, result)

    def test_repr_method(self):
        """Test that __repr__ method works."""
        schema = SchemaDef(name=self.valid_name)
        result = repr(schema)

        self.assertIsInstance(result, str)
        self.assertIn(self.valid_name, result)

    def test_equality_methods(self):
        """Test __eq__ and __ne__ methods."""
        schema1 = SchemaDef(name="test", version=1)
        schema2 = SchemaDef(name="test", version=1)
        schema3 = SchemaDef(name="different", version=1)

        # Test equality
        self.assertEqual(schema1, schema2)
        self.assertNotEqual(schema1, schema3)

        # Test inequality
        self.assertFalse(schema1 != schema2)
        self.assertTrue(schema1 != schema3)

        # Test comparison with non-SchemaDef object
        self.assertNotEqual(schema1, "not_a_schema")
        self.assertTrue(schema1 != "not_a_schema")

    def test_swagger_types_attribute(self):
        """Test that swagger_types class attribute exists and has expected structure."""
        expected_types = {
            'name': 'str',
            'version': 'int',
            'type': 'str',
            'data': 'dict(str, object)',
            'external_ref': 'str'
        }

        self.assertEqual(SchemaDef.swagger_types, expected_types)

    def test_attribute_map_attribute(self):
        """Test that attribute_map class attribute exists and has expected structure."""
        expected_map = {
            'name': 'name',
            'version': 'version',
            'type': 'type',
            'data': 'data',
            'external_ref': 'externalRef'
        }

        self.assertEqual(SchemaDef.attribute_map, expected_map)

    def test_discriminator_attribute(self):
        """Test that discriminator attribute exists and is accessible."""
        schema = SchemaDef()
        self.assertTrue(hasattr(schema, 'discriminator'))
        self.assertIsNone(schema.discriminator)

    def test_none_value_handling(self):
        """Test that None values are handled correctly."""
        schema = SchemaDef()

        # All fields should accept None
        schema.name = None
        self.assertIsNone(schema.name)

        schema.version = None
        self.assertIsNone(schema.version)

        schema.type = None
        self.assertIsNone(schema.type)

        schema.data = None
        self.assertIsNone(schema.data)

        schema.external_ref = None
        self.assertIsNone(schema.external_ref)

    def test_constructor_parameter_names(self):
        """Test that constructor accepts parameters with expected names."""
        # This ensures parameter names haven't changed
        schema = SchemaDef(
            name="test",
            version=2,
            type=SchemaType.AVRO,
            data={"test": "data"},
            external_ref="ref"
        )

        self.assertEqual(schema.name, "test")
        self.assertEqual(schema.version, 2)
        self.assertEqual(schema.type, SchemaType.AVRO)
        self.assertEqual(schema.data, {"test": "data"})
        self.assertEqual(schema.external_ref, "ref")


if __name__ == '__main__':
    unittest.main()