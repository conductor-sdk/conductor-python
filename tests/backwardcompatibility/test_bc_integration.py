import unittest
from conductor.client.http.models import Integration


class TestIntegrationBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for Integration model.

    Principles:
    - ✅ Allow additions (new fields, new enum values)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test data with valid values."""
        self.valid_category_values = ["API", "AI_MODEL", "VECTOR_DB", "RELATIONAL_DB"]
        self.sample_config = {"key1": "value1", "key2": 123}
        self.sample_tags = []  # Assuming TagObject list, empty for simplicity

    def test_constructor_accepts_all_existing_parameters(self):
        """Test that constructor still accepts all known parameters."""
        # Test with all parameters
        integration = Integration(
            category="API",
            configuration=self.sample_config,
            created_by="test_user",
            created_on=1234567890,
            description="Test integration",
            enabled=True,
            models_count=5,
            name="test_integration",
            tags=self.sample_tags,
            type="webhook",
            updated_by="test_user2",
            updated_on=1234567891
        )

        # Verify all values are set correctly
        self.assertEqual(integration.category, "API")
        self.assertEqual(integration.configuration, self.sample_config)
        self.assertEqual(integration.created_by, "test_user")
        self.assertEqual(integration.created_on, 1234567890)
        self.assertEqual(integration.description, "Test integration")
        self.assertEqual(integration.enabled, True)
        self.assertEqual(integration.models_count, 5)
        self.assertEqual(integration.name, "test_integration")
        self.assertEqual(integration.tags, self.sample_tags)
        self.assertEqual(integration.type, "webhook")
        self.assertEqual(integration.updated_by, "test_user2")
        self.assertEqual(integration.updated_on, 1234567891)

    def test_constructor_with_none_values(self):
        """Test that constructor works with None values (current default behavior)."""
        integration = Integration()

        # All fields should be None initially (based on current implementation)
        self.assertIsNone(integration.category)
        self.assertIsNone(integration.configuration)
        self.assertIsNone(integration.created_by)
        self.assertIsNone(integration.created_on)
        self.assertIsNone(integration.description)
        self.assertIsNone(integration.enabled)
        self.assertIsNone(integration.models_count)
        self.assertIsNone(integration.name)
        self.assertIsNone(integration.tags)
        self.assertIsNone(integration.type)
        self.assertIsNone(integration.updated_by)
        self.assertIsNone(integration.updated_on)

    def test_all_existing_properties_exist(self):
        """Test that all expected properties exist and are accessible."""
        integration = Integration()

        # Test all properties exist (getter)
        expected_properties = [
            'category', 'configuration', 'created_by', 'created_on',
            'description', 'enabled', 'models_count', 'name',
            'tags', 'type', 'updated_by', 'updated_on'
        ]

        for prop in expected_properties:
            # Test getter exists
            self.assertTrue(hasattr(integration, prop), f"Property {prop} should exist")
            # Test getter works
            getattr(integration, prop)

    def test_all_existing_setters_exist_and_work(self):
        """Test that all expected setters exist and work."""
        integration = Integration()

        # Test all setters work
        integration.category = "API"
        integration.configuration = self.sample_config
        integration.created_by = "test_user"
        integration.created_on = 1234567890
        integration.description = "Test description"
        integration.enabled = True
        integration.models_count = 10
        integration.name = "test_name"
        integration.tags = self.sample_tags
        integration.type = "test_type"
        integration.updated_by = "test_user2"
        integration.updated_on = 1234567891

        # Verify values are set
        self.assertEqual(integration.category, "API")
        self.assertEqual(integration.configuration, self.sample_config)
        self.assertEqual(integration.created_by, "test_user")
        self.assertEqual(integration.created_on, 1234567890)
        self.assertEqual(integration.description, "Test description")
        self.assertEqual(integration.enabled, True)
        self.assertEqual(integration.models_count, 10)
        self.assertEqual(integration.name, "test_name")
        self.assertEqual(integration.tags, self.sample_tags)
        self.assertEqual(integration.type, "test_type")
        self.assertEqual(integration.updated_by, "test_user2")
        self.assertEqual(integration.updated_on, 1234567891)

    def test_category_enum_validation_existing_values(self):
        """Test that existing category enum values are still valid."""
        integration = Integration()

        # Test all existing allowed values still work
        for category in self.valid_category_values:
            integration.category = category
            self.assertEqual(integration.category, category)

    def test_category_enum_validation_rejects_invalid_values(self):
        """Test that category validation still rejects invalid values including None."""
        integration = Integration()

        invalid_values = ["INVALID", "api", "database", "", None]

        for invalid_value in invalid_values:
            with self.assertRaises(ValueError, msg=f"Should reject invalid category: {invalid_value}"):
                integration.category = invalid_value

    def test_field_types_unchanged(self):
        """Test that field types haven't changed from expected types."""
        integration = Integration(
            category="API",
            configuration={"key": "value"},
            created_by="user",
            created_on=123456789,
            description="desc",
            enabled=True,
            models_count=5,
            name="name",
            tags=[],
            type="type",
            updated_by="user2",
            updated_on=123456790
        )

        # Test expected types
        self.assertIsInstance(integration.category, str)
        self.assertIsInstance(integration.configuration, dict)
        self.assertIsInstance(integration.created_by, str)
        self.assertIsInstance(integration.created_on, int)
        self.assertIsInstance(integration.description, str)
        self.assertIsInstance(integration.enabled, bool)
        self.assertIsInstance(integration.models_count, int)
        self.assertIsInstance(integration.name, str)
        self.assertIsInstance(integration.tags, list)
        self.assertIsInstance(integration.type, str)
        self.assertIsInstance(integration.updated_by, str)
        self.assertIsInstance(integration.updated_on, int)

    def test_swagger_types_mapping_unchanged(self):
        """Test that swagger_types mapping hasn't changed."""
        expected_swagger_types = {
            'category': 'str',
            'configuration': 'dict(str, object)',
            'created_by': 'str',
            'created_on': 'int',
            'description': 'str',
            'enabled': 'bool',
            'models_count': 'int',
            'name': 'str',
            'tags': 'list[TagObject]',
            'type': 'str',
            'updated_by': 'str',
            'updated_on': 'int'
        }

        # Check all expected keys exist
        for key, expected_type in expected_swagger_types.items():
            self.assertIn(key, Integration.swagger_types, f"swagger_types should contain {key}")
            self.assertEqual(Integration.swagger_types[key], expected_type,
                             f"swagger_types[{key}] should be {expected_type}")

    def test_attribute_map_unchanged(self):
        """Test that attribute_map mapping hasn't changed."""
        expected_attribute_map = {
            'category': 'category',
            'configuration': 'configuration',
            'created_by': 'createdBy',
            'created_on': 'createdOn',
            'description': 'description',
            'enabled': 'enabled',
            'models_count': 'modelsCount',
            'name': 'name',
            'tags': 'tags',
            'type': 'type',
            'updated_by': 'updatedBy',
            'updated_on': 'updatedOn'
        }

        # Check all expected mappings exist
        for key, expected_json_key in expected_attribute_map.items():
            self.assertIn(key, Integration.attribute_map, f"attribute_map should contain {key}")
            self.assertEqual(Integration.attribute_map[key], expected_json_key,
                             f"attribute_map[{key}] should be {expected_json_key}")

    def test_to_dict_method_exists_and_works(self):
        """Test that to_dict method exists and works as expected."""
        integration = Integration(
            category="API",
            name="test_integration",
            enabled=True
        )

        result = integration.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['category'], "API")
        self.assertEqual(result['name'], "test_integration")
        self.assertEqual(result['enabled'], True)

    def test_to_str_method_exists_and_works(self):
        """Test that to_str method exists and works."""
        integration = Integration(name="test")
        result = integration.to_str()
        self.assertIsInstance(result, str)

    def test_equality_methods_exist_and_work(self):
        """Test that __eq__ and __ne__ methods exist and work."""
        integration1 = Integration(name="test", category="API")
        integration2 = Integration(name="test", category="API")
        integration3 = Integration(name="different", category="API")

        # Test equality
        self.assertEqual(integration1, integration2)
        self.assertNotEqual(integration1, integration3)

        # Test inequality
        self.assertFalse(integration1 != integration2)
        self.assertTrue(integration1 != integration3)

    def test_repr_method_exists_and_works(self):
        """Test that __repr__ method exists and works."""
        integration = Integration(name="test")
        result = repr(integration)
        self.assertIsInstance(result, str)

    def test_none_assignment_behavior(self):
        """Test None assignment behavior for fields."""
        integration = Integration(category="API", name="test")

        # Category has validation and rejects None
        with self.assertRaises(ValueError):
            integration.category = None

        # Other fields allow None assignment
        integration.configuration = None
        integration.created_by = None
        integration.created_on = None
        integration.description = None
        integration.enabled = None
        integration.models_count = None
        integration.name = None
        integration.tags = None
        integration.type = None
        integration.updated_by = None
        integration.updated_on = None

        # Verify None assignments worked
        self.assertIsNone(integration.configuration)
        self.assertIsNone(integration.name)

    def test_configuration_accepts_dict_with_mixed_types(self):
        """Test that configuration field accepts dict with mixed value types."""
        integration = Integration()

        mixed_config = {
            "string_key": "string_value",
            "int_key": 123,
            "bool_key": True,
            "list_key": [1, 2, 3],
            "dict_key": {"nested": "value"}
        }

        integration.configuration = mixed_config
        self.assertEqual(integration.configuration, mixed_config)


if __name__ == '__main__':
    unittest.main()