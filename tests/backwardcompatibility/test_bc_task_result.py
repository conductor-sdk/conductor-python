import unittest
from unittest.mock import patch
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus


class TestTaskResultBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for TaskResult model.

    Ensures:
    - All existing fields remain accessible
    - Field types haven't changed
    - Existing validation rules still apply
    - Constructor behavior remains consistent
    """

    def setUp(self):
        """Set up test fixtures with valid data."""
        self.valid_workflow_id = "workflow_123"
        self.valid_task_id = "task_456"

        # Get valid status values from enum
        self.valid_status_values = [status.name for status in TaskResultStatus]
        self.valid_status = self.valid_status_values[0] if self.valid_status_values else None

    def test_required_fields_exist_and_accessible(self):
        """Test that required fields (workflow_instance_id, task_id) exist and are accessible."""
        task_result = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        # Test field accessibility
        self.assertEqual(task_result.workflow_instance_id, self.valid_workflow_id)
        self.assertEqual(task_result.task_id, self.valid_task_id)

        # Test private attributes exist
        self.assertTrue(hasattr(task_result, '_workflow_instance_id'))
        self.assertTrue(hasattr(task_result, '_task_id'))

    def test_all_existing_fields_exist(self):
        """Test that all known fields from the original model still exist."""
        expected_fields = [
            'workflow_instance_id',
            'task_id',
            'reason_for_incompletion',
            'callback_after_seconds',
            'worker_id',
            'status',
            'output_data',
            'logs',
            'external_output_payload_storage_path',
            'sub_workflow_id'
        ]

        task_result = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        for field in expected_fields:
            with self.subTest(field=field):
                self.assertTrue(hasattr(task_result, field),
                                f"Field '{field}' is missing from TaskResult")

    def test_field_types_unchanged(self):
        """Test that existing field types haven't changed."""
        expected_types = {
            'workflow_instance_id': str,
            'task_id': str,
            'reason_for_incompletion': str,
            'callback_after_seconds': int,
            'worker_id': str,
            'status': str,  # Note: stored as enum but accessed as string
            'output_data': dict,
            'logs': list,
            'external_output_payload_storage_path': str,
            'sub_workflow_id': str
        }

        task_result = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id,
            reason_for_incompletion="test reason",
            callback_after_seconds=30,
            worker_id="worker_123",
            status=self.valid_status,
            output_data={"key": "value"},
            logs=[],
            external_output_payload_storage_path="/path/to/storage",
            sub_workflow_id="sub_workflow_789"
        )

        for field, expected_type in expected_types.items():
            with self.subTest(field=field):
                value = getattr(task_result, field)
                if value is not None:  # Skip None values for optional fields
                    if field == 'status':
                        # Status is stored as enum but we verify string access works
                        self.assertIsInstance(value.name if hasattr(value, 'name') else value, str)
                    else:
                        self.assertIsInstance(value, expected_type,
                                              f"Field '{field}' type changed from {expected_type}")

    def test_swagger_types_structure_unchanged(self):
        """Test that swagger_types dictionary structure is preserved."""
        expected_swagger_types = {
            'workflow_instance_id': 'str',
            'task_id': 'str',
            'reason_for_incompletion': 'str',
            'callback_after_seconds': 'int',
            'worker_id': 'str',
            'status': 'str',
            'output_data': 'dict(str, object)',
            'logs': 'list[TaskExecLog]',
            'external_output_payload_storage_path': 'str',
            'sub_workflow_id': 'str'
        }

        for field, type_str in expected_swagger_types.items():
            with self.subTest(field=field):
                self.assertIn(field, TaskResult.swagger_types,
                              f"Field '{field}' missing from swagger_types")
                self.assertEqual(TaskResult.swagger_types[field], type_str,
                                 f"swagger_types for '{field}' changed")

    def test_attribute_map_structure_unchanged(self):
        """Test that attribute_map dictionary structure is preserved."""
        expected_attribute_map = {
            'workflow_instance_id': 'workflowInstanceId',
            'task_id': 'taskId',
            'reason_for_incompletion': 'reasonForIncompletion',
            'callback_after_seconds': 'callbackAfterSeconds',
            'worker_id': 'workerId',
            'status': 'status',
            'output_data': 'outputData',
            'logs': 'logs',
            'external_output_payload_storage_path': 'externalOutputPayloadStoragePath',
            'sub_workflow_id': 'subWorkflowId'
        }

        for field, json_key in expected_attribute_map.items():
            with self.subTest(field=field):
                self.assertIn(field, TaskResult.attribute_map,
                              f"Field '{field}' missing from attribute_map")
                self.assertEqual(TaskResult.attribute_map[field], json_key,
                                 f"attribute_map for '{field}' changed")

    def test_constructor_with_required_fields_only(self):
        """Test constructor works with only required fields."""
        task_result = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        self.assertEqual(task_result.workflow_instance_id, self.valid_workflow_id)
        self.assertEqual(task_result.task_id, self.valid_task_id)

        # Optional fields should be None
        self.assertIsNone(task_result.reason_for_incompletion)
        self.assertIsNone(task_result.callback_after_seconds)
        self.assertIsNone(task_result.worker_id)
        self.assertIsNone(task_result.status)
        self.assertIsNone(task_result.output_data)
        self.assertIsNone(task_result.logs)
        self.assertIsNone(task_result.external_output_payload_storage_path)
        self.assertIsNone(task_result.sub_workflow_id)

    def test_constructor_with_all_fields(self):
        """Test constructor works with all fields provided."""
        test_data = {
            'workflow_instance_id': self.valid_workflow_id,
            'task_id': self.valid_task_id,
            'reason_for_incompletion': "test reason",
            'callback_after_seconds': 30,
            'worker_id': "worker_123",
            'status': self.valid_status,
            'output_data': {"key": "value"},
            'logs': [],
            'external_output_payload_storage_path': "/path/to/storage",
            'sub_workflow_id': "sub_workflow_789"
        }

        task_result = TaskResult(**test_data)

        for field, expected_value in test_data.items():
            with self.subTest(field=field):
                actual_value = getattr(task_result, field)
                if field == 'status':
                    # Status validation converts string to enum
                    self.assertEqual(actual_value.name, expected_value)
                else:
                    self.assertEqual(actual_value, expected_value)

    def test_status_validation_unchanged(self):
        """Test that status validation behavior is preserved."""
        task_result = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        # Test valid status assignment
        if self.valid_status:
            task_result.status = self.valid_status
            self.assertEqual(task_result.status.name, self.valid_status)

        # Test invalid status assignment raises ValueError
        with self.assertRaises(ValueError) as context:
            task_result.status = "INVALID_STATUS"

        self.assertIn("Invalid value for `status`", str(context.exception))

    def test_property_setters_work(self):
        """Test that all property setters still function correctly."""
        task_result = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        # Test setting optional fields via properties
        task_result.reason_for_incompletion = "updated reason"
        task_result.callback_after_seconds = 60
        task_result.worker_id = "new_worker"
        task_result.output_data = {"new_key": "new_value"}
        task_result.logs = ["log1", "log2"]
        task_result.external_output_payload_storage_path = "/new/path"
        task_result.sub_workflow_id = "new_sub_workflow"

        # Verify assignments worked
        self.assertEqual(task_result.reason_for_incompletion, "updated reason")
        self.assertEqual(task_result.callback_after_seconds, 60)
        self.assertEqual(task_result.worker_id, "new_worker")
        self.assertEqual(task_result.output_data, {"new_key": "new_value"})
        self.assertEqual(task_result.logs, ["log1", "log2"])
        self.assertEqual(task_result.external_output_payload_storage_path, "/new/path")
        self.assertEqual(task_result.sub_workflow_id, "new_sub_workflow")

    def test_utility_methods_exist(self):
        """Test that utility methods still exist and work."""
        task_result = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        # Test to_dict method exists and returns dict
        result_dict = task_result.to_dict()
        self.assertIsInstance(result_dict, dict)
        self.assertIn('workflow_instance_id', result_dict)
        self.assertIn('task_id', result_dict)

        # Test to_str method exists and returns string
        result_str = task_result.to_str()
        self.assertIsInstance(result_str, str)

        # Test __repr__ method
        repr_str = repr(task_result)
        self.assertIsInstance(repr_str, str)

    def test_add_output_data_method_exists(self):
        """Test that the add_output_data convenience method still works."""
        task_result = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        # Test adding to None output_data
        task_result.add_output_data("key1", "value1")
        self.assertEqual(task_result.output_data, {"key1": "value1"})

        # Test adding to existing output_data
        task_result.add_output_data("key2", "value2")
        self.assertEqual(task_result.output_data, {"key1": "value1", "key2": "value2"})

    def test_equality_methods_work(self):
        """Test that equality comparison methods still work."""
        task_result1 = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        task_result2 = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        task_result3 = TaskResult(
            workflow_instance_id="different_id",
            task_id=self.valid_task_id
        )

        # Test equality
        self.assertEqual(task_result1, task_result2)
        self.assertNotEqual(task_result1, task_result3)

        # Test inequality
        self.assertFalse(task_result1 != task_result2)
        self.assertTrue(task_result1 != task_result3)

    def test_discriminator_attribute_exists(self):
        """Test that discriminator attribute is still present."""
        task_result = TaskResult(
            workflow_instance_id=self.valid_workflow_id,
            task_id=self.valid_task_id
        )

        self.assertTrue(hasattr(task_result, 'discriminator'))
        self.assertIsNone(task_result.discriminator)


if __name__ == '__main__':
    unittest.main()