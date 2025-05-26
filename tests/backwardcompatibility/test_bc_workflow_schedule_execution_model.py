import unittest
from conductor.client.http.models import WorkflowScheduleExecutionModel


class TestWorkflowScheduleExecutionModelBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for WorkflowScheduleExecutionModel.

    Ensures that:
    - All existing fields remain accessible
    - Field types haven't changed
    - Existing validation rules still apply
    - Constructor behavior is preserved
    - Enum values are maintained
    """

    def setUp(self):
        """Set up test fixtures with valid data."""
        self.valid_data = {
            'execution_id': 'exec_123',
            'schedule_name': 'daily_schedule',
            'scheduled_time': 1640995200,  # timestamp
            'execution_time': 1640995260,  # timestamp
            'workflow_name': 'test_workflow',
            'workflow_id': 'wf_456',
            'reason': 'scheduled execution',
            'stack_trace': 'stack trace info',
            'start_workflow_request': None,  # StartWorkflowRequest object
            'state': 'EXECUTED'
        }

    def test_constructor_with_all_none_parameters(self):
        """Test that constructor accepts all None values (current behavior)."""
        model = WorkflowScheduleExecutionModel()

        # Verify all fields are None initially
        self.assertIsNone(model.execution_id)
        self.assertIsNone(model.schedule_name)
        self.assertIsNone(model.scheduled_time)
        self.assertIsNone(model.execution_time)
        self.assertIsNone(model.workflow_name)
        self.assertIsNone(model.workflow_id)
        self.assertIsNone(model.reason)
        self.assertIsNone(model.stack_trace)
        self.assertIsNone(model.start_workflow_request)
        self.assertIsNone(model.state)

    def test_constructor_with_valid_parameters(self):
        """Test constructor with all valid parameters."""
        model = WorkflowScheduleExecutionModel(**self.valid_data)

        # Verify all fields are set correctly
        self.assertEqual(model.execution_id, 'exec_123')
        self.assertEqual(model.schedule_name, 'daily_schedule')
        self.assertEqual(model.scheduled_time, 1640995200)
        self.assertEqual(model.execution_time, 1640995260)
        self.assertEqual(model.workflow_name, 'test_workflow')
        self.assertEqual(model.workflow_id, 'wf_456')
        self.assertEqual(model.reason, 'scheduled execution')
        self.assertEqual(model.stack_trace, 'stack trace info')
        self.assertIsNone(model.start_workflow_request)
        self.assertEqual(model.state, 'EXECUTED')

    def test_all_expected_fields_exist(self):
        """Verify all expected fields still exist and are accessible."""
        model = WorkflowScheduleExecutionModel()

        expected_fields = [
            'execution_id', 'schedule_name', 'scheduled_time', 'execution_time',
            'workflow_name', 'workflow_id', 'reason', 'stack_trace',
            'start_workflow_request', 'state'
        ]

        for field in expected_fields:
            with self.subTest(field=field):
                # Test getter exists
                self.assertTrue(hasattr(model, field), f"Field '{field}' missing")
                # Test getter is callable
                getattr(model, field)
                # Test setter exists (property should allow assignment)
                if field == 'state':
                    # state field has validation, use valid value
                    setattr(model, field, 'POLLED')
                else:
                    setattr(model, field, None)

    def test_field_type_consistency(self):
        """Verify field types haven't changed."""
        model = WorkflowScheduleExecutionModel()

        # Test string fields (excluding state which has enum validation)
        string_fields = ['execution_id', 'schedule_name', 'workflow_name',
                         'workflow_id', 'reason', 'stack_trace']

        for field in string_fields:
            with self.subTest(field=field):
                setattr(model, field, "test_string")
                self.assertEqual(getattr(model, field), "test_string")

        # Test state field with valid enum value
        with self.subTest(field='state'):
            setattr(model, 'state', "POLLED")
            self.assertEqual(getattr(model, 'state'), "POLLED")

        # Test integer fields
        int_fields = ['scheduled_time', 'execution_time']
        for field in int_fields:
            with self.subTest(field=field):
                setattr(model, field, 123456)
                self.assertEqual(getattr(model, field), 123456)

    def test_state_enum_validation_preserved(self):
        """Test that state field validation rules are preserved."""
        model = WorkflowScheduleExecutionModel()

        # Test valid enum values still work
        valid_states = ["POLLED", "FAILED", "EXECUTED"]

        for state in valid_states:
            with self.subTest(state=state):
                model.state = state
                self.assertEqual(model.state, state)

        # Test invalid enum values still raise ValueError (including None)
        invalid_states = ["INVALID", "RUNNING", "PENDING", "", None]

        for state in invalid_states:
            with self.subTest(state=state):
                with self.assertRaises(ValueError, msg=f"State '{state}' should raise ValueError"):
                    model.state = state

    def test_attribute_map_preserved(self):
        """Verify attribute_map hasn't changed for existing fields."""
        expected_attribute_map = {
            'execution_id': 'executionId',
            'schedule_name': 'scheduleName',
            'scheduled_time': 'scheduledTime',
            'execution_time': 'executionTime',
            'workflow_name': 'workflowName',
            'workflow_id': 'workflowId',
            'reason': 'reason',
            'stack_trace': 'stackTrace',
            'start_workflow_request': 'startWorkflowRequest',
            'state': 'state'
        }

        actual_attribute_map = WorkflowScheduleExecutionModel.attribute_map

        # Check that all expected mappings exist and are correct
        for field, expected_mapping in expected_attribute_map.items():
            with self.subTest(field=field):
                self.assertIn(field, actual_attribute_map,
                              f"Field '{field}' missing from attribute_map")
                self.assertEqual(actual_attribute_map[field], expected_mapping,
                                 f"Mapping for field '{field}' has changed")

    def test_swagger_types_mapping_preserved(self):
        """Verify swagger_types mapping hasn't changed for existing fields."""
        expected_swagger_types = {
            'execution_id': 'str',
            'schedule_name': 'str',
            'scheduled_time': 'int',
            'execution_time': 'int',
            'workflow_name': 'str',
            'workflow_id': 'str',
            'reason': 'str',
            'stack_trace': 'str',
            'start_workflow_request': 'StartWorkflowRequest',
            'state': 'str'
        }

        actual_swagger_types = WorkflowScheduleExecutionModel.swagger_types

        # Check that all expected fields exist with correct types
        for field, expected_type in expected_swagger_types.items():
            with self.subTest(field=field):
                self.assertIn(field, actual_swagger_types,
                              f"Field '{field}' missing from swagger_types")
                self.assertEqual(actual_swagger_types[field], expected_type,
                                 f"Type for field '{field}' has changed")

    def test_to_dict_method_preserved(self):
        """Test that to_dict method works and returns expected structure."""
        model = WorkflowScheduleExecutionModel(**self.valid_data)
        result = model.to_dict()

        # Verify it returns a dict
        self.assertIsInstance(result, dict)

        # Verify expected keys exist
        expected_keys = set(self.valid_data.keys())
        actual_keys = set(result.keys())

        self.assertTrue(
            expected_keys.issubset(actual_keys),
            f"Missing keys in to_dict: {expected_keys - actual_keys}"
        )

    def test_to_str_method_preserved(self):
        """Test that to_str method works."""
        model = WorkflowScheduleExecutionModel(**self.valid_data)
        result = model.to_str()

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_equality_methods_preserved(self):
        """Test that __eq__ and __ne__ methods work correctly."""
        model1 = WorkflowScheduleExecutionModel(**self.valid_data)
        model2 = WorkflowScheduleExecutionModel(**self.valid_data)
        model3 = WorkflowScheduleExecutionModel()

        # Test equality
        self.assertEqual(model1, model2)
        self.assertNotEqual(model1, model3)

        # Test inequality
        self.assertFalse(model1 != model2)
        self.assertTrue(model1 != model3)

        # Test against non-model objects
        self.assertNotEqual(model1, "not a model")
        self.assertNotEqual(model1, {})

    def test_repr_method_preserved(self):
        """Test that __repr__ method works."""
        model = WorkflowScheduleExecutionModel(**self.valid_data)
        repr_result = repr(model)

        self.assertIsInstance(repr_result, str)
        self.assertGreater(len(repr_result), 0)

    def test_individual_field_assignment(self):
        """Test that individual field assignment still works."""
        model = WorkflowScheduleExecutionModel()

        # Test each field can be set and retrieved
        test_values = {
            'execution_id': 'new_exec_id',
            'schedule_name': 'new_schedule',
            'scheduled_time': 9999999,
            'execution_time': 8888888,
            'workflow_name': 'new_workflow',
            'workflow_id': 'new_wf_id',
            'reason': 'new_reason',
            'stack_trace': 'new_trace',
            'start_workflow_request': None,
            'state': 'POLLED'
        }

        for field, value in test_values.items():
            with self.subTest(field=field):
                setattr(model, field, value)
                self.assertEqual(getattr(model, field), value)

    def test_discriminator_attribute_preserved(self):
        """Test that discriminator attribute exists and is None."""
        model = WorkflowScheduleExecutionModel()
        self.assertTrue(hasattr(model, 'discriminator'))
        self.assertIsNone(model.discriminator)


if __name__ == '__main__':
    unittest.main()