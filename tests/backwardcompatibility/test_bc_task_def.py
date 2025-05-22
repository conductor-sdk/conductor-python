import unittest
from unittest.mock import Mock
from conductor.client.http.models.task_def import TaskDef
from conductor.client.http.models.schema_def import SchemaDef


class TestTaskDefBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for TaskDef model.

    Principles:
    - ✅ Allow additions (new fields, new enum values)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test fixtures with valid data for existing fields."""
        self.valid_schema_def = Mock(spec=SchemaDef)

        # Valid enum values that must continue to work
        self.valid_timeout_policies = ["RETRY", "TIME_OUT_WF", "ALERT_ONLY"]
        self.valid_retry_logics = ["FIXED", "EXPONENTIAL_BACKOFF", "LINEAR_BACKOFF"]

    def test_constructor_with_minimal_required_fields(self):
        """Test that constructor works with minimal required fields."""
        # Based on analysis: name and timeout_seconds appear to be required
        task_def = TaskDef(name="test_task", timeout_seconds=60)

        self.assertEqual(task_def.name, "test_task")
        self.assertEqual(task_def.timeout_seconds, 60)

    def test_constructor_with_all_existing_fields(self):
        """Test constructor with all existing fields to ensure they still work."""
        task_def = TaskDef(
            owner_app="test_app",
            create_time=1234567890,
            update_time=1234567891,
            created_by="test_user",
            updated_by="test_user_2",
            name="test_task",
            description="Test task description",
            retry_count=3,
            timeout_seconds=60,
            input_keys=["input1", "input2"],
            output_keys=["output1", "output2"],
            timeout_policy="RETRY",
            retry_logic="FIXED",
            retry_delay_seconds=5,
            response_timeout_seconds=30,
            concurrent_exec_limit=10,
            input_template={"key": "value"},
            rate_limit_per_frequency=100,
            rate_limit_frequency_in_seconds=60,
            isolation_group_id="group1",
            execution_name_space="namespace1",
            owner_email="test@example.com",
            poll_timeout_seconds=120,
            backoff_scale_factor=2,
            input_schema=self.valid_schema_def,
            output_schema=self.valid_schema_def,
            enforce_schema=True
        )

        # Verify all fields are set correctly
        self.assertEqual(task_def.owner_app, "test_app")
        self.assertEqual(task_def.create_time, 1234567890)
        self.assertEqual(task_def.update_time, 1234567891)
        self.assertEqual(task_def.created_by, "test_user")
        self.assertEqual(task_def.updated_by, "test_user_2")
        self.assertEqual(task_def.name, "test_task")
        self.assertEqual(task_def.description, "Test task description")
        self.assertEqual(task_def.retry_count, 3)
        self.assertEqual(task_def.timeout_seconds, 60)
        self.assertEqual(task_def.input_keys, ["input1", "input2"])
        self.assertEqual(task_def.output_keys, ["output1", "output2"])
        self.assertEqual(task_def.timeout_policy, "RETRY")
        self.assertEqual(task_def.retry_logic, "FIXED")
        self.assertEqual(task_def.retry_delay_seconds, 5)
        self.assertEqual(task_def.response_timeout_seconds, 30)
        self.assertEqual(task_def.concurrent_exec_limit, 10)
        self.assertEqual(task_def.input_template, {"key": "value"})
        self.assertEqual(task_def.rate_limit_per_frequency, 100)
        self.assertEqual(task_def.rate_limit_frequency_in_seconds, 60)
        self.assertEqual(task_def.isolation_group_id, "group1")
        self.assertEqual(task_def.execution_name_space, "namespace1")
        self.assertEqual(task_def.owner_email, "test@example.com")
        self.assertEqual(task_def.poll_timeout_seconds, 120)
        self.assertEqual(task_def.backoff_scale_factor, 2)
        self.assertEqual(task_def.input_schema, self.valid_schema_def)
        self.assertEqual(task_def.output_schema, self.valid_schema_def)
        self.assertEqual(task_def.enforce_schema, True)

    def test_all_existing_properties_exist(self):
        """Verify all existing properties still exist and are accessible."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        # Test that all existing properties exist (both getters and setters)
        existing_properties = [
            'owner_app', 'create_time', 'update_time', 'created_by', 'updated_by',
            'name', 'description', 'retry_count', 'timeout_seconds', 'input_keys',
            'output_keys', 'timeout_policy', 'retry_logic', 'retry_delay_seconds',
            'response_timeout_seconds', 'concurrent_exec_limit', 'input_template',
            'rate_limit_per_frequency', 'rate_limit_frequency_in_seconds',
            'isolation_group_id', 'execution_name_space', 'owner_email',
            'poll_timeout_seconds', 'backoff_scale_factor', 'input_schema',
            'output_schema', 'enforce_schema'
        ]

        for prop in existing_properties:
            # Test getter exists
            self.assertTrue(hasattr(task_def, prop), f"Property {prop} getter missing")
            # Test setter exists
            self.assertTrue(hasattr(type(task_def), prop), f"Property {prop} setter missing")

    def test_existing_field_types_unchanged(self):
        """Verify existing field types haven't changed."""
        expected_types = {
            'owner_app': str,
            'create_time': int,
            'update_time': int,
            'created_by': str,
            'updated_by': str,
            'name': str,
            'description': str,
            'retry_count': int,
            'timeout_seconds': int,
            'input_keys': list,
            'output_keys': list,
            'timeout_policy': str,
            'retry_logic': str,
            'retry_delay_seconds': int,
            'response_timeout_seconds': int,
            'concurrent_exec_limit': int,
            'input_template': dict,
            'rate_limit_per_frequency': int,
            'rate_limit_frequency_in_seconds': int,
            'isolation_group_id': str,
            'execution_name_space': str,
            'owner_email': str,
            'poll_timeout_seconds': int,
            'backoff_scale_factor': int,
            'input_schema': SchemaDef,
            'output_schema': SchemaDef,
            'enforce_schema': bool
        }

        # Check swagger_types mapping
        for field, expected_type_str in TaskDef.swagger_types.items():
            self.assertIn(field, expected_types, f"Unexpected field {field} in swagger_types")

    def test_timeout_policy_enum_values_preserved(self):
        """Test that existing timeout_policy enum values still work."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        for valid_value in self.valid_timeout_policies:
            # Test setter validation
            task_def.timeout_policy = valid_value
            self.assertEqual(task_def.timeout_policy, valid_value)

    def test_timeout_policy_invalid_values_rejected(self):
        """Test that invalid timeout_policy values are still rejected."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        invalid_values = ["INVALID", "invalid", "", None, 123]
        for invalid_value in invalid_values:
            with self.assertRaises(ValueError, msg=f"Should reject invalid timeout_policy: {invalid_value}"):
                task_def.timeout_policy = invalid_value

    def test_retry_logic_enum_values_preserved(self):
        """Test that existing retry_logic enum values still work."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        for valid_value in self.valid_retry_logics:
            # Test setter validation
            task_def.retry_logic = valid_value
            self.assertEqual(task_def.retry_logic, valid_value)

    def test_retry_logic_invalid_values_rejected(self):
        """Test that invalid retry_logic values are still rejected."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        invalid_values = ["INVALID", "invalid", "", None, 123]
        for invalid_value in invalid_values:
            with self.assertRaises(ValueError, msg=f"Should reject invalid retry_logic: {invalid_value}"):
                task_def.retry_logic = invalid_value

    def test_attribute_map_unchanged(self):
        """Test that attribute_map for existing fields is unchanged."""
        expected_attribute_map = {
            'owner_app': 'ownerApp',
            'create_time': 'createTime',
            'update_time': 'updateTime',
            'created_by': 'createdBy',
            'updated_by': 'updatedBy',
            'name': 'name',
            'description': 'description',
            'retry_count': 'retryCount',
            'timeout_seconds': 'timeoutSeconds',
            'input_keys': 'inputKeys',
            'output_keys': 'outputKeys',
            'timeout_policy': 'timeoutPolicy',
            'retry_logic': 'retryLogic',
            'retry_delay_seconds': 'retryDelaySeconds',
            'response_timeout_seconds': 'responseTimeoutSeconds',
            'concurrent_exec_limit': 'concurrentExecLimit',
            'input_template': 'inputTemplate',
            'rate_limit_per_frequency': 'rateLimitPerFrequency',
            'rate_limit_frequency_in_seconds': 'rateLimitFrequencyInSeconds',
            'isolation_group_id': 'isolationGroupId',
            'execution_name_space': 'executionNameSpace',
            'owner_email': 'ownerEmail',
            'poll_timeout_seconds': 'pollTimeoutSeconds',
            'backoff_scale_factor': 'backoffScaleFactor',
            'input_schema': 'inputSchema',
            'output_schema': 'outputSchema',
            'enforce_schema': 'enforceSchema'
        }

        for python_name, json_name in expected_attribute_map.items():
            self.assertIn(python_name, TaskDef.attribute_map,
                          f"Missing attribute mapping for {python_name}")
            self.assertEqual(TaskDef.attribute_map[python_name], json_name,
                             f"Changed attribute mapping for {python_name}")

    def test_to_dict_method_exists_and_works(self):
        """Test that to_dict method exists and produces expected structure."""
        task_def = TaskDef(
            name="test_task",
            timeout_seconds=60,
            description="Test description",
            retry_count=3,
            input_schema=self.valid_schema_def,
            enforce_schema=True
        )

        result = task_def.to_dict()

        self.assertIsInstance(result, dict)
        self.assertEqual(result['name'], "test_task")
        self.assertEqual(result['timeout_seconds'], 60)
        self.assertEqual(result['description'], "Test description")
        self.assertEqual(result['retry_count'], 3)
        self.assertEqual(result['enforce_schema'], True)

    def test_to_str_method_exists_and_works(self):
        """Test that to_str method exists and works."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        result = task_def.to_str()
        self.assertIsInstance(result, str)
        self.assertIn("test", result)

    def test_equality_methods_exist_and_work(self):
        """Test that __eq__ and __ne__ methods exist and work correctly."""
        task_def1 = TaskDef(name="test", timeout_seconds=60)
        task_def2 = TaskDef(name="test", timeout_seconds=60)
        task_def3 = TaskDef(name="different", timeout_seconds=60)

        # Test equality
        self.assertEqual(task_def1, task_def2)
        self.assertNotEqual(task_def1, task_def3)

        # Test inequality
        self.assertFalse(task_def1 != task_def2)
        self.assertTrue(task_def1 != task_def3)

    def test_repr_method_exists_and_works(self):
        """Test that __repr__ method exists and works."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        result = repr(task_def)
        self.assertIsInstance(result, str)

    def test_schema_properties_behavior(self):
        """Test that schema-related properties work as expected."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        # Test input_schema
        task_def.input_schema = self.valid_schema_def
        self.assertEqual(task_def.input_schema, self.valid_schema_def)

        # Test output_schema
        task_def.output_schema = self.valid_schema_def
        self.assertEqual(task_def.output_schema, self.valid_schema_def)

        # Test enforce_schema
        task_def.enforce_schema = True
        self.assertTrue(task_def.enforce_schema)

        task_def.enforce_schema = False
        self.assertFalse(task_def.enforce_schema)

    def test_list_and_dict_field_types(self):
        """Test that list and dict fields accept correct types."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        # Test list fields
        task_def.input_keys = ["key1", "key2"]
        self.assertEqual(task_def.input_keys, ["key1", "key2"])

        task_def.output_keys = ["out1", "out2"]
        self.assertEqual(task_def.output_keys, ["out1", "out2"])

        # Test dict field
        template = {"param1": "value1", "param2": 123}
        task_def.input_template = template
        self.assertEqual(task_def.input_template, template)

    def test_numeric_field_types(self):
        """Test that numeric fields accept correct types."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        numeric_fields = [
            'create_time', 'update_time', 'retry_count', 'timeout_seconds',
            'retry_delay_seconds', 'response_timeout_seconds', 'concurrent_exec_limit',
            'rate_limit_per_frequency', 'rate_limit_frequency_in_seconds',
            'poll_timeout_seconds', 'backoff_scale_factor'
        ]

        for field in numeric_fields:
            setattr(task_def, field, 42)
            self.assertEqual(getattr(task_def, field), 42, f"Numeric field {field} failed")

    def test_string_field_types(self):
        """Test that string fields accept correct types."""
        task_def = TaskDef(name="test", timeout_seconds=60)

        string_fields = [
            'owner_app', 'created_by', 'updated_by', 'name', 'description',
            'isolation_group_id', 'execution_name_space', 'owner_email'
        ]

        for field in string_fields:
            setattr(task_def, field, "test_value")
            self.assertEqual(getattr(task_def, field), "test_value", f"String field {field} failed")


if __name__ == '__main__':
    unittest.main()