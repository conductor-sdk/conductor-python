import unittest
from unittest.mock import Mock
from conductor.client.http.models import WorkflowSchedule


class TestWorkflowScheduleBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for WorkflowSchedule model.

    These tests ensure that:
    - All existing fields continue to exist
    - Field types remain unchanged
    - Constructor behavior remains consistent
    - Property getters/setters work as expected
    - Core methods (to_dict, to_str, __eq__, __ne__) exist

    Principle: ✅ Allow additions, ❌ Prevent removals/changes
    """

    def setUp(self):
        """Set up test fixtures with valid data for all known fields."""
        # Mock StartWorkflowRequest since it's a complex type
        self.mock_start_workflow_request = Mock()
        self.mock_start_workflow_request.to_dict.return_value = {"mocked": "data"}

        self.valid_data = {
            'name': 'test_schedule',
            'cron_expression': '0 0 * * *',
            'run_catchup_schedule_instances': True,
            'paused': False,
            'start_workflow_request': self.mock_start_workflow_request,
            'schedule_start_time': 1640995200,  # Unix timestamp
            'schedule_end_time': 1672531200,
            'create_time': 1640995200,
            'updated_time': 1641081600,
            'created_by': 'test_user',
            'updated_by': 'test_user_2'
        }

    def test_constructor_with_no_parameters(self):
        """Test that constructor works with no parameters (all defaults to None)."""
        schedule = WorkflowSchedule()

        # All fields should be None initially
        self.assertIsNone(schedule.name)
        self.assertIsNone(schedule.cron_expression)
        self.assertIsNone(schedule.run_catchup_schedule_instances)
        self.assertIsNone(schedule.paused)
        self.assertIsNone(schedule.start_workflow_request)
        self.assertIsNone(schedule.schedule_start_time)
        self.assertIsNone(schedule.schedule_end_time)
        self.assertIsNone(schedule.create_time)
        self.assertIsNone(schedule.updated_time)
        self.assertIsNone(schedule.created_by)
        self.assertIsNone(schedule.updated_by)

    def test_constructor_with_all_parameters(self):
        """Test constructor with all existing parameters."""
        schedule = WorkflowSchedule(**self.valid_data)

        # Verify all fields are set correctly
        self.assertEqual(schedule.name, 'test_schedule')
        self.assertEqual(schedule.cron_expression, '0 0 * * *')
        self.assertTrue(schedule.run_catchup_schedule_instances)
        self.assertFalse(schedule.paused)
        self.assertEqual(schedule.start_workflow_request, self.mock_start_workflow_request)
        self.assertEqual(schedule.schedule_start_time, 1640995200)
        self.assertEqual(schedule.schedule_end_time, 1672531200)
        self.assertEqual(schedule.create_time, 1640995200)
        self.assertEqual(schedule.updated_time, 1641081600)
        self.assertEqual(schedule.created_by, 'test_user')
        self.assertEqual(schedule.updated_by, 'test_user_2')

    def test_constructor_with_partial_parameters(self):
        """Test constructor with only some parameters."""
        partial_data = {
            'name': 'partial_schedule',
            'cron_expression': '0 12 * * *',
            'paused': True
        }
        schedule = WorkflowSchedule(**partial_data)

        # Specified fields should be set
        self.assertEqual(schedule.name, 'partial_schedule')
        self.assertEqual(schedule.cron_expression, '0 12 * * *')
        self.assertTrue(schedule.paused)

        # Unspecified fields should be None
        self.assertIsNone(schedule.run_catchup_schedule_instances)
        self.assertIsNone(schedule.start_workflow_request)
        self.assertIsNone(schedule.schedule_start_time)

    def test_all_required_properties_exist(self):
        """Test that all expected properties exist and are accessible."""
        schedule = WorkflowSchedule()

        # Test that all properties exist (should not raise AttributeError)
        required_properties = [
            'name', 'cron_expression', 'run_catchup_schedule_instances',
            'paused', 'start_workflow_request', 'schedule_start_time',
            'schedule_end_time', 'create_time', 'updated_time',
            'created_by', 'updated_by'
        ]

        for prop in required_properties:
            with self.subTest(property=prop):
                # Test getter exists
                self.assertTrue(hasattr(schedule, prop),
                                f"Property '{prop}' should exist")
                # Test getter works
                getattr(schedule, prop)

    def test_property_setters_work(self):
        """Test that all property setters work correctly."""
        schedule = WorkflowSchedule()

        # Test string properties
        schedule.name = 'new_name'
        self.assertEqual(schedule.name, 'new_name')

        schedule.cron_expression = '0 6 * * *'
        self.assertEqual(schedule.cron_expression, '0 6 * * *')

        schedule.created_by = 'setter_user'
        self.assertEqual(schedule.created_by, 'setter_user')

        schedule.updated_by = 'setter_user_2'
        self.assertEqual(schedule.updated_by, 'setter_user_2')

        # Test boolean properties
        schedule.run_catchup_schedule_instances = False
        self.assertFalse(schedule.run_catchup_schedule_instances)

        schedule.paused = True
        self.assertTrue(schedule.paused)

        # Test integer properties
        schedule.schedule_start_time = 999999999
        self.assertEqual(schedule.schedule_start_time, 999999999)

        schedule.schedule_end_time = 888888888
        self.assertEqual(schedule.schedule_end_time, 888888888)

        schedule.create_time = 777777777
        self.assertEqual(schedule.create_time, 777777777)

        schedule.updated_time = 666666666
        self.assertEqual(schedule.updated_time, 666666666)

        # Test object property
        schedule.start_workflow_request = self.mock_start_workflow_request
        self.assertEqual(schedule.start_workflow_request, self.mock_start_workflow_request)

    def test_property_types_are_preserved(self):
        """Test that property types match expected swagger_types."""
        schedule = WorkflowSchedule(**self.valid_data)

        # String fields
        self.assertIsInstance(schedule.name, str)
        self.assertIsInstance(schedule.cron_expression, str)
        self.assertIsInstance(schedule.created_by, str)
        self.assertIsInstance(schedule.updated_by, str)

        # Boolean fields
        self.assertIsInstance(schedule.run_catchup_schedule_instances, bool)
        self.assertIsInstance(schedule.paused, bool)

        # Integer fields
        self.assertIsInstance(schedule.schedule_start_time, int)
        self.assertIsInstance(schedule.schedule_end_time, int)
        self.assertIsInstance(schedule.create_time, int)
        self.assertIsInstance(schedule.updated_time, int)

        # Object field (StartWorkflowRequest)
        self.assertEqual(schedule.start_workflow_request, self.mock_start_workflow_request)

    def test_swagger_types_attribute_exists(self):
        """Test that swagger_types class attribute exists and contains expected fields."""
        self.assertTrue(hasattr(WorkflowSchedule, 'swagger_types'))
        swagger_types = WorkflowSchedule.swagger_types

        expected_types = {
            'name': 'str',
            'cron_expression': 'str',
            'run_catchup_schedule_instances': 'bool',
            'paused': 'bool',
            'start_workflow_request': 'StartWorkflowRequest',
            'schedule_start_time': 'int',
            'schedule_end_time': 'int',
            'create_time': 'int',
            'updated_time': 'int',
            'created_by': 'str',
            'updated_by': 'str'
        }

        # Check that all expected fields exist with correct types
        for field, expected_type in expected_types.items():
            with self.subTest(field=field):
                self.assertIn(field, swagger_types,
                              f"Field '{field}' should exist in swagger_types")
                self.assertEqual(swagger_types[field], expected_type,
                                 f"Field '{field}' should have type '{expected_type}'")

    def test_attribute_map_exists(self):
        """Test that attribute_map class attribute exists and contains expected mappings."""
        self.assertTrue(hasattr(WorkflowSchedule, 'attribute_map'))
        attribute_map = WorkflowSchedule.attribute_map

        expected_mappings = {
            'name': 'name',
            'cron_expression': 'cronExpression',
            'run_catchup_schedule_instances': 'runCatchupScheduleInstances',
            'paused': 'paused',
            'start_workflow_request': 'startWorkflowRequest',
            'schedule_start_time': 'scheduleStartTime',
            'schedule_end_time': 'scheduleEndTime',
            'create_time': 'createTime',
            'updated_time': 'updatedTime',
            'created_by': 'createdBy',
            'updated_by': 'updatedBy'
        }

        # Check that all expected mappings exist
        for field, expected_json_key in expected_mappings.items():
            with self.subTest(field=field):
                self.assertIn(field, attribute_map,
                              f"Field '{field}' should exist in attribute_map")
                self.assertEqual(attribute_map[field], expected_json_key,
                                 f"Field '{field}' should map to '{expected_json_key}'")

    def test_to_dict_method_exists_and_works(self):
        """Test that to_dict method exists and produces expected output."""
        schedule = WorkflowSchedule(**self.valid_data)

        # Method should exist
        self.assertTrue(hasattr(schedule, 'to_dict'))
        self.assertTrue(callable(getattr(schedule, 'to_dict')))

        # Method should return a dictionary
        result = schedule.to_dict()
        self.assertIsInstance(result, dict)

        # Should contain all the fields we set
        self.assertIn('name', result)
        self.assertIn('cron_expression', result)
        self.assertIn('run_catchup_schedule_instances', result)
        self.assertIn('paused', result)
        self.assertIn('start_workflow_request', result)

        # Values should match
        self.assertEqual(result['name'], 'test_schedule')
        self.assertEqual(result['cron_expression'], '0 0 * * *')
        self.assertTrue(result['run_catchup_schedule_instances'])
        self.assertFalse(result['paused'])

    def test_to_str_method_exists_and_works(self):
        """Test that to_str method exists and returns string representation."""
        schedule = WorkflowSchedule(name='test', cron_expression='0 0 * * *')

        # Method should exist
        self.assertTrue(hasattr(schedule, 'to_str'))
        self.assertTrue(callable(getattr(schedule, 'to_str')))

        # Method should return a string
        result = schedule.to_str()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_repr_method_works(self):
        """Test that __repr__ method works."""
        schedule = WorkflowSchedule(name='test')

        # Should return a string representation
        repr_str = repr(schedule)
        self.assertIsInstance(repr_str, str)
        self.assertGreater(len(repr_str), 0)

    def test_equality_methods_exist_and_work(self):
        """Test that __eq__ and __ne__ methods exist and work correctly."""
        schedule1 = WorkflowSchedule(name='test', paused=True)
        schedule2 = WorkflowSchedule(name='test', paused=True)
        schedule3 = WorkflowSchedule(name='different', paused=True)

        # Test equality
        self.assertEqual(schedule1, schedule2)
        self.assertNotEqual(schedule1, schedule3)

        # Test inequality
        self.assertFalse(schedule1 != schedule2)
        self.assertTrue(schedule1 != schedule3)

        # Test with non-WorkflowSchedule object
        self.assertNotEqual(schedule1, "not a schedule")
        self.assertTrue(schedule1 != "not a schedule")

    def test_discriminator_attribute_exists(self):
        """Test that discriminator attribute exists and is set to None."""
        schedule = WorkflowSchedule()
        self.assertTrue(hasattr(schedule, 'discriminator'))
        self.assertIsNone(schedule.discriminator)

    def test_private_attributes_exist(self):
        """Test that all private attributes are properly initialized."""
        schedule = WorkflowSchedule()

        private_attrs = [
            '_name', '_cron_expression', '_run_catchup_schedule_instances',
            '_paused', '_start_workflow_request', '_schedule_start_time',
            '_schedule_end_time', '_create_time', '_updated_time',
            '_created_by', '_updated_by'
        ]

        for attr in private_attrs:
            with self.subTest(attribute=attr):
                self.assertTrue(hasattr(schedule, attr),
                                f"Private attribute '{attr}' should exist")
                self.assertIsNone(getattr(schedule, attr),
                                  f"Private attribute '{attr}' should be None by default")

    def test_none_values_are_handled_correctly(self):
        """Test that None values can be set and retrieved correctly."""
        schedule = WorkflowSchedule(**self.valid_data)

        # Set all fields to None
        schedule.name = None
        schedule.cron_expression = None
        schedule.run_catchup_schedule_instances = None
        schedule.paused = None
        schedule.start_workflow_request = None
        schedule.schedule_start_time = None
        schedule.schedule_end_time = None
        schedule.create_time = None
        schedule.updated_time = None
        schedule.created_by = None
        schedule.updated_by = None

        # Verify all are None
        self.assertIsNone(schedule.name)
        self.assertIsNone(schedule.cron_expression)
        self.assertIsNone(schedule.run_catchup_schedule_instances)
        self.assertIsNone(schedule.paused)
        self.assertIsNone(schedule.start_workflow_request)
        self.assertIsNone(schedule.schedule_start_time)
        self.assertIsNone(schedule.schedule_end_time)
        self.assertIsNone(schedule.create_time)
        self.assertIsNone(schedule.updated_time)
        self.assertIsNone(schedule.created_by)
        self.assertIsNone(schedule.updated_by)

    def test_constructor_signature_compatibility(self):
        """Test that constructor signature remains compatible."""
        # Test positional arguments work (in order)
        schedule = WorkflowSchedule(
            'test_name',  # name
            '0 0 * * *',  # cron_expression
            True,  # run_catchup_schedule_instances
            False,  # paused
            self.mock_start_workflow_request,  # start_workflow_request
            1640995200,  # schedule_start_time
            1672531200,  # schedule_end_time
            1640995200,  # create_time
            1641081600,  # updated_time
            'creator',  # created_by
            'updater'  # updated_by
        )

        self.assertEqual(schedule.name, 'test_name')
        self.assertEqual(schedule.cron_expression, '0 0 * * *')
        self.assertTrue(schedule.run_catchup_schedule_instances)
        self.assertFalse(schedule.paused)
        self.assertEqual(schedule.created_by, 'creator')
        self.assertEqual(schedule.updated_by, 'updater')


if __name__ == '__main__':
    unittest.main()