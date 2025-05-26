import unittest
from conductor.client.http.models.action import Action


class TestActionBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for Action model.

    Principles:
    - ✅ Allow additions (new fields, new enum values)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test fixtures with known baseline configuration."""
        self.baseline_swagger_types = {
            'action': 'str',
            'start_workflow': 'StartWorkflow',
            'complete_task': 'TaskDetails',
            'fail_task': 'TaskDetails',
            'expand_inline_json': 'bool'
        }

        self.baseline_attribute_map = {
            'action': 'action',
            'start_workflow': 'start_workflow',
            'complete_task': 'complete_task',
            'fail_task': 'fail_task',
            'expand_inline_json': 'expandInlineJSON'
        }

        self.baseline_allowed_action_values = ["start_workflow", "complete_task", "fail_task"]

    def test_required_fields_exist(self):
        """Verify all baseline fields still exist in the model."""
        action = Action()

        # Check that all baseline swagger_types fields exist
        for field_name in self.baseline_swagger_types.keys():
            self.assertTrue(
                hasattr(action, field_name),
                f"Missing required field: {field_name}"
            )
            self.assertTrue(
                hasattr(action, f"_{field_name}"),
                f"Missing private field: _{field_name}"
            )

    def test_swagger_types_compatibility(self):
        """Verify existing swagger_types haven't changed."""
        current_swagger_types = Action.swagger_types

        # Check all baseline types are preserved
        for field_name, expected_type in self.baseline_swagger_types.items():
            self.assertIn(
                field_name,
                current_swagger_types,
                f"Field {field_name} removed from swagger_types"
            )
            self.assertEqual(
                current_swagger_types[field_name],
                expected_type,
                f"Field {field_name} type changed from {expected_type} to {current_swagger_types[field_name]}"
            )

    def test_attribute_map_compatibility(self):
        """Verify existing attribute_map hasn't changed."""
        current_attribute_map = Action.attribute_map

        # Check all baseline mappings are preserved
        for field_name, expected_json_key in self.baseline_attribute_map.items():
            self.assertIn(
                field_name,
                current_attribute_map,
                f"Field {field_name} removed from attribute_map"
            )
            self.assertEqual(
                current_attribute_map[field_name],
                expected_json_key,
                f"Field {field_name} JSON mapping changed from {expected_json_key} to {current_attribute_map[field_name]}"
            )

    def test_constructor_parameters_compatibility(self):
        """Verify constructor accepts all baseline parameters."""
        # Should be able to create Action with all baseline parameters
        try:
            action = Action(
                action="start_workflow",
                start_workflow=None,
                complete_task=None,
                fail_task=None,
                expand_inline_json=True
            )
            self.assertIsInstance(action, Action)
        except TypeError as e:
            self.fail(f"Constructor signature changed - baseline parameters rejected: {e}")

    def test_property_getters_exist(self):
        """Verify all baseline property getters still exist."""
        action = Action()

        for field_name in self.baseline_swagger_types.keys():
            # Check getter property exists
            self.assertTrue(
                hasattr(Action, field_name),
                f"Missing property getter: {field_name}"
            )
            # Check it's actually a property
            self.assertIsInstance(
                getattr(Action, field_name),
                property,
                f"{field_name} is not a property"
            )

    def test_property_setters_exist(self):
        """Verify all baseline property setters still exist."""
        action = Action()

        for field_name in self.baseline_swagger_types.keys():
            # Check setter exists by trying to access it
            prop = getattr(Action, field_name)
            self.assertIsNotNone(
                prop.fset,
                f"Missing property setter: {field_name}"
            )

    def test_action_enum_validation_compatibility(self):
        """Verify action field validation rules are preserved."""
        action = Action()

        # Test that baseline allowed values still work
        for allowed_value in self.baseline_allowed_action_values:
            try:
                action.action = allowed_value
                self.assertEqual(action.action, allowed_value)
            except ValueError:
                self.fail(f"Previously allowed action value '{allowed_value}' now rejected")

        # Test that invalid values are still rejected
        with self.assertRaises(ValueError):
            action.action = "invalid_action"

    def test_field_type_assignments(self):
        """Verify baseline field types can still be assigned."""
        action = Action()

        # Test string assignment to action
        action.action = "start_workflow"
        self.assertEqual(action.action, "start_workflow")

        # Test boolean assignment to expand_inline_json
        action.expand_inline_json = True
        self.assertTrue(action.expand_inline_json)

        action.expand_inline_json = False
        self.assertFalse(action.expand_inline_json)

    def test_to_dict_method_compatibility(self):
        """Verify to_dict method still works and includes baseline fields."""
        action = Action(
            action="complete_task",
            expand_inline_json=True
        )

        result_dict = action.to_dict()

        # Check method still works
        self.assertIsInstance(result_dict, dict)

        # Check baseline fields are included in output
        expected_fields = set(self.baseline_swagger_types.keys())
        actual_fields = set(result_dict.keys())

        self.assertTrue(
            expected_fields.issubset(actual_fields),
            f"Missing baseline fields in to_dict output: {expected_fields - actual_fields}"
        )

    def test_to_str_method_compatibility(self):
        """Verify to_str method still works."""
        action = Action(action="fail_task")

        try:
            str_result = action.to_str()
            self.assertIsInstance(str_result, str)
        except Exception as e:
            self.fail(f"to_str method failed: {e}")

    def test_equality_methods_compatibility(self):
        """Verify __eq__ and __ne__ methods still work."""
        action1 = Action(action="start_workflow", expand_inline_json=True)
        action2 = Action(action="start_workflow", expand_inline_json=True)
        action3 = Action(action="complete_task", expand_inline_json=False)

        try:
            # Test equality
            self.assertTrue(action1 == action2)
            self.assertFalse(action1 == action3)

            # Test inequality
            self.assertFalse(action1 != action2)
            self.assertTrue(action1 != action3)
        except Exception as e:
            self.fail(f"Equality methods failed: {e}")

    def test_repr_method_compatibility(self):
        """Verify __repr__ method still works."""
        action = Action(action="start_workflow")

        try:
            repr_result = repr(action)
            self.assertIsInstance(repr_result, str)
        except Exception as e:
            self.fail(f"__repr__ method failed: {e}")


if __name__ == '__main__':
    unittest.main()