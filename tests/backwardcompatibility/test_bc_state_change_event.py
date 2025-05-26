import unittest
from typing import Dict, List
from conductor.client.http.models import StateChangeEventType, StateChangeEvent, StateChangeConfig


class TestStateChangeEventBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for StateChangeEvent models.

    Tests ensure that:
    - ✅ Allow additions (new fields, new enum values)
    - ❌ Prevent removals (missing fields, removed enum values)
    - ❌ Prevent changes (field type changes, field name changes)
    """

    def test_state_change_event_type_enum_values_exist(self):
        """Verify all existing StateChangeEventType enum values still exist."""
        required_enum_values = {
            'onScheduled': 'onScheduled',
            'onStart': 'onStart',
            'onFailed': 'onFailed',
            'onSuccess': 'onSuccess',
            'onCancelled': 'onCancelled'
        }

        for name, value in required_enum_values.items():
            with self.subTest(enum_name=name):
                self.assertTrue(hasattr(StateChangeEventType, name),
                                f"StateChangeEventType.{name} must exist")
                self.assertEqual(getattr(StateChangeEventType, name).value, value,
                                 f"StateChangeEventType.{name} value must be '{value}'")

    def test_state_change_event_type_enum_access(self):
        """Verify StateChangeEventType enum can be accessed by name and value."""
        # Test access by name
        self.assertEqual(StateChangeEventType.onScheduled.name, 'onScheduled')
        self.assertEqual(StateChangeEventType.onStart.name, 'onStart')
        self.assertEqual(StateChangeEventType.onFailed.name, 'onFailed')
        self.assertEqual(StateChangeEventType.onSuccess.name, 'onSuccess')
        self.assertEqual(StateChangeEventType.onCancelled.name, 'onCancelled')

        # Test access by value
        self.assertEqual(StateChangeEventType.onScheduled.value, 'onScheduled')
        self.assertEqual(StateChangeEventType.onStart.value, 'onStart')
        self.assertEqual(StateChangeEventType.onFailed.value, 'onFailed')
        self.assertEqual(StateChangeEventType.onSuccess.value, 'onSuccess')
        self.assertEqual(StateChangeEventType.onCancelled.value, 'onCancelled')

    def test_state_change_event_constructor_signature(self):
        """Verify StateChangeEvent constructor signature remains unchanged."""
        # Test constructor with required parameters
        event = StateChangeEvent(type="test_type", payload={"key": "value"})
        self.assertIsNotNone(event)

        # Test constructor parameter requirements - both should be required
        with self.assertRaises(TypeError):
            StateChangeEvent()  # No parameters

        with self.assertRaises(TypeError):
            StateChangeEvent(type="test")  # Missing payload

        with self.assertRaises(TypeError):
            StateChangeEvent(payload={"key": "value"})  # Missing type

    def test_state_change_event_required_properties(self):
        """Verify StateChangeEvent has all required properties."""
        event = StateChangeEvent(type="test_type", payload={"key": "value"})

        # Test property existence and getter functionality
        self.assertTrue(hasattr(event, 'type'), "StateChangeEvent must have 'type' property")
        self.assertTrue(hasattr(event, 'payload'), "StateChangeEvent must have 'payload' property")

        # Test property values
        self.assertEqual(event.type, "test_type")
        self.assertEqual(event.payload, {"key": "value"})

    def test_state_change_event_property_setters(self):
        """Verify StateChangeEvent property setters work correctly."""
        event = StateChangeEvent(type="initial", payload={})

        # Test type setter
        event.type = "updated_type"
        self.assertEqual(event.type, "updated_type")

        # Test payload setter
        new_payload = {"updated": "payload"}
        event.payload = new_payload
        self.assertEqual(event.payload, new_payload)

    def test_state_change_event_class_attributes(self):
        """Verify StateChangeEvent class has required swagger attributes."""
        # Test swagger_types exists and has correct structure
        self.assertTrue(hasattr(StateChangeEvent, 'swagger_types'))
        swagger_types = StateChangeEvent.swagger_types
        self.assertIn('type', swagger_types)
        self.assertIn('payload', swagger_types)
        self.assertEqual(swagger_types['type'], 'str')
        self.assertEqual(swagger_types['payload'], 'Dict[str, object]')

        # Test attribute_map exists and has correct structure
        self.assertTrue(hasattr(StateChangeEvent, 'attribute_map'))
        attribute_map = StateChangeEvent.attribute_map
        self.assertIn('type', attribute_map)
        self.assertIn('payload', attribute_map)
        self.assertEqual(attribute_map['type'], 'type')
        self.assertEqual(attribute_map['payload'], 'payload')

    def test_state_change_config_constructor_signature(self):
        """Verify StateChangeConfig constructor signature remains unchanged."""
        # Test constructor with no parameters (should work)
        config = StateChangeConfig()
        self.assertIsNotNone(config)

        # Test constructor with event_type only
        config = StateChangeConfig(event_type=StateChangeEventType.onStart)
        self.assertIsNotNone(config)

        # Test constructor with both parameters
        events = [StateChangeEvent("test", {})]
        config = StateChangeConfig(event_type=StateChangeEventType.onSuccess, events=events)
        self.assertIsNotNone(config)

    def test_state_change_config_constructor_behavior(self):
        """Verify StateChangeConfig constructor behavior with different input types."""
        # Test with None (should return early)
        config = StateChangeConfig(event_type=None)
        self.assertIsNotNone(config)

        # Test with single StateChangeEventType
        config = StateChangeConfig(event_type=StateChangeEventType.onStart)
        self.assertEqual(config.type, 'onStart')

        # Test with list of StateChangeEventType
        event_types = [StateChangeEventType.onStart, StateChangeEventType.onSuccess]
        config = StateChangeConfig(event_type=event_types)
        self.assertEqual(config.type, 'onStart,onSuccess')

        # Test with events
        events = [StateChangeEvent("test", {})]
        config = StateChangeConfig(event_type=StateChangeEventType.onFailed, events=events)
        self.assertEqual(config.events, events)

    def test_state_change_config_required_properties(self):
        """Verify StateChangeConfig has all required properties."""
        config = StateChangeConfig(event_type=StateChangeEventType.onScheduled)

        # Test property existence
        self.assertTrue(hasattr(config, 'type'), "StateChangeConfig must have 'type' property")
        self.assertTrue(hasattr(config, 'events'), "StateChangeConfig must have 'events' property")

    def test_state_change_config_property_setters(self):
        """Verify StateChangeConfig property setters work correctly."""
        config = StateChangeConfig()

        # Test type setter (expects StateChangeEventType)
        config.type = StateChangeEventType.onCancelled
        self.assertEqual(config.type, 'onCancelled')

        # Test events setter
        events = [StateChangeEvent("test", {"data": "value"})]
        config.events = events
        self.assertEqual(config.events, events)

    def test_state_change_config_class_attributes(self):
        """Verify StateChangeConfig class has required swagger attributes."""
        # Test swagger_types exists and has correct structure
        self.assertTrue(hasattr(StateChangeConfig, 'swagger_types'))
        swagger_types = StateChangeConfig.swagger_types
        self.assertIn('type', swagger_types)
        self.assertIn('events', swagger_types)
        self.assertEqual(swagger_types['type'], 'str')
        self.assertEqual(swagger_types['events'], 'list[StateChangeEvent]')

        # Test attribute_map exists and has correct structure
        self.assertTrue(hasattr(StateChangeConfig, 'attribute_map'))
        attribute_map = StateChangeConfig.attribute_map
        self.assertIn('type', attribute_map)
        self.assertIn('events', attribute_map)
        self.assertEqual(attribute_map['type'], 'type')
        self.assertEqual(attribute_map['events'], 'events')

    def test_integration_scenario(self):
        """Test complete integration scenario with all components."""
        # Create events
        event1 = StateChangeEvent(type="workflow_started", payload={"workflow_id": "123"})
        event2 = StateChangeEvent(type="task_completed", payload={"task_id": "456"})

        # Create config with single event type
        config1 = StateChangeConfig(
            event_type=StateChangeEventType.onStart,
            events=[event1]
        )

        # Create config with multiple event types
        config2 = StateChangeConfig(
            event_type=[StateChangeEventType.onSuccess, StateChangeEventType.onFailed],
            events=[event1, event2]
        )

        # Verify everything works together
        self.assertEqual(config1.type, 'onStart')
        self.assertEqual(len(config1.events), 1)
        self.assertEqual(config1.events[0].type, "workflow_started")

        self.assertEqual(config2.type, 'onSuccess,onFailed')
        self.assertEqual(len(config2.events), 2)

    def test_type_annotations_compatibility(self):
        """Verify type annotations remain compatible."""
        # This test ensures that the models can still be used with type checking
        event: StateChangeEvent = StateChangeEvent("test", {})
        config: StateChangeConfig = StateChangeConfig()
        event_type: StateChangeEventType = StateChangeEventType.onScheduled

        # Test that assignments work without type errors
        config.type = event_type
        config.events = [event]
        event.type = "new_type"
        event.payload = {"new": "payload"}

        self.assertIsNotNone(event)
        self.assertIsNotNone(config)
        self.assertIsNotNone(event_type)


if __name__ == '__main__':
    unittest.main()