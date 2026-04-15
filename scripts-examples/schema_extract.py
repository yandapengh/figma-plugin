"""Example: read from bridge and run schema-driven extractor/validator."""

from bridge_client import read
from memory_os.extractor import extract_by_schema
from memory_os.validation import validate_pipeline


if __name__ == "__main__":
    payload = read()
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    extracted = extract_by_schema(nodes)
    report = validate_pipeline(extracted.structured_memory, write_payload=extracted.structured_memory)

    print("schemaVersion:", extracted.structured_memory.get("schemaVersion"))
    print("validation:", report)
    print("hints:", extracted.validation_hints)
