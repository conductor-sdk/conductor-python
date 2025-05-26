import unittest
from unittest.mock import Mock
from conductor.client.http.models import WorkflowRun, Task


class TestWorkflowRunBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for WorkflowRun model.

    These tests ensure that:
    - All existing fields remain accessible
    - Field types haven't changed
    - Existing validation rules still apply
    - Constructor behavior remains consistent
    - Method signatures haven't changed
    """

    def setUp(self):
        """Set up test fixtures with valid data."""
        # Mock Task objects for testing
        self.mock_task1 = Mock(spec=Task)
        self.mock_task1.task_def_name = "test_task_1"
        self.mock_task1.status = "COMPLETED"
        self.mock_task1.workflow_task = Mock()
        self.mock_task1.workflow_task.task_reference_name = "task_ref_1"

        self.mock_task2 = Mock(spec=Task)
        self.mock_task2.task_def_name = "test_task_2"
        self.mock_task2.status = "IN_PROGRESS"
        self.mock_task2.workflow_task = Mock()
        self.mock_task2.workflow_task.task_reference_name = "task_ref_2"

        # Valid test data
        self.valid_data = {
            'correlation_id': 'test_correlation_123',
            'create_time': 1640995200000,
            'created_by': 'test_user',
            'input': {'param1': 'value1', 'param2': 123},
            'output': {'result': 'success'},
            'priority': 5,
            'request_id': 'req_123',
            'status': 'COMPLETED',
            'tasks': [self.mock_task1, self.mock_task2],
            'update_time': 1640995260000,
            'variables': {'var1': 'value1'},
            'workflow_id': 'workflow_123'
        }

    def test_constructor_accepts_all_existing_parameters(self):
        """Test that constructor accepts all documented parameters."""
        # Test with all parameters
        workflow_run = WorkflowRun(**self.valid_data)

        # Verify all parameters were set
        self.assertEqual(workflow_run.correlation_id, 'test_correlation_123')
        self.assertEqual(workflow_run.create_time, 1640995200000)
        self.assertEqual(workflow_run.created_by, 'test_user')
        self.assertEqual(workflow_run.input, {'param1': 'value1', 'param2': 123})
        self.assertEqual(workflow_run.output, {'result': 'success'})
        self.assertEqual(workflow_run.priority, 5)
        self.assertEqual(workflow_run.request_id, 'req_123')
        self.assertEqual(workflow_run.status, 'COMPLETED')
        self.assertEqual(workflow_run.tasks, [self.mock_task1, self.mock_task2])
        self.assertEqual(workflow_run.update_time, 1640995260000)
        self.assertEqual(workflow_run.variables, {'var1': 'value1'})
        self.assertEqual(workflow_run.workflow_id, 'workflow_123')

    def test_constructor_accepts_none_values(self):
        """Test that constructor handles None values for optional parameters."""
        workflow_run = WorkflowRun()

        # All fields should be None initially
        self.assertIsNone(workflow_run.correlation_id)
        self.assertIsNone(workflow_run.create_time)
        self.assertIsNone(workflow_run.created_by)
        self.assertIsNone(workflow_run.input)
        self.assertIsNone(workflow_run.output)
        self.assertIsNone(workflow_run.priority)
        self.assertIsNone(workflow_run.request_id)
        self.assertIsNone(workflow_run.status)
        self.assertIsNone(workflow_run.tasks)
        self.assertIsNone(workflow_run.update_time)
        self.assertIsNone(workflow_run.variables)
        self.assertIsNone(workflow_run.workflow_id)

    def test_all_existing_properties_accessible(self):
        """Test that all existing properties remain accessible."""
        workflow_run = WorkflowRun(**self.valid_data)

        # Test getter access
        properties_to_test = [
            'correlation_id', 'create_time', 'created_by', 'input',
            'output', 'priority', 'request_id', 'status', 'tasks',
            'update_time', 'variables', 'workflow_id', 'reason_for_incompletion'
        ]

        for prop in properties_to_test:
            # Should not raise AttributeError
            value = getattr(workflow_run, prop)
            self.assertTrue(hasattr(workflow_run, prop))

    def test_all_existing_setters_functional(self):
        """Test that all existing property setters remain functional."""
        workflow_run = WorkflowRun()

        # Test setter access
        workflow_run.correlation_id = 'new_correlation'
        workflow_run.create_time = 9999999
        workflow_run.created_by = 'new_user'
        workflow_run.input = {'new': 'input'}
        workflow_run.output = {'new': 'output'}
        workflow_run.priority = 10
        workflow_run.request_id = 'new_request'
        workflow_run.tasks = [self.mock_task1]
        workflow_run.update_time = 8888888
        workflow_run.variables = {'new': 'variables'}
        workflow_run.workflow_id = 'new_workflow'

        # Verify setters worked
        self.assertEqual(workflow_run.correlation_id, 'new_correlation')
        self.assertEqual(workflow_run.create_time, 9999999)
        self.assertEqual(workflow_run.created_by, 'new_user')
        self.assertEqual(workflow_run.input, {'new': 'input'})
        self.assertEqual(workflow_run.output, {'new': 'output'})
        self.assertEqual(workflow_run.priority, 10)
        self.assertEqual(workflow_run.request_id, 'new_request')
        self.assertEqual(workflow_run.tasks, [self.mock_task1])
        self.assertEqual(workflow_run.update_time, 8888888)
        self.assertEqual(workflow_run.variables, {'new': 'variables'})
        self.assertEqual(workflow_run.workflow_id, 'new_workflow')

    def test_status_validation_rules_unchanged(self):
        """Test that status validation rules remain the same."""
        workflow_run = WorkflowRun()

        # Valid status values should work
        valid_statuses = ["RUNNING", "COMPLETED", "FAILED", "TIMED_OUT", "TERMINATED", "PAUSED"]
        for status in valid_statuses:
            workflow_run.status = status
            self.assertEqual(workflow_run.status, status)

        # Invalid status should raise ValueError
        with self.assertRaises(ValueError) as context:
            workflow_run.status = "INVALID_STATUS"

        self.assertIn("Invalid value for `status`", str(context.exception))
        self.assertIn("INVALID_STATUS", str(context.exception))

    def test_field_types_unchanged(self):
        """Test that field types haven't changed."""
        workflow_run = WorkflowRun(**self.valid_data)

        # String fields
        self.assertIsInstance(workflow_run.correlation_id, str)
        self.assertIsInstance(workflow_run.created_by, str)
        self.assertIsInstance(workflow_run.request_id, str)
        self.assertIsInstance(workflow_run.status, str)
        self.assertIsInstance(workflow_run.workflow_id, str)

        # Integer fields
        self.assertIsInstance(workflow_run.create_time, int)
        self.assertIsInstance(workflow_run.priority, int)
        self.assertIsInstance(workflow_run.update_time, int)

        # Dictionary fields
        self.assertIsInstance(workflow_run.input, dict)
        self.assertIsInstance(workflow_run.output, dict)
        self.assertIsInstance(workflow_run.variables, dict)

        # List field
        self.assertIsInstance(workflow_run.tasks, list)

    def test_status_check_methods_unchanged(self):
        """Test that status checking methods remain functional and consistent."""
        workflow_run = WorkflowRun()

        # Test is_completed method for terminal statuses
        terminal_statuses = ['COMPLETED', 'FAILED', 'TIMED_OUT', 'TERMINATED']
        for status in terminal_statuses:
            workflow_run.status = status
            self.assertTrue(workflow_run.is_completed(),
                            f"is_completed() should return True for status: {status}")

        # Test is_completed method for non-terminal statuses
        non_terminal_statuses = ['RUNNING', 'PAUSED']
        for status in non_terminal_statuses:
            workflow_run.status = status
            self.assertFalse(workflow_run.is_completed(),
                             f"is_completed() should return False for status: {status}")

        # Test is_successful method
        successful_statuses = ['PAUSED', 'COMPLETED']
        for status in successful_statuses:
            workflow_run.status = status
            self.assertTrue(workflow_run.is_successful(),
                            f"is_successful() should return True for status: {status}")

        # Test is_running method
        running_statuses = ['RUNNING', 'PAUSED']
        for status in running_statuses:
            workflow_run.status = status
            self.assertTrue(workflow_run.is_running(),
                            f"is_running() should return True for status: {status}")

    def test_get_task_method_signature_unchanged(self):
        """Test that get_task method signature and behavior remain unchanged."""
        workflow_run = WorkflowRun(tasks=[self.mock_task1, self.mock_task2])

        # Test get_task by name
        task = workflow_run.get_task(name="test_task_1")
        self.assertEqual(task, self.mock_task1)

        # Test get_task by task_reference_name
        task = workflow_run.get_task(task_reference_name="task_ref_2")
        self.assertEqual(task, self.mock_task2)

        # Test error when both parameters provided
        with self.assertRaises(Exception) as context:
            workflow_run.get_task(name="test", task_reference_name="test")
        self.assertIn("ONLY one of name or task_reference_name MUST be provided", str(context.exception))

        # Test error when no parameters provided
        with self.assertRaises(Exception) as context:
            workflow_run.get_task()
        self.assertIn("ONLY one of name or task_reference_name MUST be provided", str(context.exception))

    def test_current_task_property_unchanged(self):
        """Test that current_task property behavior remains unchanged."""
        # Create workflow with tasks in different states
        scheduled_task = Mock(spec=Task)
        scheduled_task.status = "SCHEDULED"

        in_progress_task = Mock(spec=Task)
        in_progress_task.status = "IN_PROGRESS"

        completed_task = Mock(spec=Task)
        completed_task.status = "COMPLETED"

        workflow_run = WorkflowRun(tasks=[completed_task, scheduled_task, in_progress_task])

        # Should return the in_progress_task (last one that matches criteria)
        current = workflow_run.current_task
        self.assertEqual(current, in_progress_task)

        # Test with no current tasks
        workflow_run_no_current = WorkflowRun(tasks=[completed_task])
        self.assertIsNone(workflow_run_no_current.current_task)

    def test_utility_methods_unchanged(self):
        """Test that utility methods (to_dict, to_str, __repr__, __eq__, __ne__) remain functional."""
        workflow_run1 = WorkflowRun(**self.valid_data)
        workflow_run2 = WorkflowRun(**self.valid_data)

        # Test to_dict
        result_dict = workflow_run1.to_dict()
        self.assertIsInstance(result_dict, dict)

        # Test to_str
        str_repr = workflow_run1.to_str()
        self.assertIsInstance(str_repr, str)

        # Test __repr__
        repr_str = repr(workflow_run1)
        self.assertIsInstance(repr_str, str)

        # Test __eq__
        self.assertTrue(workflow_run1 == workflow_run2)

        # Test __ne__
        workflow_run2.correlation_id = "different"
        self.assertTrue(workflow_run1 != workflow_run2)

    def test_swagger_metadata_unchanged(self):
        """Test that swagger metadata attributes remain unchanged."""
        # Test that swagger_types exists and contains expected keys
        expected_swagger_keys = {
            'correlation_id', 'create_time', 'created_by', 'input', 'output',
            'priority', 'request_id', 'status', 'tasks', 'update_time',
            'variables', 'workflow_id'
        }

        self.assertEqual(set(WorkflowRun.swagger_types.keys()), expected_swagger_keys)

        # Test that attribute_map exists and contains expected keys
        expected_attribute_keys = {
            'correlation_id', 'create_time', 'created_by', 'input', 'output',
            'priority', 'request_id', 'status', 'tasks', 'update_time',
            'variables', 'workflow_id'
        }

        self.assertEqual(set(WorkflowRun.attribute_map.keys()), expected_attribute_keys)

        # Test specific type mappings
        self.assertEqual(WorkflowRun.swagger_types['correlation_id'], 'str')
        self.assertEqual(WorkflowRun.swagger_types['create_time'], 'int')
        self.assertEqual(WorkflowRun.swagger_types['input'], 'dict(str, object)')
        self.assertEqual(WorkflowRun.swagger_types['tasks'], 'list[Task]')

    def test_reason_for_incompletion_parameter_handling(self):
        """Test that reason_for_incompletion parameter is handled correctly."""
        # Test with reason_for_incompletion parameter
        workflow_run = WorkflowRun(
            status='FAILED',
            reason_for_incompletion='Task timeout'
        )

        self.assertEqual(workflow_run.reason_for_incompletion, 'Task timeout')
        self.assertEqual(workflow_run.status, 'FAILED')


if __name__ == '__main__':
    unittest.main()