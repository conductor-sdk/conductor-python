import unittest
import sys
from unittest.mock import patch

# Import the model class - adjust this import path as needed for your project structure
try:
    from conductor.client.http.models.prompt_test_request import PromptTemplateTestRequest
except ImportError:
    try:
        from conductor.client.http.models import PromptTemplateTestRequest
    except ImportError:
        # If both fail, import directly from the file
        import os
        import importlib.util

        # Get the path to the prompt_test_request.py file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        module_path = os.path.join(current_dir, '..', '..', 'prompt_test_request.py')

        if os.path.exists(module_path):
            spec = importlib.util.spec_from_file_location("prompt_test_request", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            PromptTemplateTestRequest = module.PromptTemplateTestRequest
        else:
            raise ImportError("Could not find PromptTemplateTestRequest class")


class TestPromptTemplateTestRequestBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for PromptTemplateTestRequest model.

    Ensures:
    - ✅ Allow additions (new fields, new enum values)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test fixtures with known valid data."""
        self.valid_data = {
            'llm_provider': 'openai',
            'model': 'gpt-4',
            'prompt': 'Test prompt',
            'prompt_variables': {'var1': 'value1', 'var2': 42},
            'stop_words': ['stop1', 'stop2'],
            'temperature': 0.7,
            'top_p': 0.9
        }

    def test_class_exists(self):
        """Verify the class still exists and is importable."""
        self.assertIsNotNone(PromptTemplateTestRequest)
        self.assertTrue(callable(PromptTemplateTestRequest))
        self.assertEqual(PromptTemplateTestRequest.__name__, 'PromptTemplateTestRequest')

    def test_constructor_signature_backward_compatible(self):
        """Verify constructor accepts all existing parameters with defaults."""
        # Should work with no parameters (all defaults)
        obj = PromptTemplateTestRequest()
        self.assertIsInstance(obj, PromptTemplateTestRequest)

        # Should work with all original parameters
        obj = PromptTemplateTestRequest(
            llm_provider='openai',
            model='gpt-4',
            prompt='test',
            prompt_variables={'key': 'value'},
            stop_words=['stop'],
            temperature=0.5,
            top_p=0.8
        )
        self.assertIsInstance(obj, PromptTemplateTestRequest)

    def test_all_existing_properties_exist(self):
        """Verify all known properties still exist."""
        obj = PromptTemplateTestRequest()

        # Test property existence
        expected_properties = [
            'llm_provider', 'model', 'prompt', 'prompt_variables',
            'stop_words', 'temperature', 'top_p'
        ]

        for prop in expected_properties:
            with self.subTest(property=prop):
                self.assertTrue(hasattr(obj, prop), f"Property '{prop}' missing")
                # Verify property is readable
                value = getattr(obj, prop)
                # Should not raise exception

    def test_property_getters_return_correct_types(self):
        """Verify property getters return expected types."""
        obj = PromptTemplateTestRequest(**self.valid_data)

        # Test each property returns expected type
        type_checks = [
            ('llm_provider', str),
            ('model', str),
            ('prompt', str),
            ('prompt_variables', dict),
            ('stop_words', list),
            ('temperature', (int, float)),  # Allow both int and float
            ('top_p', (int, float))
        ]

        for prop_name, expected_type in type_checks:
            with self.subTest(property=prop_name):
                value = getattr(obj, prop_name)
                self.assertIsInstance(value, expected_type,
                                      f"Property '{prop_name}' should be {expected_type}, got {type(value)}")

    def test_property_setters_work(self):
        """Verify all property setters still work."""
        obj = PromptTemplateTestRequest()

        # Test setting each property
        test_values = {
            'llm_provider': 'anthropic',
            'model': 'claude-3',
            'prompt': 'New prompt',
            'prompt_variables': {'new_key': 'new_value'},
            'stop_words': ['new_stop'],
            'temperature': 0.3,
            'top_p': 0.95
        }

        for prop_name, test_value in test_values.items():
            with self.subTest(property=prop_name):
                setattr(obj, prop_name, test_value)
                retrieved_value = getattr(obj, prop_name)
                self.assertEqual(retrieved_value, test_value,
                                 f"Property '{prop_name}' setter/getter failed")

    def test_swagger_types_dict_exists(self):
        """Verify swagger_types dict still exists with expected structure."""
        self.assertTrue(hasattr(PromptTemplateTestRequest, 'swagger_types'))
        swagger_types = PromptTemplateTestRequest.swagger_types
        self.assertIsInstance(swagger_types, dict)

        # Verify all expected fields are present with correct types
        expected_swagger_types = {
            'llm_provider': 'str',
            'model': 'str',
            'prompt': 'str',
            'prompt_variables': 'dict(str, object)',
            'stop_words': 'list[str]',
            'temperature': 'float',
            'top_p': 'float'
        }

        for field, expected_type in expected_swagger_types.items():
            with self.subTest(field=field):
                self.assertIn(field, swagger_types, f"Field '{field}' missing from swagger_types")
                self.assertEqual(swagger_types[field], expected_type,
                                 f"Field '{field}' type changed from '{expected_type}' to '{swagger_types[field]}'")

    def test_attribute_map_dict_exists(self):
        """Verify attribute_map dict still exists with expected structure."""
        self.assertTrue(hasattr(PromptTemplateTestRequest, 'attribute_map'))
        attribute_map = PromptTemplateTestRequest.attribute_map
        self.assertIsInstance(attribute_map, dict)

        # Verify all expected mappings are present
        expected_attribute_map = {
            'llm_provider': 'llmProvider',
            'model': 'model',
            'prompt': 'prompt',
            'prompt_variables': 'promptVariables',
            'stop_words': 'stopWords',
            'temperature': 'temperature',
            'top_p': 'topP'
        }

        for field, expected_json_key in expected_attribute_map.items():
            with self.subTest(field=field):
                self.assertIn(field, attribute_map, f"Field '{field}' missing from attribute_map")
                self.assertEqual(attribute_map[field], expected_json_key,
                                 f"Field '{field}' JSON mapping changed from '{expected_json_key}' to '{attribute_map[field]}'")

    def test_to_dict_method_exists_and_works(self):
        """Verify to_dict method still exists and returns expected structure."""
        obj = PromptTemplateTestRequest(**self.valid_data)

        self.assertTrue(hasattr(obj, 'to_dict'))
        self.assertTrue(callable(obj.to_dict))

        result = obj.to_dict()
        self.assertIsInstance(result, dict)

        # Verify all expected fields are in the result
        expected_fields = ['llm_provider', 'model', 'prompt', 'prompt_variables',
                           'stop_words', 'temperature', 'top_p']

        for field in expected_fields:
            with self.subTest(field=field):
                self.assertIn(field, result, f"Field '{field}' missing from to_dict() result")

    def test_to_str_method_exists_and_works(self):
        """Verify to_str method still exists and returns string."""
        obj = PromptTemplateTestRequest(**self.valid_data)

        self.assertTrue(hasattr(obj, 'to_str'))
        self.assertTrue(callable(obj.to_str))

        result = obj.to_str()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_repr_method_exists_and_works(self):
        """Verify __repr__ method still works."""
        obj = PromptTemplateTestRequest(**self.valid_data)

        result = repr(obj)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_equality_methods_exist_and_work(self):
        """Verify __eq__ and __ne__ methods still work."""
        obj1 = PromptTemplateTestRequest(**self.valid_data)
        obj2 = PromptTemplateTestRequest(**self.valid_data)
        obj3 = PromptTemplateTestRequest(llm_provider='different')

        # Test equality
        self.assertTrue(hasattr(obj1, '__eq__'))
        self.assertEqual(obj1, obj2)
        self.assertNotEqual(obj1, obj3)
        self.assertNotEqual(obj1, "not an object")

        # Test inequality
        self.assertTrue(hasattr(obj1, '__ne__'))
        self.assertFalse(obj1 != obj2)
        self.assertTrue(obj1 != obj3)

    def test_none_values_handling(self):
        """Verify None values are handled correctly (existing behavior)."""
        obj = PromptTemplateTestRequest()

        # All properties should be None by default
        expected_none_properties = [
            'llm_provider', 'model', 'prompt', 'prompt_variables',
            'stop_words', 'temperature', 'top_p'
        ]

        for prop in expected_none_properties:
            with self.subTest(property=prop):
                value = getattr(obj, prop)
                self.assertIsNone(value, f"Property '{prop}' should default to None")

    def test_discriminator_attribute_exists(self):
        """Verify discriminator attribute still exists."""
        obj = PromptTemplateTestRequest()
        self.assertTrue(hasattr(obj, 'discriminator'))
        self.assertIsNone(obj.discriminator)  # Should be None by default

    def test_private_attributes_exist(self):
        """Verify private attributes still exist (internal structure)."""
        obj = PromptTemplateTestRequest()

        expected_private_attrs = [
            '_llm_provider', '_model', '_prompt', '_prompt_variables',
            '_stop_words', '_temperature', '_top_p'
        ]

        for attr in expected_private_attrs:
            with self.subTest(attribute=attr):
                self.assertTrue(hasattr(obj, attr), f"Private attribute '{attr}' missing")

    def test_field_type_validation_constraints(self):
        """Test that existing type constraints are preserved."""
        obj = PromptTemplateTestRequest()

        # Test string fields accept strings
        string_fields = ['llm_provider', 'model', 'prompt']
        for field in string_fields:
            with self.subTest(field=field):
                setattr(obj, field, "test_string")
                self.assertEqual(getattr(obj, field), "test_string")

        # Test dict field accepts dict
        obj.prompt_variables = {"key": "value"}
        self.assertEqual(obj.prompt_variables, {"key": "value"})

        # Test list field accepts list
        obj.stop_words = ["word1", "word2"]
        self.assertEqual(obj.stop_words, ["word1", "word2"])

        # Test numeric fields accept numbers
        obj.temperature = 0.5
        self.assertEqual(obj.temperature, 0.5)

        obj.top_p = 0.9
        self.assertEqual(obj.top_p, 0.9)

    def test_constructor_parameter_order_preserved(self):
        """Verify constructor parameter order hasn't changed."""
        # This test ensures positional arguments still work
        obj = PromptTemplateTestRequest(
            'openai',  # llm_provider
            'gpt-4',  # model
            'test prompt',  # prompt
            {'var': 'val'},  # prompt_variables
            ['stop'],  # stop_words
            0.7,  # temperature
            0.9  # top_p
        )

        self.assertEqual(obj.llm_provider, 'openai')
        self.assertEqual(obj.model, 'gpt-4')
        self.assertEqual(obj.prompt, 'test prompt')
        self.assertEqual(obj.prompt_variables, {'var': 'val'})
        self.assertEqual(obj.stop_words, ['stop'])
        self.assertEqual(obj.temperature, 0.7)
        self.assertEqual(obj.top_p, 0.9)


if __name__ == '__main__':
    unittest.main()