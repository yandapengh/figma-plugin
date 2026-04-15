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


if __name__ == "__main__":
    unittest.main()
