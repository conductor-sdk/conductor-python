import unittest
from conductor.client.http.models import SubjectRef
from conductor.client.http.models.subject_ref import SubjectType


class TestSubjectRefBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for SubjectRef model.

    Principles:
    ✅ Allow additions (new fields, new enum values)
    ❌ Prevent removals (missing fields, removed enum values)
    ❌ Prevent changes (field type changes, field name changes)
    """

    def test_constructor_signature_compatibility(self):
        """Test that constructor signature remains backward compatible."""
        # Should accept no arguments (all optional)
        obj1 = SubjectRef()
        self.assertIsNone(obj1.type)
        self.assertIsNone(obj1.id)

        # Should accept type only
        obj2 = SubjectRef(type="USER")
        self.assertEqual(obj2.type, "USER")
        self.assertIsNone(obj2.id)

        # Should accept id only
        obj3 = SubjectRef(id="test-id")
        self.assertIsNone(obj3.type)
        self.assertEqual(obj3.id, "test-id")

        # Should accept both parameters
        obj4 = SubjectRef(type="ROLE", id="admin-role")
        self.assertEqual(obj4.type, "ROLE")
        self.assertEqual(obj4.id, "admin-role")

    def test_required_fields_exist(self):
        """Test that all existing fields still exist."""
        obj = SubjectRef()

        # Core fields must exist
        self.assertTrue(hasattr(obj, 'type'))
        self.assertTrue(hasattr(obj, 'id'))

        # Internal fields must exist
        self.assertTrue(hasattr(obj, '_type'))
        self.assertTrue(hasattr(obj, '_id'))

        # Metadata fields must exist
        self.assertTrue(hasattr(obj, 'discriminator'))
        self.assertTrue(hasattr(obj, 'swagger_types'))
        self.assertTrue(hasattr(obj, 'attribute_map'))

    def test_field_types_unchanged(self):
        """Test that field types haven't changed."""
        obj = SubjectRef(type="USER", id="test-id")

        # Type field should be string
        self.assertIsInstance(obj.type, str)

        # ID field should be string
        self.assertIsInstance(obj.id, str)

        # Swagger types metadata unchanged
        expected_types = {'type': 'str', 'id': 'str'}
        self.assertEqual(obj.swagger_types, expected_types)

        # Attribute map unchanged
        expected_map = {'type': 'type', 'id': 'id'}
        self.assertEqual(obj.attribute_map, expected_map)

    def test_type_validation_rules_preserved(self):
        """Test that existing type validation rules still apply."""
        obj = SubjectRef()

        # Valid values should work (existing enum values)
        valid_types = ["USER", "ROLE", "GROUP"]
        for valid_type in valid_types:
            obj.type = valid_type
            self.assertEqual(obj.type, valid_type)

        # Invalid values should raise ValueError
        invalid_types = ["INVALID", "user", "role", "group", "", None, 123, []]
        for invalid_type in invalid_types:
            with self.assertRaises(ValueError) as context:
                obj.type = invalid_type
            self.assertIn("Invalid value for `type`", str(context.exception))
            self.assertIn("must be one of", str(context.exception))

    def test_constructor_validation_behavior(self):
        """Test that constructor validation behavior is preserved."""
        # Constructor with None type should not validate (current behavior)
        obj1 = SubjectRef(type=None, id="test")
        self.assertIsNone(obj1.type)
        self.assertEqual(obj1.id, "test")

        # Constructor with valid type should work
        obj2 = SubjectRef(type="USER", id="test")
        self.assertEqual(obj2.type, "USER")
        self.assertEqual(obj2.id, "test")

        # Constructor with invalid type should raise error
        with self.assertRaises(ValueError):
            SubjectRef(type="INVALID", id="test")

    def test_id_field_no_validation(self):
        """Test that ID field has no validation (current behavior)."""
        obj = SubjectRef()

        # Any value should be acceptable for ID
        test_values = ["test", "", None, 123, [], {}]
        for value in test_values:
            obj.id = value
            self.assertEqual(obj.id, value)

    def test_property_accessors_work(self):
        """Test that property getters and setters still work."""
        obj = SubjectRef()

        # Type property
        obj.type = "USER"
        self.assertEqual(obj.type, "USER")
        self.assertEqual(obj._type, "USER")  # Internal field should match

        # ID property
        obj.id = "test-id"
        self.assertEqual(obj.id, "test-id")
        self.assertEqual(obj._id, "test-id")  # Internal field should match

    def test_core_methods_exist(self):
        """Test that essential methods still exist and work."""
        obj = SubjectRef(type="USER", id="test-id")

        # to_dict method
        self.assertTrue(hasattr(obj, 'to_dict'))
        result_dict = obj.to_dict()
        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict['type'], "USER")
        self.assertEqual(result_dict['id'], "test-id")

        # to_str method
        self.assertTrue(hasattr(obj, 'to_str'))
        result_str = obj.to_str()
        self.assertIsInstance(result_str, str)

        # __repr__ method
        repr_str = repr(obj)
        self.assertIsInstance(repr_str, str)

        # __eq__ method
        obj2 = SubjectRef(type="USER", id="test-id")
        self.assertEqual(obj, obj2)

        # __ne__ method
        obj3 = SubjectRef(type="ROLE", id="test-id")
        self.assertNotEqual(obj, obj3)

    def test_subject_type_enum_compatibility(self):
        """Test that SubjectType enum values are preserved."""
        # Existing enum values must still exist
        self.assertEqual(SubjectType.USER, "USER")
        self.assertEqual(SubjectType.ROLE, "ROLE")
        self.assertEqual(SubjectType.GROUP, "GROUP")

        # Note: TAG is in enum but not in validation - this is current behavior
        self.assertEqual(SubjectType.TAG, "TAG")

        # Enum should be usable with the model
        obj = SubjectRef()
        obj.type = SubjectType.USER.value
        self.assertEqual(obj.type, "USER")

    def test_discriminator_field_preserved(self):
        """Test that discriminator field behavior is preserved."""
        obj = SubjectRef()
        self.assertIsNone(obj.discriminator)  # Should be None by default

        # Should be assignable (if needed for future compatibility)
        obj.discriminator = "test"
        self.assertEqual(obj.discriminator, "test")

    def test_serialization_compatibility(self):
        """Test that serialization format hasn't changed."""
        obj = SubjectRef(type="USER", id="user-123")

        # to_dict should produce expected structure
        expected_dict = {
            'type': 'USER',
            'id': 'user-123'
        }
        self.assertEqual(obj.to_dict(), expected_dict)

    def test_existing_validation_error_format(self):
        """Test that validation error messages haven't changed format."""
        obj = SubjectRef()

        with self.assertRaises(ValueError) as context:
            obj.type = "INVALID"

        error_msg = str(context.exception)
        # Check specific error message format
        self.assertIn("Invalid value for `type` (INVALID)", error_msg)
        self.assertIn("must be one of ['USER', 'ROLE', 'GROUP']", error_msg)

    def test_edge_cases_compatibility(self):
        """Test edge cases that should maintain backward compatibility."""
        # Empty constructor
        obj1 = SubjectRef()
        self.assertIsNone(obj1.type)
        self.assertIsNone(obj1.id)

        # Setting type to None after initialization
        obj2 = SubjectRef(type="USER")
        obj2._type = None  # Direct assignment to bypass setter
        self.assertIsNone(obj2.type)

        # Case sensitivity (should fail)
        with self.assertRaises(ValueError):
            SubjectRef(type="user")  # lowercase should fail


if __name__ == '__main__':
    unittest.main()