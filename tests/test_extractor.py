import unittest

from memory_os.extractor import extract_by_schema


class ExtractorTests(unittest.TestCase):
    def test_extract_uses_memory_node_schema_version(self):
        result = extract_by_schema([{"id": "n1", "type": "FRAME", "name": "Container"}])
        payload = result.structured_memory

        self.assertEqual("memory-node@1.0.0", payload["schemaVersion"])
        self.assertNotIn("schema_version", payload)


if __name__ == "__main__":
    unittest.main()
