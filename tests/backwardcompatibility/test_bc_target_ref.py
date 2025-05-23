import unittest
from conductor.client.http.models.target_ref import TargetRef, TargetType


class TestTargetRefBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for TargetRef model.

    Principles:
    ✅ Allow additions (new fields, new enum values)
    ❌ Prevent removals (missing fields, removed enum values)
    ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test fixtures with current valid enum values."""
        self.valid_enum_values = [
            "WORKFLOW_DEF",
            "TASK_DEF",
            "APPLICATION",
            "USER",
            "SECRET",
            "TAG",
            "DOMAIN"
        ]

    def test_class_exists_and_importable(self):
        """Verify TargetRef class still exists and is importable."""
        self.assertTrue(hasattr(TargetRef, '__init__'))
        self.assertTrue(callable(TargetRef))

    def test_target_type_enum_exists_and_importable(self):
        """Verify TargetType enum still exists and is importable."""
        self.assertTrue(hasattr(TargetType, '__members__'))

    def test_existing_enum_values_still_exist(self):
        """Verify all existing TargetType enum values are still present."""
        for expected_value in self.valid_enum_values:
            with self.subTest(enum_value=expected_value):
                # Check enum has the attribute
                self.assertTrue(hasattr(TargetType, expected_value))
                # Check the value is correct
                enum_member = getattr(TargetType, expected_value)
                self.assertEqual(enum_member.value, expected_value)

    def test_no_parameter_constructor_behavior(self):
        """Test the actual behavior when no parameters are provided."""
        # Based on the model, constructor with no params should fail
        # because type=None triggers validation
        with self.assertRaises(ValueError) as context:
            TargetRef()

        # Verify it's the expected validation error
        error_message = str(context.exception)
        self.assertIn("Invalid value for `type` (None)", error_message)

    def test_constructor_signature_backward_compatible(self):
        """Verify constructor still accepts the same parameters that work."""
        # Should work with valid type parameter only
        target_ref = TargetRef(type="WORKFLOW_DEF")
        self.assertIsNotNone(target_ref)

        # Should work with both parameters
        target_ref = TargetRef(type="TASK_DEF", id="test-id")
        self.assertIsNotNone(target_ref)

    def test_constructor_with_only_id_parameter(self):
        """Test constructor behavior when only id is provided."""
        # This should also fail because type defaults to None
        with self.assertRaises(ValueError) as context:
            TargetRef(id="test-id")

        # Verify it's the expected validation error
        error_message = str(context.exception)
        self.assertIn("Invalid value for `type` (None)", error_message)

    def test_required_attributes_exist(self):
        """Verify all existing attributes still exist."""
        target_ref = TargetRef(type="WORKFLOW_DEF")

        # Core attributes must exist
        self.assertTrue(hasattr(target_ref, 'type'))
        self.assertTrue(hasattr(target_ref, 'id'))

        # Internal attributes must exist
        self.assertTrue(hasattr(target_ref, '_type'))
        self.assertTrue(hasattr(target_ref, '_id'))

        # Swagger metadata must exist
        self.assertTrue(hasattr(target_ref, 'swagger_types'))
        self.assertTrue(hasattr(target_ref, 'attribute_map'))
        self.assertTrue(hasattr(target_ref, 'discriminator'))

    def test_swagger_types_structure_unchanged(self):
        """Verify swagger_types contains existing fields with correct types."""
        expected_swagger_types = {
            'type': 'str',
            'id': 'str'
        }

        target_ref = TargetRef(type="APPLICATION")

        # Existing fields must be present with correct types
        for field, expected_type in expected_swagger_types.items():
            with self.subTest(field=field):
                self.assertIn(field, target_ref.swagger_types)
                self.assertEqual(target_ref.swagger_types[field], expected_type)

    def test_attribute_map_structure_unchanged(self):
        """Verify attribute_map contains existing mappings."""
        expected_attribute_map = {
            'type': 'type',
            'id': 'id'
        }

        target_ref = TargetRef(type="USER")

        # Existing mappings must be present
        for attr, expected_json_key in expected_attribute_map.items():
            with self.subTest(attribute=attr):
                self.assertIn(attr, target_ref.attribute_map)
                self.assertEqual(target_ref.attribute_map[attr], expected_json_key)

    def test_type_property_getter_behavior(self):
        """Verify type property getter works as expected."""
        target_ref = TargetRef(type="WORKFLOW_DEF")

        # Should return assigned value
        self.assertEqual(target_ref.type, "WORKFLOW_DEF")

        # Test by setting directly to internal field
        target_ref._type = "TASK_DEF"
        self.assertEqual(target_ref.type, "TASK_DEF")

    def test_id_property_getter_behavior(self):
        """Verify id property getter works as expected."""
        target_ref = TargetRef(type="SECRET")

        # Initially should be None (since we only set type)
        self.assertIsNone(target_ref.id)

        # Should return assigned value
        target_ref._id = "test-id"
        self.assertEqual(target_ref.id, "test-id")

    def test_type_setter_validation_with_valid_values(self):
        """Verify type setter accepts all existing valid enum values."""
        target_ref = TargetRef(type="WORKFLOW_DEF")  # Start with valid value

        for valid_value in self.valid_enum_values:
            with self.subTest(type_value=valid_value):
                # Should not raise exception
                target_ref.type = valid_value
                self.assertEqual(target_ref.type, valid_value)
                self.assertEqual(target_ref._type, valid_value)

    def test_type_setter_validation_rejects_invalid_values(self):
        """Verify type setter still validates and rejects invalid values."""
        target_ref = TargetRef(type="TAG")  # Start with valid value

        invalid_values = ["INVALID", "workflow_def", "", None, 123]

        for invalid_value in invalid_values:
            with self.subTest(invalid_value=invalid_value):
                with self.assertRaises(ValueError) as context:
                    target_ref.type = invalid_value

                # Verify error message format is preserved
                error_message = str(context.exception)
                self.assertIn("Invalid value for `type`", error_message)
                self.assertIn("must be one of", error_message)

    def test_id_setter_behavior_unchanged(self):
        """Verify id setter accepts any value (no validation)."""
        target_ref = TargetRef(type="DOMAIN")  # Start with valid type

        test_values = ["test-id", "", None, 123, [], {}]

        for test_value in test_values:
            with self.subTest(id_value=test_value):
                # Should not raise exception
                target_ref.id = test_value
                self.assertEqual(target_ref.id, test_value)
                self.assertEqual(target_ref._id, test_value)

    def test_constructor_assignment_triggers_validation(self):
        """Verify constructor parameter assignment triggers proper validation."""
        # Valid type should work
        target_ref = TargetRef(type="WORKFLOW_DEF")
        self.assertEqual(target_ref.type, "WORKFLOW_DEF")

        # Invalid type should raise error during construction
        with self.assertRaises(ValueError):
            TargetRef(type="INVALID_TYPE")

        # None type should raise error during construction
        with self.assertRaises(ValueError):
            TargetRef(type=None)

    def test_required_methods_exist_with_correct_signatures(self):
        """Verify all existing methods still exist."""
        target_ref = TargetRef(type="APPLICATION")

        # Core methods must exist and be callable
        self.assertTrue(hasattr(target_ref, 'to_dict'))
        self.assertTrue(callable(target_ref.to_dict))

        self.assertTrue(hasattr(target_ref, 'to_str'))
        self.assertTrue(callable(target_ref.to_str))

        self.assertTrue(hasattr(target_ref, '__repr__'))
        self.assertTrue(callable(target_ref.__repr__))

        self.assertTrue(hasattr(target_ref, '__eq__'))
        self.assertTrue(callable(target_ref.__eq__))

        self.assertTrue(hasattr(target_ref, '__ne__'))
        self.assertTrue(callable(target_ref.__ne__))

    def test_to_dict_method_behavior(self):
        """Verify to_dict method returns expected structure."""
        target_ref = TargetRef(type="APPLICATION", id="app-123")
        result = target_ref.to_dict()

        # Should be a dictionary
        self.assertIsInstance(result, dict)

        # Should contain existing fields
        self.assertIn('type', result)
        self.assertIn('id', result)

        # Values should match
        self.assertEqual(result['type'], "APPLICATION")
        self.assertEqual(result['id'], "app-123")

    def test_equality_comparison_behavior(self):
        """Verify equality comparison works as expected."""
        target_ref1 = TargetRef(type="USER", id="user-123")
        target_ref2 = TargetRef(type="USER", id="user-123")
        target_ref3 = TargetRef(type="USER", id="user-456")

        # Equal objects should be equal
        self.assertEqual(target_ref1, target_ref2)
        self.assertFalse(target_ref1 != target_ref2)

        # Different objects should not be equal
        self.assertNotEqual(target_ref1, target_ref3)
        self.assertTrue(target_ref1 != target_ref3)

        # Comparison with non-TargetRef should return False
        self.assertNotEqual(target_ref1, "not a target ref")
        self.assertTrue(target_ref1 != "not a target ref")

    def test_string_representation_works(self):
        """Verify string representation methods work."""
        target_ref = TargetRef(type="SECRET", id="secret-456")

        # to_str should return a string
        str_result = target_ref.to_str()
        self.assertIsInstance(str_result, str)

        # __repr__ should return a string
        repr_result = repr(target_ref)
        self.assertIsInstance(repr_result, str)

        # They should be the same
        self.assertEqual(str_result, repr_result)


if __name__ == '__main__':
    unittest.main()