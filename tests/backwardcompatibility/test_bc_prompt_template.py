import unittest
from unittest.mock import Mock
from conductor.client.http.models.prompt_template import PromptTemplate


class TestPromptTemplateBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for PromptTemplate model.

    Ensures that:
    ✅ All existing fields remain accessible
    ✅ Field types remain unchanged
    ✅ Constructor behavior remains consistent
    ✅ Setter validation remains consistent
    ❌ No existing fields are removed
    ❌ No existing field types are changed
    """

    def setUp(self):
        """Set up test fixtures with valid data for all known fields."""
        # Mock TagObject for tags field
        self.mock_tag = Mock()
        self.mock_tag.to_dict.return_value = {"name": "test_tag"}

        # Valid test data for all current fields
        self.valid_data = {
            'created_by': 'test_user',
            'created_on': 1234567890,
            'description': 'Test description',
            'integrations': ['integration1', 'integration2'],
            'name': 'test_template',
            'tags': [self.mock_tag],
            'template': 'Hello {{variable}}',
            'updated_by': 'update_user',
            'updated_on': 1234567899,
            'variables': ['variable1', 'variable2']
        }

    def test_constructor_with_no_parameters(self):
        """Test that constructor works with no parameters (all optional)."""
        template = PromptTemplate()
        self.assertIsInstance(template, PromptTemplate)

        # All fields should be None initially
        self.assertIsNone(template.created_by)
        self.assertIsNone(template.created_on)
        self.assertIsNone(template.description)
        self.assertIsNone(template.integrations)
        self.assertIsNone(template.name)
        self.assertIsNone(template.tags)
        self.assertIsNone(template.template)
        self.assertIsNone(template.updated_by)
        self.assertIsNone(template.updated_on)
        self.assertIsNone(template.variables)

    def test_constructor_with_all_parameters(self):
        """Test constructor with all known parameters."""
        template = PromptTemplate(**self.valid_data)

        # Verify all fields are set correctly
        self.assertEqual(template.created_by, 'test_user')
        self.assertEqual(template.created_on, 1234567890)
        self.assertEqual(template.description, 'Test description')
        self.assertEqual(template.integrations, ['integration1', 'integration2'])
        self.assertEqual(template.name, 'test_template')
        self.assertEqual(template.tags, [self.mock_tag])
        self.assertEqual(template.template, 'Hello {{variable}}')
        self.assertEqual(template.updated_by, 'update_user')
        self.assertEqual(template.updated_on, 1234567899)
        self.assertEqual(template.variables, ['variable1', 'variable2'])

    def test_field_existence_and_accessibility(self):
        """Test that all expected fields exist and are accessible."""
        template = PromptTemplate()

        # Test property getters exist
        expected_fields = [
            'created_by', 'created_on', 'description', 'integrations',
            'name', 'tags', 'template', 'updated_by', 'updated_on', 'variables'
        ]

        for field in expected_fields:
            with self.subTest(field=field):
                # Property should exist and be accessible
                self.assertTrue(hasattr(template, field))
                # Should be able to get the value (even if None)
                getattr(template, field)

    def test_field_types_remain_consistent(self):
        """Test that field types haven't changed."""
        template = PromptTemplate(**self.valid_data)

        # Test string fields
        string_fields = ['created_by', 'description', 'name', 'template', 'updated_by']
        for field in string_fields:
            with self.subTest(field=field):
                value = getattr(template, field)
                self.assertIsInstance(value, str)

        # Test integer fields
        int_fields = ['created_on', 'updated_on']
        for field in int_fields:
            with self.subTest(field=field):
                value = getattr(template, field)
                self.assertIsInstance(value, int)

        # Test list fields
        list_fields = ['integrations', 'tags', 'variables']
        for field in list_fields:
            with self.subTest(field=field):
                value = getattr(template, field)
                self.assertIsInstance(value, list)

    def test_setters_work_correctly(self):
        """Test that all setters work as expected."""
        template = PromptTemplate()

        # Test setting string fields
        template.created_by = 'new_user'
        self.assertEqual(template.created_by, 'new_user')

        template.description = 'new description'
        self.assertEqual(template.description, 'new description')

        template.name = 'new_name'
        self.assertEqual(template.name, 'new_name')

        template.template = 'new template'
        self.assertEqual(template.template, 'new template')

        template.updated_by = 'new_updater'
        self.assertEqual(template.updated_by, 'new_updater')

        # Test setting integer fields
        template.created_on = 9999999999
        self.assertEqual(template.created_on, 9999999999)

        template.updated_on = 8888888888
        self.assertEqual(template.updated_on, 8888888888)

        # Test setting list fields
        template.integrations = ['new_integration']
        self.assertEqual(template.integrations, ['new_integration'])

        template.variables = ['new_var']
        self.assertEqual(template.variables, ['new_var'])

        template.tags = [self.mock_tag]
        self.assertEqual(template.tags, [self.mock_tag])

    def test_none_values_allowed(self):
        """Test that None values are allowed for all fields."""
        template = PromptTemplate(**self.valid_data)

        # All fields should accept None
        fields = [
            'created_by', 'created_on', 'description', 'integrations',
            'name', 'tags', 'template', 'updated_by', 'updated_on', 'variables'
        ]

        for field in fields:
            with self.subTest(field=field):
                setattr(template, field, None)
                self.assertIsNone(getattr(template, field))

    def test_to_dict_method_exists_and_works(self):
        """Test that to_dict method exists and includes all expected fields."""
        template = PromptTemplate(**self.valid_data)
        result = template.to_dict()

        self.assertIsInstance(result, dict)

        # Check that all expected keys are present
        expected_keys = [
            'created_by', 'created_on', 'description', 'integrations',
            'name', 'tags', 'template', 'updated_by', 'updated_on', 'variables'
        ]

        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, result)

    def test_to_str_method_exists(self):
        """Test that to_str method exists and returns string."""
        template = PromptTemplate(**self.valid_data)
        result = template.to_str()
        self.assertIsInstance(result, str)

    def test_repr_method_exists(self):
        """Test that __repr__ method exists and returns string."""
        template = PromptTemplate(**self.valid_data)
        result = repr(template)
        self.assertIsInstance(result, str)

    def test_equality_comparison_works(self):
        """Test that equality comparison works correctly."""
        template1 = PromptTemplate(**self.valid_data)
        template2 = PromptTemplate(**self.valid_data)
        template3 = PromptTemplate(name='different')

        # Equal objects
        self.assertEqual(template1, template2)
        self.assertFalse(template1 != template2)

        # Different objects
        self.assertNotEqual(template1, template3)
        self.assertTrue(template1 != template3)

        # Different type
        self.assertNotEqual(template1, "not a template")

    def test_swagger_types_attribute_exists(self):
        """Test that swagger_types class attribute exists and has expected structure."""
        self.assertTrue(hasattr(PromptTemplate, 'swagger_types'))
        swagger_types = PromptTemplate.swagger_types
        self.assertIsInstance(swagger_types, dict)

        # Check for expected field types
        expected_swagger_types = {
            'created_by': 'str',
            'created_on': 'int',
            'description': 'str',
            'integrations': 'list[str]',
            'name': 'str',
            'tags': 'list[TagObject]',
            'template': 'str',
            'updated_by': 'str',
            'updated_on': 'int',
            'variables': 'list[str]'
        }

        for field, expected_type in expected_swagger_types.items():
            with self.subTest(field=field):
                self.assertIn(field, swagger_types)
                self.assertEqual(swagger_types[field], expected_type)

    def test_attribute_map_exists(self):
        """Test that attribute_map class attribute exists and has expected structure."""
        self.assertTrue(hasattr(PromptTemplate, 'attribute_map'))
        attribute_map = PromptTemplate.attribute_map
        self.assertIsInstance(attribute_map, dict)

        # Check for expected attribute mappings
        expected_mappings = {
            'created_by': 'createdBy',
            'created_on': 'createdOn',
            'description': 'description',
            'integrations': 'integrations',
            'name': 'name',
            'tags': 'tags',
            'template': 'template',
            'updated_by': 'updatedBy',
            'updated_on': 'updatedOn',
            'variables': 'variables'
        }

        for field, expected_mapping in expected_mappings.items():
            with self.subTest(field=field):
                self.assertIn(field, attribute_map)
                self.assertEqual(attribute_map[field], expected_mapping)

    def test_discriminator_attribute_exists(self):
        """Test that discriminator attribute exists and is None."""
        template = PromptTemplate()
        self.assertTrue(hasattr(template, 'discriminator'))
        self.assertIsNone(template.discriminator)

    def test_partial_initialization(self):
        """Test that partial initialization works (only some fields provided)."""
        partial_data = {
            'name': 'partial_template',
            'description': 'partial description'
        }

        template = PromptTemplate(**partial_data)

        # Specified fields should be set
        self.assertEqual(template.name, 'partial_template')
        self.assertEqual(template.description, 'partial description')

        # Other fields should be None
        self.assertIsNone(template.created_by)
        self.assertIsNone(template.integrations)
        self.assertIsNone(template.template)

    def test_list_field_mutation_safety(self):
        """Test that list fields can be safely modified."""
        template = PromptTemplate()

        # Test integrations list
        template.integrations = ['int1']
        template.integrations.append('int2')
        self.assertEqual(template.integrations, ['int1', 'int2'])

        # Test variables list
        template.variables = ['var1']
        template.variables.extend(['var2', 'var3'])
        self.assertEqual(template.variables, ['var1', 'var2', 'var3'])


if __name__ == '__main__':
    unittest.main()