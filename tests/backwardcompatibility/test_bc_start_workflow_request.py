import unittest
from conductor.client.http.models import StartWorkflowRequest, IdempotencyStrategy


class TestStartWorkflowRequestBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility test for StartWorkflowRequest.

    Principle:
    ✅ Allow additions (new fields, new enum values)
    ❌ Prevent removals (missing fields, removed enum values)
    ❌ Prevent changes (field type changes, field name changes)
    """

    def setUp(self):
        """Set up test fixtures with known valid data."""
        self.valid_name = "test_workflow"
        self.valid_version = 1
        self.valid_correlation_id = "test-correlation-id"
        self.valid_input = {"key": "value"}
        self.valid_task_to_domain = {"task1": "domain1"}
        self.valid_priority = 5
        self.valid_created_by = "test_user"
        self.valid_idempotency_key = "test-key"
        self.valid_external_path = "/path/to/storage"

    def test_required_fields_still_exist(self):
        """Test that all existing required fields still exist."""
        # 'name' is the only required field - constructor should work with just name
        request = StartWorkflowRequest(name=self.valid_name)
        self.assertEqual(request.name, self.valid_name)

        # Verify the field exists and is accessible
        self.assertTrue(hasattr(request, 'name'))
        self.assertTrue(hasattr(request, '_name'))

    def test_all_existing_fields_still_exist(self):
        """Test that all existing fields (required and optional) still exist."""
        expected_fields = [
            'name', 'version', 'correlation_id', 'input', 'task_to_domain',
            'workflow_def', 'external_input_payload_storage_path', 'priority',
            'created_by', 'idempotency_key', 'idempotency_strategy'
        ]

        request = StartWorkflowRequest(name=self.valid_name)

        for field in expected_fields:
            with self.subTest(field=field):
                # Check property exists
                self.assertTrue(hasattr(request, field),
                                f"Field '{field}' no longer exists")
                # Check private attribute exists
                private_field = f"_{field}"
                self.assertTrue(hasattr(request, private_field),
                                f"Private field '{private_field}' no longer exists")

    def test_field_types_unchanged(self):
        """Test that existing field types haven't changed."""
        expected_types = {
            'name': str,
            'version': (int, type(None)),
            'correlation_id': (str, type(None)),
            'input': (dict, type(None)),
            'task_to_domain': (dict, type(None)),
            'priority': (int, type(None)),
            'created_by': (str, type(None)),
            'idempotency_key': (str, type(None)),
            'external_input_payload_storage_path': (str, type(None))
        }

        request = StartWorkflowRequest(
            name=self.valid_name,
            version=self.valid_version,
            correlation_id=self.valid_correlation_id,
            input=self.valid_input,
            task_to_domain=self.valid_task_to_domain,
            priority=self.valid_priority,
            created_by=self.valid_created_by,
            idempotency_key=self.valid_idempotency_key,
            external_input_payload_storage_path=self.valid_external_path
        )

        for field, expected_type in expected_types.items():
            with self.subTest(field=field):
                value = getattr(request, field)
                if isinstance(expected_type, tuple):
                    self.assertIsInstance(value, expected_type,
                                          f"Field '{field}' type changed")
                else:
                    self.assertIsInstance(value, expected_type,
                                          f"Field '{field}' type changed")

    def test_constructor_backward_compatibility(self):
        """Test that constructor signature remains backward compatible."""
        # Test with minimal required parameters (original behavior)
        request1 = StartWorkflowRequest(name=self.valid_name)
        self.assertEqual(request1.name, self.valid_name)

        # Test with all original parameters
        request2 = StartWorkflowRequest(
            name=self.valid_name,
            version=self.valid_version,
            correlation_id=self.valid_correlation_id,
            input=self.valid_input,
            task_to_domain=self.valid_task_to_domain,
            workflow_def=None,  # This would be a WorkflowDef object
            external_input_payload_storage_path=self.valid_external_path,
            priority=self.valid_priority,
            created_by=self.valid_created_by,
            idempotency_key=self.valid_idempotency_key,
            idempotency_strategy=IdempotencyStrategy.RETURN_EXISTING
        )

        # Verify all values are set correctly
        self.assertEqual(request2.name, self.valid_name)
        self.assertEqual(request2.version, self.valid_version)
        self.assertEqual(request2.correlation_id, self.valid_correlation_id)
        self.assertEqual(request2.input, self.valid_input)
        self.assertEqual(request2.task_to_domain, self.valid_task_to_domain)
        self.assertEqual(request2.priority, self.valid_priority)
        self.assertEqual(request2.created_by, self.valid_created_by)
        self.assertEqual(request2.idempotency_key, self.valid_idempotency_key)
        self.assertEqual(request2.idempotency_strategy, IdempotencyStrategy.RETURN_EXISTING)

    def test_property_setters_still_work(self):
        """Test that all property setters still work as expected."""
        request = StartWorkflowRequest(name=self.valid_name)

        # Test setting each property
        request.version = self.valid_version
        self.assertEqual(request.version, self.valid_version)

        request.correlation_id = self.valid_correlation_id
        self.assertEqual(request.correlation_id, self.valid_correlation_id)

        request.input = self.valid_input
        self.assertEqual(request.input, self.valid_input)

        request.task_to_domain = self.valid_task_to_domain
        self.assertEqual(request.task_to_domain, self.valid_task_to_domain)

        request.priority = self.valid_priority
        self.assertEqual(request.priority, self.valid_priority)

        request.created_by = self.valid_created_by
        self.assertEqual(request.created_by, self.valid_created_by)

        request.idempotency_key = self.valid_idempotency_key
        self.assertEqual(request.idempotency_key, self.valid_idempotency_key)

        request.idempotency_strategy = IdempotencyStrategy.RETURN_EXISTING
        self.assertEqual(request.idempotency_strategy, IdempotencyStrategy.RETURN_EXISTING)

    def test_enum_values_still_exist(self):
        """Test that existing enum values haven't been removed."""
        # Test that existing IdempotencyStrategy values still exist
        self.assertTrue(hasattr(IdempotencyStrategy, 'FAIL'))
        self.assertTrue(hasattr(IdempotencyStrategy, 'RETURN_EXISTING'))

        # Test that enum values work as expected
        self.assertEqual(IdempotencyStrategy.FAIL, "FAIL")
        self.assertEqual(IdempotencyStrategy.RETURN_EXISTING, "RETURN_EXISTING")

        # Test that enum values can be used in the model
        request = StartWorkflowRequest(
            name=self.valid_name,
            idempotency_strategy=IdempotencyStrategy.FAIL
        )
        self.assertEqual(request.idempotency_strategy, IdempotencyStrategy.FAIL)

        request.idempotency_strategy = IdempotencyStrategy.RETURN_EXISTING
        self.assertEqual(request.idempotency_strategy, IdempotencyStrategy.RETURN_EXISTING)

    def test_idempotency_default_behavior(self):
        """Test that idempotency default behavior is preserved."""
        # When no idempotency_key is provided, strategy should default to FAIL
        request1 = StartWorkflowRequest(name=self.valid_name)
        self.assertIsNone(request1.idempotency_key)
        self.assertEqual(request1.idempotency_strategy, IdempotencyStrategy.FAIL)

        # When idempotency_key is provided without strategy, should default to FAIL
        request2 = StartWorkflowRequest(
            name=self.valid_name,
            idempotency_key=self.valid_idempotency_key
        )
        self.assertEqual(request2.idempotency_key, self.valid_idempotency_key)
        self.assertEqual(request2.idempotency_strategy, IdempotencyStrategy.FAIL)

        # When both are provided, should use provided strategy
        request3 = StartWorkflowRequest(
            name=self.valid_name,
            idempotency_key=self.valid_idempotency_key,
            idempotency_strategy=IdempotencyStrategy.RETURN_EXISTING
        )
        self.assertEqual(request3.idempotency_key, self.valid_idempotency_key)
        self.assertEqual(request3.idempotency_strategy, IdempotencyStrategy.RETURN_EXISTING)

    def test_swagger_types_dict_exists(self):
        """Test that swagger_types class attribute still exists with expected mappings."""
        self.assertTrue(hasattr(StartWorkflowRequest, 'swagger_types'))

        expected_swagger_types = {
            'name': 'str',
            'version': 'int',
            'correlation_id': 'str',
            'input': 'dict(str, object)',
            'task_to_domain': 'dict(str, str)',
            'workflow_def': 'WorkflowDef',
            'external_input_payload_storage_path': 'str',
            'priority': 'int',
            'created_by': 'str',
            'idempotency_key': 'str',
            'idempotency_strategy': 'str'
        }

        swagger_types = StartWorkflowRequest.swagger_types

        for field, expected_type in expected_swagger_types.items():
            with self.subTest(field=field):
                self.assertIn(field, swagger_types,
                              f"Field '{field}' missing from swagger_types")
                self.assertEqual(swagger_types[field], expected_type,
                                 f"Field '{field}' type changed in swagger_types")

    def test_attribute_map_exists(self):
        """Test that attribute_map class attribute still exists with expected mappings."""
        self.assertTrue(hasattr(StartWorkflowRequest, 'attribute_map'))

        expected_attribute_map = {
            'name': 'name',
            'version': 'version',
            'correlation_id': 'correlationId',
            'input': 'input',
            'task_to_domain': 'taskToDomain',
            'workflow_def': 'workflowDef',
            'external_input_payload_storage_path': 'externalInputPayloadStoragePath',
            'priority': 'priority',
            'created_by': 'createdBy',
            'idempotency_key': 'idempotencyKey',
            'idempotency_strategy': 'idempotencyStrategy'
        }

        attribute_map = StartWorkflowRequest.attribute_map

        for field, expected_json_key in expected_attribute_map.items():
            with self.subTest(field=field):
                self.assertIn(field, attribute_map,
                              f"Field '{field}' missing from attribute_map")
                self.assertEqual(attribute_map[field], expected_json_key,
                                 f"Field '{field}' JSON mapping changed in attribute_map")

    def test_to_dict_method_exists(self):
        """Test that to_dict method still exists and works."""
        request = StartWorkflowRequest(
            name=self.valid_name,
            version=self.valid_version,
            priority=self.valid_priority
        )

        self.assertTrue(hasattr(request, 'to_dict'))
        result = request.to_dict()
        self.assertIsInstance(result, dict)

        # Check that basic fields are present in the dict
        self.assertIn('name', result)
        self.assertEqual(result['name'], self.valid_name)

    def test_equality_methods_exist(self):
        """Test that __eq__ and __ne__ methods still exist and work."""
        request1 = StartWorkflowRequest(name=self.valid_name)
        request2 = StartWorkflowRequest(name=self.valid_name)
        request3 = StartWorkflowRequest(name="different_name")

        # Test __eq__
        self.assertTrue(hasattr(request1, '__eq__'))
        self.assertEqual(request1, request2)
        self.assertNotEqual(request1, request3)

        # Test __ne__
        self.assertTrue(hasattr(request1, '__ne__'))
        self.assertFalse(request1 != request2)
        self.assertTrue(request1 != request3)

    def test_string_methods_exist(self):
        """Test that string representation methods still exist."""
        request = StartWorkflowRequest(name=self.valid_name)

        # Test to_str method
        self.assertTrue(hasattr(request, 'to_str'))
        str_result = request.to_str()
        self.assertIsInstance(str_result, str)

        # Test __repr__ method
        self.assertTrue(hasattr(request, '__repr__'))
        repr_result = repr(request)
        self.assertIsInstance(repr_result, str)


if __name__ == '__main__':
    unittest.main()