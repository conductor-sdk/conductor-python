import unittest
from typing import Dict, List
from conductor.client.http.models.workflow_task import WorkflowTask, CacheConfig
from conductor.client.http.models.state_change_event import StateChangeConfig, StateChangeEventType, StateChangeEvent


class TestWorkflowTaskBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for WorkflowTask model.

    Ensures:
    - All existing fields remain accessible
    - Field types haven't changed
    - Constructor behavior is preserved
    - Existing validation rules still apply
    - New fields can be added without breaking existing code
    """

    def setUp(self):
        """Set up test fixtures with valid test data."""
        self.valid_cache_config = CacheConfig(key="test_key", ttl_in_second=300)

        # Create a valid state change event first
        self.valid_state_change_event = StateChangeEvent(
            type="task_status_changed",
            payload={"task": "${task}", "workflow": "${workflow}"}
        )

        # Create state change config with proper constructor parameters
        self.valid_state_change_config = StateChangeConfig(
            event_type=StateChangeEventType.onStart,
            events=[self.valid_state_change_event]
        )

    def test_required_fields_in_constructor(self):
        """Test that required fields (name, task_reference_name) work in constructor."""
        # Test with only required fields
        task = WorkflowTask(name="test_task", task_reference_name="test_ref")
        self.assertEqual(task.name, "test_task")
        self.assertEqual(task.task_reference_name, "test_ref")

    def test_all_existing_fields_accessible(self):
        """Test that all existing fields can be set and retrieved."""
        task = WorkflowTask(
            name="test_task",
            task_reference_name="test_ref",
            description="test description",
            input_parameters={"key": "value"},
            type="SIMPLE",
            dynamic_task_name_param="dynamic_param",
            case_value_param="case_param",
            case_expression="case_expr",
            script_expression="script_expr",
            decision_cases={"case1": []},
            dynamic_fork_join_tasks_param="fork_join_param",
            dynamic_fork_tasks_param="fork_param",
            dynamic_fork_tasks_input_param_name="fork_input_param",
            default_case=[],
            fork_tasks=[[]],
            start_delay=1000,
            sub_workflow_param=None,
            join_on=["task1", "task2"],
            sink="test_sink",
            optional=True,
            task_definition=None,
            rate_limited=False,
            default_exclusive_join_task=["join_task"],
            async_complete=True,
            loop_condition="condition",
            loop_over=[],
            retry_count=3,
            evaluator_type="javascript",
            expression="test_expression",
            workflow_task_type="SIMPLE",
            on_state_change={"onStart": self.valid_state_change_config.events},
            cache_config=self.valid_cache_config
        )

        # Verify all fields are accessible and have correct values
        self.assertEqual(task.name, "test_task")
        self.assertEqual(task.task_reference_name, "test_ref")
        self.assertEqual(task.description, "test description")
        self.assertEqual(task.input_parameters, {"key": "value"})
        self.assertEqual(task.type, "SIMPLE")
        self.assertEqual(task.dynamic_task_name_param, "dynamic_param")
        self.assertEqual(task.case_value_param, "case_param")
        self.assertEqual(task.case_expression, "case_expr")
        self.assertEqual(task.script_expression, "script_expr")
        self.assertEqual(task.decision_cases, {"case1": []})
        self.assertEqual(task.dynamic_fork_join_tasks_param, "fork_join_param")
        self.assertEqual(task.dynamic_fork_tasks_param, "fork_param")
        self.assertEqual(task.dynamic_fork_tasks_input_param_name, "fork_input_param")
        self.assertEqual(task.default_case, [])
        self.assertEqual(task.fork_tasks, [[]])
        self.assertEqual(task.start_delay, 1000)
        self.assertIsNone(task.sub_workflow_param)
        self.assertEqual(task.join_on, ["task1", "task2"])
        self.assertEqual(task.sink, "test_sink")
        self.assertTrue(task.optional)
        self.assertIsNone(task.task_definition)
        self.assertFalse(task.rate_limited)
        self.assertEqual(task.default_exclusive_join_task, ["join_task"])
        self.assertTrue(task.async_complete)
        self.assertEqual(task.loop_condition, "condition")
        self.assertEqual(task.loop_over, [])
        self.assertEqual(task.retry_count, 3)
        self.assertEqual(task.evaluator_type, "javascript")
        self.assertEqual(task.expression, "test_expression")
        self.assertEqual(task.workflow_task_type, "SIMPLE")
        self.assertEqual(task.on_state_change, {"onStart": self.valid_state_change_config.events})
        self.assertEqual(task.cache_config, self.valid_cache_config)

    def test_field_types_unchanged(self):
        """Test that existing field types haven't changed."""
        task = WorkflowTask(name="test", task_reference_name="ref")

        # String fields
        task.name = "string_value"
        task.task_reference_name = "string_value"
        task.description = "string_value"
        task.type = "string_value"
        task.dynamic_task_name_param = "string_value"
        task.case_value_param = "string_value"
        task.case_expression = "string_value"
        task.script_expression = "string_value"
        task.dynamic_fork_join_tasks_param = "string_value"
        task.dynamic_fork_tasks_param = "string_value"
        task.dynamic_fork_tasks_input_param_name = "string_value"
        task.sink = "string_value"
        task.loop_condition = "string_value"
        task.evaluator_type = "string_value"
        task.expression = "string_value"
        task.workflow_task_type = "string_value"

        # Dictionary fields
        task.input_parameters = {"key": "value"}
        task.decision_cases = {"case": []}

        # List fields
        task.default_case = []
        task.fork_tasks = [[]]
        task.join_on = ["task1"]
        task.default_exclusive_join_task = ["task1"]
        task.loop_over = []

        # Integer fields
        task.start_delay = 100
        task.retry_count = 5

        # Boolean fields
        task.optional = True
        task.rate_limited = False
        task.async_complete = True

        # Complex object fields
        task.cache_config = self.valid_cache_config

        # All assignments should succeed without type errors
        self.assertIsInstance(task.name, str)
        self.assertIsInstance(task.input_parameters, dict)
        self.assertIsInstance(task.default_case, list)
        self.assertIsInstance(task.start_delay, int)
        self.assertIsInstance(task.optional, bool)
        self.assertIsInstance(task.cache_config, CacheConfig)

    def test_property_setters_work(self):
        """Test that all property setters continue to work."""
        task = WorkflowTask(name="test", task_reference_name="ref")

        # Test setter functionality
        task.name = "new_name"
        self.assertEqual(task.name, "new_name")

        task.description = "new_description"
        self.assertEqual(task.description, "new_description")

        task.input_parameters = {"new_key": "new_value"}
        self.assertEqual(task.input_parameters, {"new_key": "new_value"})

        task.optional = False
        self.assertFalse(task.optional)

        task.retry_count = 10
        self.assertEqual(task.retry_count, 10)

    def test_none_values_accepted(self):
        """Test that None values are properly handled for optional fields."""
        task = WorkflowTask(name="test", task_reference_name="ref")

        # These fields should accept None
        optional_fields = [
            'description', 'input_parameters', 'type', 'dynamic_task_name_param',
            'case_value_param', 'case_expression', 'script_expression', 'decision_cases',
            'dynamic_fork_join_tasks_param', 'dynamic_fork_tasks_param',
            'dynamic_fork_tasks_input_param_name', 'default_case', 'fork_tasks',
            'start_delay', 'sub_workflow_param', 'join_on', 'sink', 'optional',
            'task_definition', 'rate_limited', 'default_exclusive_join_task',
            'async_complete', 'loop_condition', 'loop_over', 'retry_count',
            'evaluator_type', 'expression', 'workflow_task_type'
        ]

        for field in optional_fields:
            setattr(task, field, None)
            self.assertIsNone(getattr(task, field))

    def test_special_properties_behavior(self):
        """Test special properties like on_state_change that have custom setters."""
        task = WorkflowTask(name="test", task_reference_name="ref")

        # Test on_state_change setter behavior
        state_change_event = StateChangeEvent(
            type="task_status_changed",
            payload={"task": "${task}", "workflow": "${workflow}"}
        )
        state_change_config = StateChangeConfig(
            event_type=StateChangeEventType.onSuccess,
            events=[state_change_event]
        )
        task.on_state_change = state_change_config

        # The setter should create a dictionary with state_change.type (string) as key
        # and state_change.events as value
        expected_dict = {
            "onSuccess": state_change_config.events
        }
        self.assertEqual(task.on_state_change, expected_dict)

    def test_cache_config_integration(self):
        """Test CacheConfig integration works as expected."""
        cache_config = CacheConfig(key="test_cache", ttl_in_second=600)
        task = WorkflowTask(
            name="test",
            task_reference_name="ref",
            cache_config=cache_config
        )

        self.assertEqual(task.cache_config, cache_config)
        self.assertEqual(task.cache_config.key, "test_cache")
        self.assertEqual(task.cache_config.ttl_in_second, 600)

    def test_to_dict_method_exists(self):
        """Test that to_dict method exists and works."""
        task = WorkflowTask(
            name="test",
            task_reference_name="ref",
            description="test desc"
        )

        result = task.to_dict()
        self.assertIsInstance(result, dict)
        self.assertIn('name', result)
        self.assertIn('task_reference_name', result)
        self.assertIn('description', result)

    def test_str_representation_methods(self):
        """Test string representation methods exist."""
        task = WorkflowTask(name="test", task_reference_name="ref")

        # Test to_str method
        str_result = task.to_str()
        self.assertIsInstance(str_result, str)

        # Test __repr__ method
        repr_result = repr(task)
        self.assertIsInstance(repr_result, str)

    def test_equality_methods(self):
        """Test equality comparison methods work."""
        task1 = WorkflowTask(name="test", task_reference_name="ref")
        task2 = WorkflowTask(name="test", task_reference_name="ref")
        task3 = WorkflowTask(name="different", task_reference_name="ref")

        # Test __eq__
        self.assertEqual(task1, task2)
        self.assertNotEqual(task1, task3)

        # Test __ne__
        self.assertFalse(task1 != task2)
        self.assertTrue(task1 != task3)

    def test_swagger_types_attribute_map_exist(self):
        """Test that swagger_types and attribute_map class attributes exist."""
        self.assertTrue(hasattr(WorkflowTask, 'swagger_types'))
        self.assertTrue(hasattr(WorkflowTask, 'attribute_map'))
        self.assertIsInstance(WorkflowTask.swagger_types, dict)
        self.assertIsInstance(WorkflowTask.attribute_map, dict)

        # Test that all expected fields are in swagger_types
        expected_fields = [
            'name', 'task_reference_name', 'description', 'input_parameters',
            'type', 'dynamic_task_name_param', 'case_value_param', 'case_expression',
            'script_expression', 'decision_cases', 'dynamic_fork_join_tasks_param',
            'dynamic_fork_tasks_param', 'dynamic_fork_tasks_input_param_name',
            'default_case', 'fork_tasks', 'start_delay', 'sub_workflow_param',
            'join_on', 'sink', 'optional', 'task_definition', 'rate_limited',
            'default_exclusive_join_task', 'async_complete', 'loop_condition',
            'loop_over', 'retry_count', 'evaluator_type', 'expression',
            'workflow_task_type', 'on_state_change', 'cache_config'
        ]

        for field in expected_fields:
            self.assertIn(field, WorkflowTask.swagger_types)
            self.assertIn(field, WorkflowTask.attribute_map)

    def test_discriminator_attribute_exists(self):
        """Test that discriminator attribute exists and is properly set."""
        task = WorkflowTask(name="test", task_reference_name="ref")
        self.assertTrue(hasattr(task, 'discriminator'))
        self.assertIsNone(task.discriminator)

    def test_complex_nested_structures(self):
        """Test handling of complex nested structures."""
        # Test with nested WorkflowTask structures
        nested_task = WorkflowTask(name="nested", task_reference_name="nested_ref")

        task = WorkflowTask(
            name="parent",
            task_reference_name="parent_ref",
            decision_cases={"case1": [nested_task]},
            default_case=[nested_task],
            fork_tasks=[[nested_task]],
            loop_over=[nested_task]
        )

        self.assertEqual(len(task.decision_cases["case1"]), 1)
        self.assertEqual(task.decision_cases["case1"][0].name, "nested")
        self.assertEqual(len(task.default_case), 1)
        self.assertEqual(task.default_case[0].name, "nested")


