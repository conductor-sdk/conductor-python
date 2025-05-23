import unittest
from conductor.client.http.models import SaveScheduleRequest, StartWorkflowRequest


class TestSaveScheduleRequestBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for SaveScheduleRequest model.

    Principles:
    - ✅ Allow additions (new fields, new enum values)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test fixtures with valid data for all existing fields."""
        # Mock StartWorkflowRequest for testing
        self.start_workflow_request = StartWorkflowRequest() if StartWorkflowRequest else None

        self.valid_data = {
            'name': 'test_schedule',
            'cron_expression': '0 0 * * *',
            'run_catchup_schedule_instances': True,
            'paused': False,
            'start_workflow_request': self.start_workflow_request,
            'created_by': 'test_user',
            'updated_by': 'test_user',
            'schedule_start_time': 1640995200,  # Unix timestamp
            'schedule_end_time': 1672531200  # Unix timestamp
        }

    def test_constructor_with_all_existing_fields(self):
        """Test that constructor accepts all existing fields without errors."""
        # Test constructor with all fields
        request = SaveScheduleRequest(**self.valid_data)

        # Verify all fields are set correctly
        self.assertEqual(request.name, 'test_schedule')
        self.assertEqual(request.cron_expression, '0 0 * * *')
        self.assertTrue(request.run_catchup_schedule_instances)
        self.assertFalse(request.paused)
        self.assertEqual(request.start_workflow_request, self.start_workflow_request)
        self.assertEqual(request.created_by, 'test_user')
        self.assertEqual(request.updated_by, 'test_user')
        self.assertEqual(request.schedule_start_time, 1640995200)
        self.assertEqual(request.schedule_end_time, 1672531200)

    def test_constructor_with_minimal_required_fields(self):
        """Test constructor with only required fields (name and cron_expression)."""
        request = SaveScheduleRequest(
            name='test_schedule',
            cron_expression='0 0 * * *'
        )

        # Required fields should be set
        self.assertEqual(request.name, 'test_schedule')
        self.assertEqual(request.cron_expression, '0 0 * * *')

        # Optional fields should be None or default values
        self.assertIsNone(request.run_catchup_schedule_instances)
        self.assertIsNone(request.paused)
        self.assertIsNone(request.start_workflow_request)
        self.assertIsNone(request.created_by)
        self.assertIsNone(request.updated_by)
        self.assertIsNone(request.schedule_start_time)
        self.assertIsNone(request.schedule_end_time)

    def test_all_expected_attributes_exist(self):
        """Verify all expected attributes exist on the class."""
        expected_attributes = [
            'name', 'cron_expression', 'run_catchup_schedule_instances',
            'paused', 'start_workflow_request', 'created_by', 'updated_by',
            'schedule_start_time', 'schedule_end_time'
        ]

        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')

        for attr in expected_attributes:
            self.assertTrue(hasattr(request, attr),
                            f"Missing expected attribute: {attr}")

    def test_swagger_types_mapping_exists(self):
        """Verify swagger_types mapping contains all expected field types."""
        expected_swagger_types = {
            'name': 'str',
            'cron_expression': 'str',
            'run_catchup_schedule_instances': 'bool',
            'paused': 'bool',
            'start_workflow_request': 'StartWorkflowRequest',
            'created_by': 'str',
            'updated_by': 'str',
            'schedule_start_time': 'int',
            'schedule_end_time': 'int'
        }

        for field, expected_type in expected_swagger_types.items():
            self.assertIn(field, SaveScheduleRequest.swagger_types,
                          f"Missing field in swagger_types: {field}")
            self.assertEqual(SaveScheduleRequest.swagger_types[field], expected_type,
                             f"Type mismatch for field {field}")

    def test_attribute_map_exists(self):
        """Verify attribute_map contains all expected JSON mappings."""
        expected_attribute_map = {
            'name': 'name',
            'cron_expression': 'cronExpression',
            'run_catchup_schedule_instances': 'runCatchupScheduleInstances',
            'paused': 'paused',
            'start_workflow_request': 'startWorkflowRequest',
            'created_by': 'createdBy',
            'updated_by': 'updatedBy',
            'schedule_start_time': 'scheduleStartTime',
            'schedule_end_time': 'scheduleEndTime'
        }

        for field, expected_json_key in expected_attribute_map.items():
            self.assertIn(field, SaveScheduleRequest.attribute_map,
                          f"Missing field in attribute_map: {field}")
            self.assertEqual(SaveScheduleRequest.attribute_map[field], expected_json_key,
                             f"JSON key mismatch for field {field}")

    def test_property_getters_exist(self):
        """Verify all property getters exist and work correctly."""
        request = SaveScheduleRequest(**self.valid_data)

        # Test all getters
        self.assertEqual(request.name, 'test_schedule')
        self.assertEqual(request.cron_expression, '0 0 * * *')
        self.assertTrue(request.run_catchup_schedule_instances)
        self.assertFalse(request.paused)
        self.assertEqual(request.start_workflow_request, self.start_workflow_request)
        self.assertEqual(request.created_by, 'test_user')
        self.assertEqual(request.updated_by, 'test_user')
        self.assertEqual(request.schedule_start_time, 1640995200)
        self.assertEqual(request.schedule_end_time, 1672531200)

    def test_property_setters_exist(self):
        """Verify all property setters exist and work correctly."""
        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')

        # Test all setters
        request.name = 'updated_schedule'
        self.assertEqual(request.name, 'updated_schedule')

        request.cron_expression = '0 12 * * *'
        self.assertEqual(request.cron_expression, '0 12 * * *')

        request.run_catchup_schedule_instances = False
        self.assertFalse(request.run_catchup_schedule_instances)

        request.paused = True
        self.assertTrue(request.paused)

        request.start_workflow_request = self.start_workflow_request
        self.assertEqual(request.start_workflow_request, self.start_workflow_request)

        request.created_by = 'new_user'
        self.assertEqual(request.created_by, 'new_user')

        request.updated_by = 'another_user'
        self.assertEqual(request.updated_by, 'another_user')

        request.schedule_start_time = 1672531200
        self.assertEqual(request.schedule_start_time, 1672531200)

        request.schedule_end_time = 1704067200
        self.assertEqual(request.schedule_end_time, 1704067200)

    def test_field_type_validation_string_fields(self):
        """Test that string fields accept string values."""
        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')

        # String fields should accept string values
        string_fields = ['name', 'cron_expression', 'created_by', 'updated_by']
        for field in string_fields:
            setattr(request, field, 'test_string')
            self.assertEqual(getattr(request, field), 'test_string')

    def test_field_type_validation_boolean_fields(self):
        """Test that boolean fields accept boolean values."""
        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')

        # Boolean fields should accept boolean values
        boolean_fields = ['run_catchup_schedule_instances', 'paused']
        for field in boolean_fields:
            setattr(request, field, True)
            self.assertTrue(getattr(request, field))
            setattr(request, field, False)
            self.assertFalse(getattr(request, field))

    def test_field_type_validation_integer_fields(self):
        """Test that integer fields accept integer values."""
        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')

        # Integer fields should accept integer values
        integer_fields = ['schedule_start_time', 'schedule_end_time']
        for field in integer_fields:
            setattr(request, field, 1234567890)
            self.assertEqual(getattr(request, field), 1234567890)

    def test_to_dict_method_exists(self):
        """Verify to_dict method exists and includes all expected fields."""
        request = SaveScheduleRequest(**self.valid_data)
        result_dict = request.to_dict()

        self.assertIsInstance(result_dict, dict)

        # Check that all fields are present in the dictionary
        expected_fields = [
            'name', 'cron_expression', 'run_catchup_schedule_instances',
            'paused', 'start_workflow_request', 'created_by', 'updated_by',
            'schedule_start_time', 'schedule_end_time'
        ]

        for field in expected_fields:
            self.assertIn(field, result_dict)

    def test_to_str_method_exists(self):
        """Verify to_str method exists and returns a string."""
        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')
        result = request.to_str()

        self.assertIsInstance(result, str)

    def test_repr_method_exists(self):
        """Verify __repr__ method exists and returns a string."""
        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')
        result = repr(request)

        self.assertIsInstance(result, str)

    def test_equality_methods_exist(self):
        """Verify __eq__ and __ne__ methods exist and work correctly."""
        request1 = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')
        request2 = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')
        request3 = SaveScheduleRequest(name='different', cron_expression='0 0 * * *')

        # Test equality
        self.assertEqual(request1, request2)
        self.assertNotEqual(request1, request3)

        # Test inequality with non-SaveScheduleRequest object
        self.assertNotEqual(request1, "not a SaveScheduleRequest")

    def test_discriminator_attribute_exists(self):
        """Verify discriminator attribute exists and is None by default."""
        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')
        self.assertTrue(hasattr(request, 'discriminator'))
        self.assertIsNone(request.discriminator)

    def test_private_attributes_exist(self):
        """Verify all private attributes exist."""
        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')

        expected_private_attrs = [
            '_name', '_cron_expression', '_run_catchup_schedule_instances',
            '_paused', '_start_workflow_request', '_created_by', '_updated_by',
            '_schedule_start_time', '_schedule_end_time'
        ]

        for attr in expected_private_attrs:
            self.assertTrue(hasattr(request, attr),
                            f"Missing expected private attribute: {attr}")

    def test_none_values_handling(self):
        """Test that None values are handled correctly for optional fields."""
        request = SaveScheduleRequest(name='test', cron_expression='0 0 * * *')

        # Optional fields should accept None
        optional_fields = [
            'run_catchup_schedule_instances', 'paused', 'start_workflow_request',
            'created_by', 'updated_by', 'schedule_start_time', 'schedule_end_time'
        ]

        for field in optional_fields:
            setattr(request, field, None)
            self.assertIsNone(getattr(request, field))


if __name__ == '__main__':
    unittest.main()