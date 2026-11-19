import json
import tempfile
import unittest
from pathlib import Path

from docsync import SyncError, sync


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "sources").mkdir()
        (self.root / "docs").mkdir()
        self.source = self.root / "sources" / "billing-api.json"
        self.output = self.root / "docs" / "API.md"

    def tearDown(self):
        self.temp.cleanup()

    def write_source(self, data):
        self.source.write_text(json.dumps(data), encoding="utf-8")

    def test_happy_path(self):
        self.write_source({"endpoints": [{
            "method": "GET", "path": "/invoices", "summary": "List invoices",
            "auth": "OAuth", "owner": "Billing team"
        }]})
        sync(self.source, self.output, root=self.root)
        rendered = self.output.read_text(encoding="utf-8")
        for value in ("GET", "/invoices", "List invoices", "OAuth", "Billing team"):
            self.assertIn(value, rendered)

    def test_missing_values_are_not_found(self):
        self.write_source({"endpoints": [{"method": "GET", "owner": None}]})
        sync(self.source, self.output, root=self.root)
        rendered = self.output.read_text(encoding="utf-8")
        self.assertGreaterEqual(rendered.count("Not Found"), 4)

    def test_secret_values_are_not_rendered(self):
        self.write_source({"endpoints": [{
            "method": "GET", "path": "/x", "summary": "api_key=supersecret",
            "auth": "Bearer abc123", "owner": "Billing"
        }]})
        sync(self.source, self.output, root=self.root)
        rendered = self.output.read_text(encoding="utf-8")
        self.assertNotIn("supersecret", rendered)
        self.assertNotIn("abc123", rendered)
        self.assertIn("Not Found", rendered)

    def test_missing_source_does_not_write_output(self):
        self.output.write_text("keep", encoding="utf-8")
        with self.assertRaises(SyncError):
            sync(self.source, self.output, root=self.root)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "keep")

    def test_empty_source_does_not_write_output(self):
        self.source.write_text(" \n", encoding="utf-8")
        self.output.write_text("keep", encoding="utf-8")
        with self.assertRaises(SyncError):
            sync(self.source, self.output, root=self.root)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "keep")

    def test_bad_json_does_not_write_output(self):
        self.source.write_text("{bad", encoding="utf-8")
        self.output.write_text("keep", encoding="utf-8")
        with self.assertRaises(SyncError):
            sync(self.source, self.output, root=self.root)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "keep")

    def test_empty_endpoints_is_valid(self):
        self.write_source({"endpoints": []})
        sync(self.source, self.output, root=self.root)
        self.assertIn("No endpoints are defined", self.output.read_text(encoding="utf-8"))

    def test_path_escape_is_rejected_without_writing(self):
        self.write_source({"endpoints": []})
        escaped = self.root.parent / "outside.md"
        with self.assertRaises(SyncError):
            sync(self.source, escaped, root=self.root)
        self.assertFalse(escaped.exists())


if __name__ == "__main__":
    unittest.main()
