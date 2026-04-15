import unittest

from memory_os.validation import validate_pipeline, write_payload_validation


class ValidationPipelineTests(unittest.TestCase):
    def test_missing_nodes_fails_schema(self):
        result = validate_pipeline({"schemaVersion": "component@1.0.0"})
        self.assertFalse(result["pass"])
        self.assertIn("schema:nodes_missing", result["schema_errors"])

    def test_invalid_auto_layout_direction_is_warning(self):
        memory = {
            "schemaVersion": "component@1.0.0",
            "nodes": [{"id": "n1", "autoLayout": {"enabled": True, "direction": "DIAGONAL"}}],
        }
        result = validate_pipeline(memory)
        self.assertTrue(result["pass"])
        self.assertIn("rule:invalid_direction:n1", result["rule_warnings"])

    def test_missing_schema_version_in_write_payload_fails(self):
        memory = {"schemaVersion": "component@1.0.0", "nodes": [{"id": "n1"}]}
        result = validate_pipeline(memory, write_payload={"nodes": [{"id": "n1"}]})
        self.assertFalse(result["pass"])
        self.assertIn("write:schema_version_missing", result["write_errors"])

    def test_node_linked_note_requires_node_id(self):
        payload = {
            "schemaVersion": "component@1.0.0",
            "notes": [{"nodeLinked": True, "content": "hello"}],
        }
        errors = write_payload_validation(payload)
        self.assertIn("write:node_link_missing_nodeId:0", errors)

    def test_additive_structure_change_passes(self):
        previous = {"schemaVersion": "component@1.0.0", "nodes": [{"id": "n1", "name": "Button"}]}
        current = {
            "schemaVersion": "component@1.0.0",
            "nodes": [{"id": "n1", "name": "Button"}, {"id": "n2", "name": "Icon"}],
        }

        result = validate_pipeline(current, previous_memory=previous)

        self.assertTrue(result["pass"])
        self.assertEqual([], result["structure_change_errors"])
        self.assertIn("additive", result["structure_change_types"])

    def test_move_rename_delete_blocked_by_default(self):
        previous = {
            "schemaVersion": "component@1.0.0",
            "nodes": [
                {"id": "n1", "name": "Button", "parentId": "root"},
                {"id": "n2", "name": "Text", "parentId": "root"},
                {"id": "n3", "name": "Icon", "parentId": "root"},
            ],
        }
        current = {
            "schemaVersion": "component@1.0.0",
            "nodes": [
                {"id": "n1", "name": "Button/Primary", "parentId": "root"},
                {"id": "n2", "name": "Text", "parentId": "panel"},
            ],
        }

        result = validate_pipeline(current, previous_memory=previous)

        self.assertFalse(result["pass"])
        self.assertIn("structure:blocked:move", result["structure_change_errors"])
        self.assertIn("structure:blocked:rename", result["structure_change_errors"])
        self.assertIn("structure:blocked:delete", result["structure_change_errors"])

    def test_restructure_blocked_by_default(self):
        previous = {"schemaVersion": "component@1.0.0", "nodes": [{"id": "n1", "name": "Board"}]}
        current = {
            "schemaVersion": "component@1.0.0",
            "nodes": [{"id": "n1", "name": "Board", "restructure": True}],
        }

        result = validate_pipeline(current, previous_memory=previous)

        self.assertFalse(result["pass"])
        self.assertIn("restructure", result["structure_change_types"])
        self.assertIn("structure:blocked:restructure", result["structure_change_errors"])

    def test_restructure_allowed_only_with_mode_and_confirmation(self):
        previous = {"schemaVersion": "component@1.0.0", "nodes": [{"id": "n1", "name": "Board"}]}
        current = {
            "schemaVersion": "component@1.0.0",
            "nodes": [{"id": "n1", "name": "Board", "restructure": True}],
        }

        result_without_confirmation = validate_pipeline(
            current,
            previous_memory=previous,
            restructure_mode=True,
            restructure_confirmed=False,
        )
        self.assertFalse(result_without_confirmation["pass"])
        self.assertIn("structure:blocked:restructure", result_without_confirmation["structure_change_errors"])

        result_with_confirmation = validate_pipeline(
            current,
            previous_memory=previous,
            restructure_mode=True,
            restructure_confirmed=True,
        )
        self.assertTrue(result_with_confirmation["pass"])
        self.assertEqual([], result_with_confirmation["structure_change_errors"])


if __name__ == "__main__":
    unittest.main()
