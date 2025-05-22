import unittest
from conductor.client.http.models.task_summary import TaskSummary


class TestTaskSummaryBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for TaskSummary model.

    Principles:
    - ✅ Allow additions (new fields, new enum values)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test fixtures with valid data."""
        self.valid_data = {
            'workflow_id': 'wf_123',
            'workflow_type': 'test_workflow',
            'correlation_id': 'corr_456',
            'scheduled_time': '2024-01-01T10:00:00Z',
            'start_time': '2024-01-01T10:05:00Z',
            'update_time': '2024-01-01T10:10:00Z',
            'end_time': '2024-01-01T10:15:00Z',
            'status': 'COMPLETED',
            'reason_for_incompletion': None,
            'execution_time': 600000,  # milliseconds
            'queue_wait_time': 300000,  # milliseconds
            'task_def_name': 'test_task',
            'task_type': 'SIMPLE',
            'input': '{"key": "value"}',
            'output': '{"result": "success"}',
            'task_id': 'task_789',
            'external_input_payload_storage_path': '/path/to/input',
            'external_output_payload_storage_path': '/path/to/output',
            'workflow_priority': 5
        }

    def test_constructor_accepts_all_current_fields(self):
        """Test that constructor accepts all current fields without error."""
        task_summary = TaskSummary(**self.valid_data)

        # Verify all fields are set correctly
        self.assertEqual(task_summary.workflow_id, 'wf_123')
        self.assertEqual(task_summary.workflow_type, 'test_workflow')
        self.assertEqual(task_summary.correlation_id, 'corr_456')
        self.assertEqual(task_summary.scheduled_time, '2024-01-01T10:00:00Z')
        self.assertEqual(task_summary.start_time, '2024-01-01T10:05:00Z')
        self.assertEqual(task_summary.update_time, '2024-01-01T10:10:00Z')
        self.assertEqual(task_summary.end_time, '2024-01-01T10:15:00Z')
        self.assertEqual(task_summary.status, 'COMPLETED')
        self.assertEqual(task_summary.reason_for_incompletion, None)
        self.assertEqual(task_summary.execution_time, 600000)
        self.assertEqual(task_summary.queue_wait_time, 300000)
        self.assertEqual(task_summary.task_def_name, 'test_task')
        self.assertEqual(task_summary.task_type, 'SIMPLE')
        self.assertEqual(task_summary.input, '{"key": "value"}')
        self.assertEqual(task_summary.output, '{"result": "success"}')
        self.assertEqual(task_summary.task_id, 'task_789')
        self.assertEqual(task_summary.external_input_payload_storage_path, '/path/to/input')
        self.assertEqual(task_summary.external_output_payload_storage_path, '/path/to/output')
        self.assertEqual(task_summary.workflow_priority, 5)

    def test_constructor_with_no_arguments(self):
        """Test that constructor works with no arguments (all fields optional)."""
        task_summary = TaskSummary()

        # All fields should be None initially
        self.assertIsNone(task_summary.workflow_id)
        self.assertIsNone(task_summary.workflow_type)
        self.assertIsNone(task_summary.correlation_id)
        self.assertIsNone(task_summary.scheduled_time)
        self.assertIsNone(task_summary.start_time)
        self.assertIsNone(task_summary.update_time)
        self.assertIsNone(task_summary.end_time)
        self.assertIsNone(task_summary.status)
        self.assertIsNone(task_summary.reason_for_incompletion)
        self.assertIsNone(task_summary.execution_time)
        self.assertIsNone(task_summary.queue_wait_time)
        self.assertIsNone(task_summary.task_def_name)
        self.assertIsNone(task_summary.task_type)
        self.assertIsNone(task_summary.input)
        self.assertIsNone(task_summary.output)
        self.assertIsNone(task_summary.task_id)
        self.assertIsNone(task_summary.external_input_payload_storage_path)
        self.assertIsNone(task_summary.external_output_payload_storage_path)
        self.assertIsNone(task_summary.workflow_priority)

    def test_all_property_getters_exist(self):
        """Test that all property getters exist and return correct types."""
        task_summary = TaskSummary(**self.valid_data)

        # String properties
        self.assertIsInstance(task_summary.workflow_id, str)
        self.assertIsInstance(task_summary.workflow_type, str)
        self.assertIsInstance(task_summary.correlation_id, str)
        self.assertIsInstance(task_summary.scheduled_time, str)
        self.assertIsInstance(task_summary.start_time, str)
        self.assertIsInstance(task_summary.update_time, str)
        self.assertIsInstance(task_summary.end_time, str)
        self.assertIsInstance(task_summary.status, str)
        self.assertIsInstance(task_summary.task_def_name, str)
        self.assertIsInstance(task_summary.task_type, str)
        self.assertIsInstance(task_summary.input, str)
        self.assertIsInstance(task_summary.output, str)
        self.assertIsInstance(task_summary.task_id, str)
        self.assertIsInstance(task_summary.external_input_payload_storage_path, str)
        self.assertIsInstance(task_summary.external_output_payload_storage_path, str)

        # Integer properties
        self.assertIsInstance(task_summary.execution_time, int)
        self.assertIsInstance(task_summary.queue_wait_time, int)
        self.assertIsInstance(task_summary.workflow_priority, int)

        # Optional string property
        self.assertIsNone(task_summary.reason_for_incompletion)

    def test_all_property_setters_exist(self):
        """Test that all property setters exist and work correctly."""
        task_summary = TaskSummary()

        # Test string setters
        task_summary.workflow_id = 'new_wf_id'
        self.assertEqual(task_summary.workflow_id, 'new_wf_id')

        task_summary.workflow_type = 'new_workflow_type'
        self.assertEqual(task_summary.workflow_type, 'new_workflow_type')

        task_summary.correlation_id = 'new_corr_id'
        self.assertEqual(task_summary.correlation_id, 'new_corr_id')

        task_summary.scheduled_time = '2024-02-01T10:00:00Z'
        self.assertEqual(task_summary.scheduled_time, '2024-02-01T10:00:00Z')

        task_summary.start_time = '2024-02-01T10:05:00Z'
        self.assertEqual(task_summary.start_time, '2024-02-01T10:05:00Z')

        task_summary.update_time = '2024-02-01T10:10:00Z'
        self.assertEqual(task_summary.update_time, '2024-02-01T10:10:00Z')

        task_summary.end_time = '2024-02-01T10:15:00Z'
        self.assertEqual(task_summary.end_time, '2024-02-01T10:15:00Z')

        task_summary.reason_for_incompletion = 'Test reason'
        self.assertEqual(task_summary.reason_for_incompletion, 'Test reason')

        task_summary.task_def_name = 'new_task_def'
        self.assertEqual(task_summary.task_def_name, 'new_task_def')

        task_summary.task_type = 'new_task_type'
        self.assertEqual(task_summary.task_type, 'new_task_type')

        task_summary.input = '{"new": "input"}'
        self.assertEqual(task_summary.input, '{"new": "input"}')

        task_summary.output = '{"new": "output"}'
        self.assertEqual(task_summary.output, '{"new": "output"}')

        task_summary.task_id = 'new_task_id'
        self.assertEqual(task_summary.task_id, 'new_task_id')

        task_summary.external_input_payload_storage_path = '/new/input/path'
        self.assertEqual(task_summary.external_input_payload_storage_path, '/new/input/path')

        task_summary.external_output_payload_storage_path = '/new/output/path'
        self.assertEqual(task_summary.external_output_payload_storage_path, '/new/output/path')

        # Test integer setters
        task_summary.execution_time = 1000000
        self.assertEqual(task_summary.execution_time, 1000000)

        task_summary.queue_wait_time = 500000
        self.assertEqual(task_summary.queue_wait_time, 500000)

        task_summary.workflow_priority = 10
        self.assertEqual(task_summary.workflow_priority, 10)

    def test_status_enum_validation_all_allowed_values(self):
        """Test that status setter accepts all currently allowed enum values."""
        task_summary = TaskSummary()

        allowed_statuses = [
            "IN_PROGRESS",
            "CANCELED",
            "FAILED",
            "FAILED_WITH_TERMINAL_ERROR",
            "COMPLETED",
            "COMPLETED_WITH_ERRORS",
            "SCHEDULED",
            "TIMED_OUT",
            "SKIPPED"
        ]

        for status in allowed_statuses:
            task_summary.status = status
            self.assertEqual(task_summary.status, status)

    def test_status_enum_validation_rejects_invalid_values(self):
        """Test that status setter rejects invalid enum values."""
        task_summary = TaskSummary()

        invalid_statuses = [
            "INVALID_STATUS",
            "RUNNING",
            "PENDING",
            "ERROR",
            "",
            None
        ]

        for invalid_status in invalid_statuses:
            with self.assertRaises(ValueError):
                task_summary.status = invalid_status

    def test_status_validation_in_constructor(self):
        """Test that status validation works in constructor."""
        # Valid status in constructor
        task_summary = TaskSummary(status='COMPLETED')
        self.assertEqual(task_summary.status, 'COMPLETED')

        # Invalid status in constructor should raise ValueError
        with self.assertRaises(ValueError):
            TaskSummary(status='INVALID_STATUS')

    def test_swagger_types_contains_minimum_required_fields(self):
        """Test that swagger_types contains all minimum required fields and types."""
        # Define the minimum required fields that must exist for backward compatibility
        minimum_required_swagger_types = {
            'workflow_id': 'str',
            'workflow_type': 'str',
            'correlation_id': 'str',
            'scheduled_time': 'str',
            'start_time': 'str',
            'update_time': 'str',
            'end_time': 'str',
            'status': 'str',
            'reason_for_incompletion': 'str',
            'execution_time': 'int',
            'queue_wait_time': 'int',
            'task_def_name': 'str',
            'task_type': 'str',
            'input': 'str',
            'output': 'str',
            'task_id': 'str',
            'external_input_payload_storage_path': 'str',
            'external_output_payload_storage_path': 'str',
            'workflow_priority': 'int'
        }

        # Check that all required fields exist with correct types
        for field, expected_type in minimum_required_swagger_types.items():
            self.assertIn(field, TaskSummary.swagger_types,
                          f"Required field '{field}' missing from swagger_types")
            self.assertEqual(TaskSummary.swagger_types[field], expected_type,
                             f"Field '{field}' has type '{TaskSummary.swagger_types[field]}', expected '{expected_type}'")

    def test_attribute_map_contains_minimum_required_mappings(self):
        """Test that attribute_map contains all minimum required mappings."""
        # Define the minimum required mappings that must exist for backward compatibility
        minimum_required_attribute_map = {
            'workflow_id': 'workflowId',
            'workflow_type': 'workflowType',
            'correlation_id': 'correlationId',
            'scheduled_time': 'scheduledTime',
            'start_time': 'startTime',
            'update_time': 'updateTime',
            'end_time': 'endTime',
            'status': 'status',
            'reason_for_incompletion': 'reasonForIncompletion',
            'execution_time': 'executionTime',
            'queue_wait_time': 'queueWaitTime',
            'task_def_name': 'taskDefName',
            'task_type': 'taskType',
            'input': 'input',
            'output': 'output',
            'task_id': 'taskId',
            'external_input_payload_storage_path': 'externalInputPayloadStoragePath',
            'external_output_payload_storage_path': 'externalOutputPayloadStoragePath',
            'workflow_priority': 'workflowPriority'
        }

        # Check that all required mappings exist with correct values
        for field, expected_mapping in minimum_required_attribute_map.items():
            self.assertIn(field, TaskSummary.attribute_map,
                          f"Required field '{field}' missing from attribute_map")
            self.assertEqual(TaskSummary.attribute_map[field], expected_mapping,
                             f"Field '{field}' maps to '{TaskSummary.attribute_map[field]}', expected '{expected_mapping}'")

    def test_to_dict_method_exists_and_works(self):
        """Test that to_dict method exists and returns expected structure."""
        task_summary = TaskSummary(**self.valid_data)
        result_dict = task_summary.to_dict()

        self.assertIsInstance(result_dict, dict)

        # Check that all minimum required fields are present in the dictionary
        minimum_required_fields = {
            'workflow_id', 'workflow_type', 'correlation_id', 'scheduled_time',
            'start_time', 'update_time', 'end_time', 'status', 'reason_for_incompletion',
            'execution_time', 'queue_wait_time', 'task_def_name', 'task_type',
            'input', 'output', 'task_id', 'external_input_payload_storage_path',
            'external_output_payload_storage_path', 'workflow_priority'
        }

        for field in minimum_required_fields:
            self.assertIn(field, result_dict, f"Required field '{field}' missing from to_dict() output")

    def test_to_str_method_exists(self):
        """Test that to_str method exists."""
        task_summary = TaskSummary(**self.valid_data)
        str_result = task_summary.to_str()
        self.assertIsInstance(str_result, str)

    def test_repr_method_exists(self):
        """Test that __repr__ method exists."""
        task_summary = TaskSummary(**self.valid_data)
        repr_result = repr(task_summary)
        self.assertIsInstance(repr_result, str)

    def test_equality_methods_exist(self):
        """Test that __eq__ and __ne__ methods exist and work correctly."""
        task_summary1 = TaskSummary(**self.valid_data)
        task_summary2 = TaskSummary(**self.valid_data)
        task_summary3 = TaskSummary(workflow_id='different_id')

        # Test equality
        self.assertEqual(task_summary1, task_summary2)
        self.assertNotEqual(task_summary1, task_summary3)

        # Test inequality
        self.assertFalse(task_summary1 != task_summary2)
        self.assertTrue(task_summary1 != task_summary3)

    def test_discriminator_attribute_exists(self):
        """Test that discriminator attribute exists and is None."""
        task_summary = TaskSummary()
        self.assertIsNone(task_summary.discriminator)

    def test_backward_compatibility_field_count(self):
        """Test that the model has at least the expected number of fields."""
        # This test ensures no fields are removed
        expected_minimum_field_count = 19
        actual_field_count = len(TaskSummary.swagger_types)

        self.assertGreaterEqual(
            actual_field_count,
            expected_minimum_field_count,
            f"Model has {actual_field_count} fields, expected at least {expected_minimum_field_count}. "
            "Fields may have been removed, breaking backward compatibility."
        )

    def test_backward_compatibility_status_enum_values(self):
        """Test that all expected status enum values are still supported."""
        # This test ensures no enum values are removed
        expected_minimum_status_values = {
            "IN_PROGRESS",
            "CANCELED",
            "FAILED",
            "FAILED_WITH_TERMINAL_ERROR",
            "COMPLETED",
            "COMPLETED_WITH_ERRORS",
            "SCHEDULED",
            "TIMED_OUT",
            "SKIPPED"
        }

        task_summary = TaskSummary()

        # Test that all expected values are still accepted
        for status in expected_minimum_status_values:
            try:
                task_summary.status = status
                self.assertEqual(task_summary.status, status)
            except ValueError:
                self.fail(f"Status value '{status}' is no longer supported, breaking backward compatibility")

    def test_new_fields_are_optional_and_backward_compatible(self):
        """Test that any new fields added don't break existing functionality."""
        # Test that old code can still create instances without new fields
        task_summary = TaskSummary(**self.valid_data)

        # Verify the object was created successfully
        self.assertIsNotNone(task_summary)

        # Test that to_dict() works with the old data
        result_dict = task_summary.to_dict()
        self.assertIsInstance(result_dict, dict)

        # Test that all original fields are still accessible
        for field_name in self.valid_data.keys():
            self.assertTrue(hasattr(task_summary, field_name),
                            f"Original field '{field_name}' is no longer accessible")


if __name__ == '__main__':
    unittest.main()