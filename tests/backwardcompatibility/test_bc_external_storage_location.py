import unittest
from conductor.client.http.models.external_storage_location import ExternalStorageLocation


class TestExternalStorageLocationBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for ExternalStorageLocation model.

    Ensures:
    - ✅ Allow additions (new fields, new enum values)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent changes (field type changes, field name changes)
    """

    def test_constructor_with_no_arguments(self):
        """Test that constructor works without any arguments (current behavior)."""
        storage_location = ExternalStorageLocation()
        self.assertIsNotNone(storage_location)
        self.assertIsNone(storage_location.uri)
        self.assertIsNone(storage_location.path)

    def test_constructor_with_all_arguments(self):
        """Test constructor with all known arguments."""
        uri = "s3://my-bucket"
        path = "/data/files"

        storage_location = ExternalStorageLocation(uri=uri, path=path)

        self.assertEqual(storage_location.uri, uri)
        self.assertEqual(storage_location.path, path)

    def test_constructor_with_partial_arguments(self):
        """Test constructor with partial arguments."""
        # Test with only uri
        storage_location1 = ExternalStorageLocation(uri="s3://bucket1")
        self.assertEqual(storage_location1.uri, "s3://bucket1")
        self.assertIsNone(storage_location1.path)

        # Test with only path
        storage_location2 = ExternalStorageLocation(path="/data")
        self.assertIsNone(storage_location2.uri)
        self.assertEqual(storage_location2.path, "/data")

    def test_required_fields_exist(self):
        """Test that all expected fields exist in the model."""
        storage_location = ExternalStorageLocation()

        # These fields must exist for backward compatibility
        required_attributes = ['uri', 'path']

        for attr in required_attributes:
            self.assertTrue(hasattr(storage_location, attr),
                            f"Required attribute '{attr}' is missing")

    def test_field_types_unchanged(self):
        """Test that field types haven't changed."""
        storage_location = ExternalStorageLocation()

        # Verify swagger_types mapping exists and contains expected types
        self.assertTrue(hasattr(ExternalStorageLocation, 'swagger_types'))
        expected_types = {
            'uri': 'str',
            'path': 'str'
        }

        for field, expected_type in expected_types.items():
            self.assertIn(field, ExternalStorageLocation.swagger_types,
                          f"Field '{field}' missing from swagger_types")
            self.assertEqual(ExternalStorageLocation.swagger_types[field], expected_type,
                             f"Field '{field}' type changed from '{expected_type}' to "
                             f"'{ExternalStorageLocation.swagger_types[field]}'")

    def test_attribute_map_unchanged(self):
        """Test that attribute mapping hasn't changed."""
        self.assertTrue(hasattr(ExternalStorageLocation, 'attribute_map'))
        expected_mapping = {
            'uri': 'uri',
            'path': 'path'
        }

        for attr, json_key in expected_mapping.items():
            self.assertIn(attr, ExternalStorageLocation.attribute_map,
                          f"Attribute '{attr}' missing from attribute_map")
            self.assertEqual(ExternalStorageLocation.attribute_map[attr], json_key,
                             f"Attribute mapping for '{attr}' changed")

    def test_uri_property_behavior(self):
        """Test uri property getter and setter behavior."""
        storage_location = ExternalStorageLocation()

        # Test getter when value is None
        self.assertIsNone(storage_location.uri)

        # Test setter with string value
        test_uri = "s3://test-bucket/path"
        storage_location.uri = test_uri
        self.assertEqual(storage_location.uri, test_uri)

        # Test setter with None
        storage_location.uri = None
        self.assertIsNone(storage_location.uri)

    def test_path_property_behavior(self):
        """Test path property getter and setter behavior."""
        storage_location = ExternalStorageLocation()

        # Test getter when value is None
        self.assertIsNone(storage_location.path)

        # Test setter with string value
        test_path = "/data/files/input"
        storage_location.path = test_path
        self.assertEqual(storage_location.path, test_path)

        # Test setter with None
        storage_location.path = None
        self.assertIsNone(storage_location.path)

    def test_to_dict_method_exists_and_works(self):
        """Test that to_dict method exists and produces expected output."""
        storage_location = ExternalStorageLocation(
            uri="s3://bucket",
            path="/data"
        )

        result = storage_location.to_dict()
        self.assertIsInstance(result, dict)

        # Verify expected keys exist in output
        expected_keys = ['uri', 'path']
        for key in expected_keys:
            self.assertIn(key, result)

        self.assertEqual(result['uri'], "s3://bucket")
        self.assertEqual(result['path'], "/data")

    def test_to_str_method_exists(self):
        """Test that to_str method exists and returns string."""
        storage_location = ExternalStorageLocation()
        result = storage_location.to_str()
        self.assertIsInstance(result, str)

    def test_repr_method_exists(self):
        """Test that __repr__ method exists and returns string."""
        storage_location = ExternalStorageLocation()
        result = repr(storage_location)
        self.assertIsInstance(result, str)

    def test_equality_methods_exist(self):
        """Test that equality methods exist and work correctly."""
        storage1 = ExternalStorageLocation(uri="s3://bucket", path="/data")
        storage2 = ExternalStorageLocation(uri="s3://bucket", path="/data")
        storage3 = ExternalStorageLocation(uri="s3://other", path="/data")

        # Test __eq__
        self.assertEqual(storage1, storage2)
        self.assertNotEqual(storage1, storage3)

        # Test __ne__
        self.assertFalse(storage1 != storage2)
        self.assertTrue(storage1 != storage3)

        # Test equality with non-ExternalStorageLocation object
        self.assertNotEqual(storage1, "not_a_storage_location")

    def test_private_attributes_exist(self):
        """Test that private attributes exist (implementation detail preservation)."""
        storage_location = ExternalStorageLocation()

        # These private attributes should exist for backward compatibility
        self.assertTrue(hasattr(storage_location, '_uri'))
        self.assertTrue(hasattr(storage_location, '_path'))
        self.assertTrue(hasattr(storage_location, 'discriminator'))

    def test_string_type_validation(self):
        """Test that string fields accept string values without validation errors."""
        storage_location = ExternalStorageLocation()

        # Test various string values
        string_values = [
            "",  # empty string
            "simple_string",
            "s3://bucket/path/to/file",
            "/absolute/path",
            "relative/path",
            "string with spaces",
            "string-with-dashes",
            "string_with_underscores",
            "http://example.com/path?query=value",
        ]

        for value in string_values:
            # Should not raise any exceptions
            storage_location.uri = value
            self.assertEqual(storage_location.uri, value)

            storage_location.path = value
            self.assertEqual(storage_location.path, value)

    def test_none_values_accepted(self):
        """Test that None values are accepted (current behavior)."""
        storage_location = ExternalStorageLocation()

        # Set to None should work
        storage_location.uri = None
        storage_location.path = None

        self.assertIsNone(storage_location.uri)
        self.assertIsNone(storage_location.path)

    def test_field_independence(self):
        """Test that fields can be set independently."""
        storage_location = ExternalStorageLocation()

        # Set uri only
        storage_location.uri = "s3://bucket"
        self.assertEqual(storage_location.uri, "s3://bucket")
        self.assertIsNone(storage_location.path)

        # Set path only (clear uri first)
        storage_location.uri = None
        storage_location.path = "/data"
        self.assertIsNone(storage_location.uri)
        self.assertEqual(storage_location.path, "/data")

        # Set both
        storage_location.uri = "s3://bucket"
        storage_location.path = "/data"
        self.assertEqual(storage_location.uri, "s3://bucket")
        self.assertEqual(storage_location.path, "/data")


if __name__ == '__main__':
    unittest.main()