import unittest
from conductor.client.http.models import WorkflowSummary


class TestWorkflowSummaryBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for WorkflowSummary model.

    Principles:
    - ✅ Allow additions (new fields, new enum values)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test fixtures with valid values."""
        self.valid_status_values = ["RUNNING", "COMPLETED", "FAILED", "TIMED_OUT", "TERMINATED", "PAUSED"]

        # Valid constructor parameters
        self.valid_params = {
            'workflow_type': 'test_workflow',
            'version': 1,
            'workflow_id': 'wf_123',
            'correlation_id': 'corr_456',
            'start_time': '2025-01-01T00:00:00Z',
            'update_time': '2025-01-01T00:30:00Z',
            'end_time': '2025-01-01T01:00:00Z',
            'status': 'COMPLETED',
            'input': '{"key": "value"}',
            'output': '{"result": "success"}',
            'reason_for_incompletion': None,
            'execution_time': 3600000,
            'event': 'workflow_completed',
            'failed_reference_task_names': None,
            'external_input_payload_storage_path': '/path/to/input',
            'external_output_payload_storage_path': '/path/to/output',
            'priority': 5,
            'created_by': 'user123',
            'output_size': 1024,
            'input_size': 512
        }

    def test_constructor_with_no_parameters(self):
        """Test that constructor works with no parameters (all optional)."""
        workflow = WorkflowSummary()
        self.assertIsNotNone(workflow)

        # All fields should be None initially
        for field_name in self.valid_params.keys():
            self.assertIsNone(getattr(workflow, field_name))

    def test_constructor_with_all_parameters(self):
        """Test constructor with all valid parameters."""
        workflow = WorkflowSummary(**self.valid_params)

        # Verify all values are set correctly
        for field_name, expected_value in self.valid_params.items():
            self.assertEqual(getattr(workflow, field_name), expected_value)

    def test_all_expected_fields_exist(self):
        """Test that all expected fields exist as properties."""
        workflow = WorkflowSummary()

        expected_fields = [
            'workflow_type', 'version', 'workflow_id', 'correlation_id',
            'start_time', 'update_time', 'end_time', 'status', 'input',
            'output', 'reason_for_incompletion', 'execution_time', 'event',
            'failed_reference_task_names', 'external_input_payload_storage_path',
            'external_output_payload_storage_path', 'priority', 'created_by',
            'output_size', 'input_size'
        ]

        for field_name in expected_fields:
            # Test that property exists (both getter and setter)
            self.assertTrue(hasattr(workflow, field_name),
                            f"Field '{field_name}' should exist")

            # Test that we can get the property
            try:
                getattr(workflow, field_name)
            except Exception as e:
                self.fail(f"Getting field '{field_name}' should not raise exception: {e}")

            # Test that we can set the property (use valid value for status field)
            try:
                if field_name == 'status':
                    # Status field has validation, use a valid value
                    setattr(workflow, field_name, 'RUNNING')
                else:
                    setattr(workflow, field_name, None)
            except Exception as e:
                self.fail(f"Setting field '{field_name}' should not raise exception: {e}")

    def test_field_types_unchanged(self):
        """Test that field types haven't changed from expected swagger types."""
        workflow = WorkflowSummary()

        expected_swagger_types = {
            'workflow_type': 'str',
            'version': 'int',
            'workflow_id': 'str',
            'correlation_id': 'str',
            'start_time': 'str',
            'update_time': 'str',
            'end_time': 'str',
            'status': 'str',
            'input': 'str',
            'output': 'str',
            'reason_for_incompletion': 'str',
            'execution_time': 'int',
            'event': 'str',
            'failed_reference_task_names': 'str',
            'external_input_payload_storage_path': 'str',
            'external_output_payload_storage_path': 'str',
            'priority': 'int',
            'created_by': 'str',
            'output_size': 'int',
            'input_size': 'int'
        }

        # Test that swagger_types attribute exists and contains expected types
        self.assertTrue(hasattr(workflow, 'swagger_types'))

        for field_name, expected_type in expected_swagger_types.items():
            self.assertIn(field_name, workflow.swagger_types,
                          f"Field '{field_name}' should be in swagger_types")
            self.assertEqual(workflow.swagger_types[field_name], expected_type,
                             f"Field '{field_name}' should have type '{expected_type}'")

    def test_attribute_map_unchanged(self):
        """Test that attribute mapping hasn't changed."""
        workflow = WorkflowSummary()

        expected_attribute_map = {
            'workflow_type': 'workflowType',
            'version': 'version',
            'workflow_id': 'workflowId',
            'correlation_id': 'correlationId',
            'start_time': 'startTime',
            'update_time': 'updateTime',
            'end_time': 'endTime',
            'status': 'status',
            'input': 'input',
            'output': 'output',
            'reason_for_incompletion': 'reasonForIncompletion',
            'execution_time': 'executionTime',
            'event': 'event',
            'failed_reference_task_names': 'failedReferenceTaskNames',
            'external_input_payload_storage_path': 'externalInputPayloadStoragePath',
            'external_output_payload_storage_path': 'externalOutputPayloadStoragePath',
            'priority': 'priority',
            'created_by': 'createdBy',
            'output_size': 'outputSize',
            'input_size': 'inputSize'
        }

        self.assertTrue(hasattr(workflow, 'attribute_map'))

        for field_name, expected_json_key in expected_attribute_map.items():
            self.assertIn(field_name, workflow.attribute_map,
                          f"Field '{field_name}' should be in attribute_map")
            self.assertEqual(workflow.attribute_map[field_name], expected_json_key,
                             f"Field '{field_name}' should map to '{expected_json_key}'")

    def test_status_enum_values_preserved(self):
        """Test that all existing status enum values are still valid."""
        workflow = WorkflowSummary()

        # Test each known valid status value
        for status_value in self.valid_status_values:
            try:
                workflow.status = status_value
                self.assertEqual(workflow.status, status_value)
            except ValueError as e:
                self.fail(f"Status value '{status_value}' should be valid but got error: {e}")

    def test_status_validation_still_works(self):
        """Test that status validation rejects invalid values."""
        workflow = WorkflowSummary()

        invalid_status_values = ["INVALID", "running", "completed", ""]

        for invalid_status in invalid_status_values:
            with self.assertRaises(ValueError,
                                   msg=f"Status '{invalid_status}' should be rejected"):
                workflow.status = invalid_status

        # Test None separately since it might have different behavior
        with self.assertRaises(ValueError, msg="Status None should be rejected"):
            workflow.status = None

    def test_string_fields_accept_strings(self):
        """Test that string fields accept string values."""
        workflow = WorkflowSummary()

        string_fields = [
            'workflow_type', 'workflow_id', 'correlation_id', 'start_time',
            'update_time', 'end_time', 'input', 'output', 'reason_for_incompletion',
            'event', 'failed_reference_task_names', 'external_input_payload_storage_path',
            'external_output_payload_storage_path', 'created_by'
        ]

        for field_name in string_fields:
            setattr(workflow, field_name, "test_value")
            self.assertEqual(getattr(workflow, field_name), "test_value")

    def test_integer_fields_accept_integers(self):
        """Test that integer fields accept integer values."""
        workflow = WorkflowSummary()

        integer_fields = ['version', 'execution_time', 'priority', 'output_size', 'input_size']

        for field_name in integer_fields:
            setattr(workflow, field_name, 42)
            self.assertEqual(getattr(workflow, field_name), 42)

    def test_to_dict_method_exists(self):
        """Test that to_dict method exists and works."""
        workflow = WorkflowSummary(**self.valid_params)

        self.assertTrue(hasattr(workflow, 'to_dict'))
        result = workflow.to_dict()
        self.assertIsInstance(result, dict)

        # Verify some key fields are in the dict
        for field_name in ['workflow_type', 'version', 'status']:
            self.assertIn(field_name, result)

    def test_to_str_method_exists(self):
        """Test that to_str method exists and works."""
        workflow = WorkflowSummary(**self.valid_params)

        self.assertTrue(hasattr(workflow, 'to_str'))
        result = workflow.to_str()
        self.assertIsInstance(result, str)

    def test_equality_methods_exist(self):
        """Test that equality methods exist and work."""
        workflow1 = WorkflowSummary(**self.valid_params)
        workflow2 = WorkflowSummary(**self.valid_params)
        workflow3 = WorkflowSummary()

        # Test __eq__
        self.assertTrue(hasattr(workflow1, '__eq__'))
        self.assertEqual(workflow1, workflow2)
        self.assertNotEqual(workflow1, workflow3)

        # Test __ne__
        self.assertTrue(hasattr(workflow1, '__ne__'))
        self.assertFalse(workflow1 != workflow2)
        self.assertTrue(workflow1 != workflow3)

    def test_repr_method_exists(self):
        """Test that __repr__ method exists and works."""
        workflow = WorkflowSummary(**self.valid_params)

        self.assertTrue(hasattr(workflow, '__repr__'))
        result = repr(workflow)
        self.assertIsInstance(result, str)

    def test_constructor_parameter_names_unchanged(self):
        """Test that constructor parameter names haven't changed."""
        import inspect

        sig = inspect.signature(WorkflowSummary.__init__)
        param_names = list(sig.parameters.keys())

        # Remove 'self' parameter
        param_names.remove('self')

        expected_params = [
            'workflow_type', 'version', 'workflow_id', 'correlation_id',
            'start_time', 'update_time', 'end_time', 'status', 'input',
            'output', 'reason_for_incompletion', 'execution_time', 'event',
            'failed_reference_task_names', 'external_input_payload_storage_path',
            'external_output_payload_storage_path', 'priority', 'created_by',
            'output_size', 'input_size'
        ]

        for expected_param in expected_params:
            self.assertIn(expected_param, param_names,
                          f"Constructor parameter '{expected_param}' should exist")

    def test_individual_field_setters_work(self):
        """Test that individual field setters work for all fields."""
        workflow = WorkflowSummary()

        # Test setting each field individually
        test_values = {
            'workflow_type': 'test_type',
            'version': 2,
            'workflow_id': 'test_id',
            'correlation_id': 'test_correlation',
            'start_time': '2025-01-01T00:00:00Z',
            'update_time': '2025-01-01T00:30:00Z',
            'end_time': '2025-01-01T01:00:00Z',
            'status': 'RUNNING',
            'input': '{"test": "input"}',
            'output': '{"test": "output"}',
            'reason_for_incompletion': 'test_reason',
            'execution_time': 1000,
            'event': 'test_event',
            'failed_reference_task_names': 'task1,task2',
            'external_input_payload_storage_path': '/test/input/path',
            'external_output_payload_storage_path': '/test/output/path',
            'priority': 10,
            'created_by': 'test_user',
            'output_size': 2048,
            'input_size': 1024
        }

        for field_name, test_value in test_values.items():
            setattr(workflow, field_name, test_value)
            self.assertEqual(getattr(workflow, field_name), test_value,
                             f"Field '{field_name}' should be settable to '{test_value}'")


if __name__ == '__main__':
    unittest.main()