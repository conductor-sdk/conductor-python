import unittest
from conductor.client.http.models.task_result_status import TaskResultStatus


class TestTaskResultStatusBackwardCompatibility(unittest.TestCase):
    """
    Backward compatibility tests for TaskResultStatus enum.

    Principles:
    - ✅ Allow additions (new enum values)
    - ❌ Prevent removals (removed enum values)
    - ❌ Prevent changes (enum value changes)
    """

    def setUp(self):
        """Set up test fixtures with expected enum values that must always exist."""
        # These are the enum values that existed in the original version
        # and must remain for backward compatibility
        self.required_enum_values = {
            'COMPLETED',
            'FAILED',
            'FAILED_WITH_TERMINAL_ERROR',
            'IN_PROGRESS'
        }

        self.required_string_values = {
            'COMPLETED',
            'FAILED',
            'FAILED_WITH_TERMINAL_ERROR',
            'IN_PROGRESS'
        }

    def test_all_required_enum_values_exist(self):
        """Test that all originally existing enum values still exist."""
        actual_enum_names = {member.name for member in TaskResultStatus}

        missing_values = self.required_enum_values - actual_enum_names
        self.assertEqual(
            len(missing_values), 0,
            f"Missing required enum values: {missing_values}. "
            f"Removing enum values breaks backward compatibility."
        )

    def test_enum_values_unchanged(self):
        """Test that existing enum values haven't changed their string representation."""
        for enum_name in self.required_enum_values:
            with self.subTest(enum_value=enum_name):
                # Verify the enum member exists
                self.assertTrue(
                    hasattr(TaskResultStatus, enum_name),
                    f"Enum value {enum_name} no longer exists"
                )

                enum_member = getattr(TaskResultStatus, enum_name)

                # Test the string value matches expected
                expected_string_value = enum_name
                self.assertEqual(
                    enum_member.value, expected_string_value,
                    f"Enum {enum_name} value changed from '{expected_string_value}' to '{enum_member.value}'"
                )

    def test_str_method_backward_compatibility(self):
        """Test that __str__ method returns expected values for existing enums."""
        for enum_name in self.required_enum_values:
            with self.subTest(enum_value=enum_name):
                enum_member = getattr(TaskResultStatus, enum_name)
                expected_str = enum_name
                actual_str = str(enum_member)

                self.assertEqual(
                    actual_str, expected_str,
                    f"str({enum_name}) changed from '{expected_str}' to '{actual_str}'"
                )

    def test_enum_inheritance_unchanged(self):
        """Test that TaskResultStatus still inherits from expected base classes."""
        # Verify it's still an Enum
        from enum import Enum
        self.assertTrue(
            issubclass(TaskResultStatus, Enum),
            "TaskResultStatus no longer inherits from Enum"
        )

        # Verify it's still a str enum (can be used as string)
        self.assertTrue(
            issubclass(TaskResultStatus, str),
            "TaskResultStatus no longer inherits from str"
        )

    def test_enum_can_be_constructed_from_string(self):
        """Test that existing enum values can still be constructed from strings."""
        for string_value in self.required_string_values:
            with self.subTest(string_value=string_value):
                try:
                    enum_instance = TaskResultStatus(string_value)
                    self.assertEqual(
                        enum_instance.value, string_value,
                        f"TaskResultStatus('{string_value}') does not have expected value"
                    )
                except (ValueError, TypeError) as e:
                    self.fail(
                        f"TaskResultStatus('{string_value}') construction failed: {e}. "
                        f"This breaks backward compatibility."
                    )

    def test_enum_equality_with_strings(self):
        """Test that enum values can still be compared with strings."""
        for enum_name in self.required_enum_values:
            with self.subTest(enum_value=enum_name):
                enum_member = getattr(TaskResultStatus, enum_name)

                # Test equality with string value
                self.assertEqual(
                    enum_member, enum_name,
                    f"TaskResultStatus.{enum_name} != '{enum_name}' (string comparison failed)"
                )

    def test_enum_serialization_compatibility(self):
        """Test that enum values serialize to expected strings for JSON/API compatibility."""
        for enum_name in self.required_enum_values:
            with self.subTest(enum_value=enum_name):
                enum_member = getattr(TaskResultStatus, enum_name)

                # Test that the enum value can be used in JSON-like contexts
                serialized = str(enum_member)
                self.assertEqual(
                    serialized, enum_name,
                    f"Serialization of {enum_name} changed from '{enum_name}' to '{serialized}'"
                )

    def test_enum_membership_operations(self):
        """Test that existing enum values work with membership operations."""
        all_members = list(TaskResultStatus)
        all_member_names = [member.name for member in all_members]

        for required_name in self.required_enum_values:
            with self.subTest(enum_value=required_name):
                self.assertIn(
                    required_name, all_member_names,
                    f"Required enum value {required_name} not found in TaskResultStatus members"
                )

    def test_addition_tolerance(self):
        """Test that the enum can have additional values (forward compatibility)."""
        # This test ensures that if new enum values are added,
        # the existing functionality still works
        actual_values = {member.name for member in TaskResultStatus}

        # Verify we have at least the required values
        self.assertTrue(
            self.required_enum_values.issubset(actual_values),
            f"Missing required enum values: {self.required_enum_values - actual_values}"
        )

        # Additional values are allowed (this should not fail)
        additional_values = actual_values - self.required_enum_values
        if additional_values:
            # Log that additional values exist (this is OK for backward compatibility)
            print(f"INFO: Additional enum values found (this is OK): {additional_values}")

    def test_enum_immutability(self):
        """Test that enum values are immutable."""
        for enum_name in self.required_enum_values:
            with self.subTest(enum_value=enum_name):
                enum_member = getattr(TaskResultStatus, enum_name)

                # Attempt to modify the enum value should fail
                with self.assertRaises((AttributeError, TypeError)):
                    enum_member.value = "MODIFIED"


if __name__ == '__main__':
    unittest.main()