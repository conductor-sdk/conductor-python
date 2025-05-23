import unittest

from conductor.client.http.models.integration_def import IntegrationDef


class TestIntegrationDefBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for IntegrationDef model.

    Principles:
    - ✅ Allow additions (new fields, new enum values, enhanced types)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent behavioral changes (constructor, properties, methods)

    Focus: Test actual behavioral compatibility, not implementation details.
    """

    def setUp(self):
        """Set up test fixtures with valid data."""
        # Valid enum values based on current model
        self.valid_category_values = ["API", "AI_MODEL", "VECTOR_DB", "RELATIONAL_DB"]

        # Valid test data
        self.valid_data = {
            'category': 'API',
            'category_label': 'API Integration',
            'configuration': {'key': 'value'},
            'description': 'Test integration',
            'enabled': True,
            'icon_name': 'test-icon',
            'name': 'test-integration',
            'tags': ['tag1', 'tag2'],
            'type': 'custom'
        }

    def test_constructor_all_parameters_none(self):
        """Test that constructor works with all parameters as None (current behavior)."""
        integration = IntegrationDef()

        # Verify all fields are initialized to None
        self.assertIsNone(integration.category)
        self.assertIsNone(integration.category_label)
        self.assertIsNone(integration.configuration)
        self.assertIsNone(integration.description)
        self.assertIsNone(integration.enabled)
        self.assertIsNone(integration.icon_name)
        self.assertIsNone(integration.name)
        self.assertIsNone(integration.tags)
        self.assertIsNone(integration.type)

    def test_constructor_with_valid_parameters(self):
        """Test constructor with all valid parameters."""
        integration = IntegrationDef(**self.valid_data)

        # Verify all values are set correctly
        self.assertEqual(integration.category, 'API')
        self.assertEqual(integration.category_label, 'API Integration')
        self.assertEqual(integration.configuration, {'key': 'value'})
        self.assertEqual(integration.description, 'Test integration')
        self.assertEqual(integration.enabled, True)
        self.assertEqual(integration.icon_name, 'test-icon')
        self.assertEqual(integration.name, 'test-integration')
        self.assertEqual(integration.tags, ['tag1', 'tag2'])
        self.assertEqual(integration.type, 'custom')

    def test_all_expected_fields_exist(self):
        """Test that all expected fields exist and are accessible."""
        integration = IntegrationDef()

        # Test field existence via property access
        expected_fields = [
            'category', 'category_label', 'configuration', 'description',
            'enabled', 'icon_name', 'name', 'tags', 'type'
        ]

        for field in expected_fields:
            with self.subTest(field=field):
                # Should not raise AttributeError
                value = getattr(integration, field)
                self.assertIsNone(value)  # Default value should be None

    def test_swagger_types_contains_required_fields(self):
        """Test that swagger_types contains all required fields (allows type evolution)."""
        required_fields = [
            'category', 'category_label', 'configuration', 'description',
            'enabled', 'icon_name', 'name', 'tags', 'type'
        ]

        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, IntegrationDef.swagger_types)
                # Verify it has a type (but don't enforce specific type for compatibility)
                self.assertIsInstance(IntegrationDef.swagger_types[field], str)
                self.assertTrue(len(IntegrationDef.swagger_types[field]) > 0)

    def test_attribute_map_structure(self):
        """Test that attribute_map maintains expected mapping."""
        expected_map = {
            'category': 'category',
            'category_label': 'categoryLabel',
            'configuration': 'configuration',
            'description': 'description',
            'enabled': 'enabled',
            'icon_name': 'iconName',
            'name': 'name',
            'tags': 'tags',
            'type': 'type'
        }

        for field, expected_json_key in expected_map.items():
            with self.subTest(field=field):
                self.assertIn(field, IntegrationDef.attribute_map)
                self.assertEqual(IntegrationDef.attribute_map[field], expected_json_key)

    def test_category_enum_validation(self):
        """Test that category field validates against expected enum values."""
        integration = IntegrationDef()

        # Test valid enum values
        for valid_value in self.valid_category_values:
            with self.subTest(category=valid_value):
                integration.category = valid_value
                self.assertEqual(integration.category, valid_value)

        # Test invalid enum value
        with self.assertRaises(ValueError) as context:
            integration.category = "INVALID_CATEGORY"

        self.assertIn("Invalid value for `category`", str(context.exception))
        self.assertIn("must be one of", str(context.exception))

        # Test None assignment also raises ValueError
        with self.assertRaises(ValueError) as context:
            integration.category = None

        self.assertIn("Invalid value for `category`", str(context.exception))

    def test_category_constructor_validation(self):
        """Test category validation during construction."""
        # Valid category in constructor
        integration = IntegrationDef(category='API')
        self.assertEqual(integration.category, 'API')

        # None category in constructor (should work - validation happens on setter)
        integration_none = IntegrationDef(category=None)
        self.assertIsNone(integration_none.category)

        # Invalid category in constructor
        with self.assertRaises(ValueError):
            IntegrationDef(category='INVALID_CATEGORY')

    def test_field_type_assignments(self):
        """Test that fields accept expected types."""
        integration = IntegrationDef()

        # String fields
        string_fields = ['category_label', 'description', 'icon_name', 'name', 'type']
        for field in string_fields:
            with self.subTest(field=field):
                setattr(integration, field, 'test_value')
                self.assertEqual(getattr(integration, field), 'test_value')

        # Boolean field
        integration.enabled = True
        self.assertEqual(integration.enabled, True)
        integration.enabled = False
        self.assertEqual(integration.enabled, False)

        # Configuration field (should accept dict for backward compatibility)
        test_config = {'key1': 'value1', 'key2': 2}
        integration.configuration = test_config
        self.assertEqual(integration.configuration, test_config)

        # List field
        test_tags = ['tag1', 'tag2', 'tag3']
        integration.tags = test_tags
        self.assertEqual(integration.tags, test_tags)

    def test_configuration_backward_compatibility(self):
        """Test that configuration field maintains backward compatibility with dict input."""
        integration = IntegrationDef()

        # Should accept dictionary (original behavior)
        config_dict = {'api_key': 'secret', 'timeout': 30}
        integration.configuration = config_dict
        self.assertEqual(integration.configuration, config_dict)

        # Should work in constructor
        integration2 = IntegrationDef(configuration={'host': 'localhost'})
        self.assertEqual(integration2.configuration, {'host': 'localhost'})

    def test_to_dict_method_exists(self):
        """Test that to_dict method exists and works."""
        integration = IntegrationDef(**self.valid_data)
        result = integration.to_dict()

        self.assertIsInstance(result, dict)
        # Verify key fields are present in output
        self.assertEqual(result['category'], 'API')
        self.assertEqual(result['name'], 'test-integration')

    def test_to_str_method_exists(self):
        """Test that to_str method exists and works."""
        integration = IntegrationDef(**self.valid_data)
        result = integration.to_str()

        self.assertIsInstance(result, str)
        self.assertIn('API', result)

    def test_equality_methods_exist(self):
        """Test that equality methods exist and work."""
        integration1 = IntegrationDef(**self.valid_data)
        integration2 = IntegrationDef(**self.valid_data)
        integration3 = IntegrationDef(name='different')

        # Test __eq__
        self.assertEqual(integration1, integration2)
        self.assertNotEqual(integration1, integration3)

        # Test __ne__
        self.assertFalse(integration1 != integration2)
        self.assertTrue(integration1 != integration3)

    def test_repr_method_exists(self):
        """Test that __repr__ method exists and works."""
        integration = IntegrationDef(**self.valid_data)
        repr_str = repr(integration)

        self.assertIsInstance(repr_str, str)
        self.assertIn('API', repr_str)

    def test_discriminator_field_exists(self):
        """Test that discriminator field exists (swagger/openapi compatibility)."""
        integration = IntegrationDef()
        self.assertIsNone(integration.discriminator)

    def test_private_attributes_exist(self):
        """Test that private attributes are properly initialized."""
        integration = IntegrationDef()

        # These private attributes should exist
        private_attrs = [
            '_category', '_category_label', '_configuration', '_description',
            '_enabled', '_icon_name', '_name', '_tags', '_type'
        ]

        for attr in private_attrs:
            with self.subTest(attr=attr):
                self.assertTrue(hasattr(integration, attr))
                self.assertIsNone(getattr(integration, attr))

    def test_partial_construction(self):
        """Test construction with only some parameters."""
        integration = IntegrationDef(
            name='partial-test',
            category='API',
            enabled=True
        )

        self.assertEqual(integration.name, 'partial-test')
        self.assertEqual(integration.category, 'API')
        self.assertEqual(integration.enabled, True)
        # Other fields should be None
        self.assertIsNone(integration.description)
        self.assertIsNone(integration.tags)

    def test_none_assignments_behavior(self):
        """Test None assignment behavior for different field types."""
        integration = IntegrationDef(**self.valid_data)

        # Verify initial values are set
        self.assertIsNotNone(integration.category)

        # Category field does NOT allow None assignment (validates against enum)
        with self.assertRaises(ValueError):
            integration.category = None

        # Other fields allow None assignment
        integration.category_label = None
        integration.configuration = None
        integration.description = None
        integration.enabled = None
        integration.icon_name = None
        integration.name = None
        integration.tags = None
        integration.type = None

        # Verify non-category fields can be None
        self.assertIsNone(integration.category_label)
        self.assertIsNone(integration.configuration)
        self.assertIsNone(integration.description)
        self.assertIsNone(integration.enabled)
        self.assertIsNone(integration.icon_name)
        self.assertIsNone(integration.name)
        self.assertIsNone(integration.tags)
        self.assertIsNone(integration.type)

        # Category should still have original value
        self.assertEqual(integration.category, 'API')

    def test_serialization_consistency(self):
        """Test that serialization produces consistent results."""
        integration = IntegrationDef(**self.valid_data)

        # to_dict should work
        dict_result = integration.to_dict()
        self.assertIsInstance(dict_result, dict)

        # Should contain all the expected fields with correct values
        self.assertEqual(dict_result.get('category'), 'API')
        self.assertEqual(dict_result.get('name'), 'test-integration')
        self.assertEqual(dict_result.get('enabled'), True)

        # Configuration should be serialized properly regardless of internal type
        self.assertIsNotNone(dict_result.get('configuration'))

    def test_backward_compatible_construction_patterns(self):
        """Test various construction patterns that existing code might use."""
        # Pattern 1: Positional arguments (if supported)
        try:
            integration1 = IntegrationDef('API', 'API Integration')
            # If this works, verify it
            self.assertEqual(integration1.category, 'API')
        except TypeError:
            # If positional args not supported, that's fine for this version
            pass

        # Pattern 2: Keyword arguments (most common)
        integration2 = IntegrationDef(category='API', name='test')
        self.assertEqual(integration2.category, 'API')
        self.assertEqual(integration2.name, 'test')

        # Pattern 3: Mixed with configuration dict
        integration3 = IntegrationDef(
            category='API',
            configuration={'key': 'value'},
            enabled=True
        )
        self.assertEqual(integration3.category, 'API')
        self.assertEqual(integration3.configuration, {'key': 'value'})
        self.assertEqual(integration3.enabled, True)

    def test_api_contract_stability(self):
        """Test that the public API contract remains stable."""
        integration = IntegrationDef()

        # All expected public methods should exist
        public_methods = ['to_dict', 'to_str', '__eq__', '__ne__', '__repr__']
        for method in public_methods:
            with self.subTest(method=method):
                self.assertTrue(hasattr(integration, method))
                self.assertTrue(callable(getattr(integration, method)))

        # All expected properties should exist and be settable
        properties = [
            'category', 'category_label', 'configuration', 'description',
            'enabled', 'icon_name', 'name', 'tags', 'type'
        ]
        for prop in properties:
            with self.subTest(property=prop):
                # Should be readable
                value = getattr(integration, prop)
                # Should be writable (except category needs valid value)
                if prop == 'category':
                    setattr(integration, prop, 'API')
                    self.assertEqual(getattr(integration, prop), 'API')
                else:
                    setattr(integration, prop, f'test_{prop}')
                    self.assertEqual(getattr(integration, prop), f'test_{prop}')


if __name__ == '__main__':
    unittest.main()