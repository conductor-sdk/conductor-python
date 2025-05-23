import unittest
from conductor.client.http.models import WorkflowStatus


class TestWorkflowStatusBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for WorkflowStatus model.

    Principles:
    ✅ Allow additions (new fields, new enum values)
    ❌ Prevent removals (missing fields, removed enum values)
    ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test fixtures with valid data"""
        self.valid_workflow_id = "test_workflow_123"
        self.valid_correlation_id = "corr_123"
        self.valid_output = {"result": "success", "data": {"key": "value"}}
        self.valid_variables = {"var1": "value1", "var2": 42}
        self.valid_status_values = ["RUNNING", "COMPLETED", "FAILED", "TIMED_OUT", "TERMINATED", "PAUSED"]

    def test_constructor_exists_and_accepts_expected_parameters(self):
        """Test that constructor exists and accepts all expected parameters"""
        # Should work with no parameters (all optional)
        workflow_status = WorkflowStatus()
        self.assertIsInstance(workflow_status, WorkflowStatus)

        # Should work with all parameters
        workflow_status = WorkflowStatus(
            workflow_id=self.valid_workflow_id,
            correlation_id=self.valid_correlation_id,
            output=self.valid_output,
            variables=self.valid_variables,
            status="RUNNING"
        )
        self.assertIsInstance(workflow_status, WorkflowStatus)

    def test_all_expected_fields_exist(self):
        """Test that all expected fields exist and are accessible"""
        workflow_status = WorkflowStatus()

        # Test that all expected properties exist
        expected_properties = [
            'workflow_id', 'correlation_id', 'output', 'variables', 'status'
        ]

        for prop in expected_properties:
            self.assertTrue(hasattr(workflow_status, prop),
                            f"Property '{prop}' should exist")
            # Should be able to get the property
            getattr(workflow_status, prop)

    def test_field_getters_and_setters_work(self):
        """Test that field getters and setters work as expected"""
        workflow_status = WorkflowStatus()

        # Test workflow_id
        workflow_status.workflow_id = self.valid_workflow_id
        self.assertEqual(workflow_status.workflow_id, self.valid_workflow_id)

        # Test correlation_id
        workflow_status.correlation_id = self.valid_correlation_id
        self.assertEqual(workflow_status.correlation_id, self.valid_correlation_id)

        # Test output
        workflow_status.output = self.valid_output
        self.assertEqual(workflow_status.output, self.valid_output)

        # Test variables
        workflow_status.variables = self.valid_variables
        self.assertEqual(workflow_status.variables, self.valid_variables)

        # Test status with valid value
        workflow_status.status = "RUNNING"
        self.assertEqual(workflow_status.status, "RUNNING")

    def test_status_validation_rules_preserved(self):
        """Test that status field validation rules are preserved"""
        workflow_status = WorkflowStatus()

        # Test that all historically valid status values still work
        for status_value in self.valid_status_values:
            workflow_status.status = status_value
            self.assertEqual(workflow_status.status, status_value)

        # Test that invalid status still raises ValueError
        with self.assertRaises(ValueError) as context:
            workflow_status.status = "INVALID_STATUS"

        error_message = str(context.exception)
        self.assertIn("Invalid value for `status`", error_message)
        self.assertIn("INVALID_STATUS", error_message)

    def test_constructor_with_status_validation(self):
        """Test that constructor properly validates status when provided"""
        # Valid status should work
        for status_value in self.valid_status_values:
            workflow_status = WorkflowStatus(status=status_value)
            self.assertEqual(workflow_status.status, status_value)

        # Invalid status should raise ValueError
        with self.assertRaises(ValueError):
            WorkflowStatus(status="INVALID_STATUS")

    def test_none_values_allowed_for_applicable_fields(self):
        """Test that None values are allowed for fields that support them"""
        workflow_status = WorkflowStatus()

        # All fields should default to None
        self.assertIsNone(workflow_status.workflow_id)
        self.assertIsNone(workflow_status.correlation_id)
        self.assertIsNone(workflow_status.output)
        self.assertIsNone(workflow_status.variables)
        self.assertIsNone(workflow_status.status)

        # Should be able to explicitly set to None for fields that support it
        workflow_status.workflow_id = None
        workflow_status.correlation_id = None
        workflow_status.output = None
        workflow_status.variables = None

        # Status field does NOT allow None after construction due to validation
        with self.assertRaises(ValueError):
            workflow_status.status = None

    def test_expected_methods_exist(self):
        """Test that expected methods exist and work"""
        workflow_status = WorkflowStatus(
            workflow_id=self.valid_workflow_id,
            status="COMPLETED"
        )

        # Test methods exist
        expected_methods = ['to_dict', 'to_str', 'is_completed', 'is_successful', 'is_running']
        for method_name in expected_methods:
            self.assertTrue(hasattr(workflow_status, method_name),
                            f"Method '{method_name}' should exist")
            self.assertTrue(callable(getattr(workflow_status, method_name)),
                            f"Method '{method_name}' should be callable")

    def test_is_completed_method_behavior(self):
        """Test that is_completed method works with expected status values"""
        workflow_status = WorkflowStatus()

        # Test terminal statuses
        terminal_statuses = ['COMPLETED', 'FAILED', 'TIMED_OUT', 'TERMINATED']
        for status in terminal_statuses:
            workflow_status.status = status
            self.assertTrue(workflow_status.is_completed(),
                            f"Status '{status}' should be considered completed")

        # Test non-terminal statuses
        non_terminal_statuses = ['RUNNING', 'PAUSED']
        for status in non_terminal_statuses:
            workflow_status.status = status
            self.assertFalse(workflow_status.is_completed(),
                             f"Status '{status}' should not be considered completed")

    def test_is_successful_method_behavior(self):
        """Test that is_successful method works with expected status values"""
        workflow_status = WorkflowStatus()

        # Test successful statuses
        successful_statuses = ['PAUSED', 'COMPLETED']
        for status in successful_statuses:
            workflow_status.status = status
            self.assertTrue(workflow_status.is_successful(),
                            f"Status '{status}' should be considered successful")

        # Test non-successful statuses
        non_successful_statuses = ['RUNNING', 'FAILED', 'TIMED_OUT', 'TERMINATED']
        for status in non_successful_statuses:
            workflow_status.status = status
            self.assertFalse(workflow_status.is_successful(),
                             f"Status '{status}' should not be considered successful")

    def test_is_running_method_behavior(self):
        """Test that is_running method works with expected status values"""
        workflow_status = WorkflowStatus()

        # Test running statuses
        running_statuses = ['RUNNING', 'PAUSED']
        for status in running_statuses:
            workflow_status.status = status
            self.assertTrue(workflow_status.is_running(),
                            f"Status '{status}' should be considered running")

        # Test non-running statuses
        non_running_statuses = ['COMPLETED', 'FAILED', 'TIMED_OUT', 'TERMINATED']
        for status in non_running_statuses:
            workflow_status.status = status
            self.assertFalse(workflow_status.is_running(),
                             f"Status '{status}' should not be considered running")

    def test_to_dict_method_returns_expected_structure(self):
        """Test that to_dict method returns expected structure"""
        workflow_status = WorkflowStatus(
            workflow_id=self.valid_workflow_id,
            correlation_id=self.valid_correlation_id,
            output=self.valid_output,
            variables=self.valid_variables,
            status="RUNNING"
        )

        result_dict = workflow_status.to_dict()

        # Should return a dictionary
        self.assertIsInstance(result_dict, dict)

        # Should contain expected keys
        expected_keys = ['workflow_id', 'correlation_id', 'output', 'variables', 'status']
        for key in expected_keys:
            self.assertIn(key, result_dict, f"Key '{key}' should be in to_dict() result")

    def test_string_representations_work(self):
        """Test that string representation methods work"""
        workflow_status = WorkflowStatus(workflow_id=self.valid_workflow_id)

        # to_str should return a string
        str_repr = workflow_status.to_str()
        self.assertIsInstance(str_repr, str)

        # __repr__ should return a string
        repr_result = repr(workflow_status)
        self.assertIsInstance(repr_result, str)

    def test_equality_methods_work(self):
        """Test that equality methods work as expected"""
        workflow_status1 = WorkflowStatus(
            workflow_id=self.valid_workflow_id,
            status="RUNNING"
        )
        workflow_status2 = WorkflowStatus(
            workflow_id=self.valid_workflow_id,
            status="RUNNING"
        )
        workflow_status3 = WorkflowStatus(
            workflow_id="different_id",
            status="RUNNING"
        )

        # Equal objects should be equal
        self.assertEqual(workflow_status1, workflow_status2)
        self.assertFalse(workflow_status1 != workflow_status2)

        # Different objects should not be equal
        self.assertNotEqual(workflow_status1, workflow_status3)
        self.assertTrue(workflow_status1 != workflow_status3)

    def test_attribute_map_preserved(self):
        """Test that attribute_map is preserved for API compatibility"""
        expected_attribute_map = {
            'workflow_id': 'workflowId',
            'correlation_id': 'correlationId',
            'output': 'output',
            'variables': 'variables',
            'status': 'status'
        }

        self.assertTrue(hasattr(WorkflowStatus, 'attribute_map'))
        self.assertEqual(WorkflowStatus.attribute_map, expected_attribute_map)

    def test_swagger_types_preserved(self):
        """Test that swagger_types is preserved for API compatibility"""
        expected_swagger_types = {
            'workflow_id': 'str',
            'correlation_id': 'str',
            'output': 'dict(str, object)',
            'variables': 'dict(str, object)',
            'status': 'str'
        }

        self.assertTrue(hasattr(WorkflowStatus, 'swagger_types'))
        self.assertEqual(WorkflowStatus.swagger_types, expected_swagger_types)


if __name__ == '__main__':
    unittest.main()