class TestCacheConfigBackwardCompatibility(unittest.TestCase):
    """Backward compatibility test for CacheConfig model."""

    def test_cache_config_required_fields(self):
        """Test CacheConfig constructor with required fields."""
        cache_config = CacheConfig(key="test_key", ttl_in_second=300)
        self.assertEqual(cache_config.key, "test_key")
        self.assertEqual(cache_config.ttl_in_second, 300)

    def test_cache_config_property_setters(self):
        """Test CacheConfig property setters work."""
        cache_config = CacheConfig(key="initial", ttl_in_second=100)

        cache_config.key = "updated_key"
        cache_config.ttl_in_second = 500

        self.assertEqual(cache_config.key, "updated_key")
        self.assertEqual(cache_config.ttl_in_second, 500)

    def test_cache_config_attributes_exist(self):
        """Test that CacheConfig has required class attributes."""
        self.assertTrue(hasattr(CacheConfig, 'swagger_types'))
        self.assertTrue(hasattr(CacheConfig, 'attribute_map'))

        expected_swagger_types = {'key': 'str', 'ttl_in_second': 'int'}
        expected_attribute_map = {'key': 'key', 'ttl_in_second': 'ttlInSecond'}

        self.assertEqual(CacheConfig.swagger_types, expected_swagger_types)
        self.assertEqual(CacheConfig.attribute_map, expected_attribute_map)


if __name__ == '__main__':
    unittest.main()