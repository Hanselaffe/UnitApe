from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path

import unitape_core as unitape


class UnitApeTests(unittest.TestCase):
    def test_parse_classes_without_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.py"
            source.write_text(
                "class Example:\n    def run(self):\n        return 1\n",
                encoding="utf-8",
            )
            classes = unitape.parse_classes(source)
            self.assertEqual([node.name for node in classes], ["Example"])

    def test_parse_classes_accepts_utf8_bom(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample_bom.py"
            source.write_bytes(
                b"\xef\xbb\xbfclass Example:\n    def run(self):\n        return 1\n"
            )
            classes = unitape.parse_classes(source)
            self.assertEqual([node.name for node in classes], ["Example"])

    def test_public_methods_excludes_private(self) -> None:
        node = ast.parse(
            "class Example:\n"
            "    def visible(self): pass\n"
            "    def _hidden(self): pass\n"
        ).body[0]
        self.assertIsInstance(node, ast.ClassDef)
        self.assertEqual(unitape.public_methods(node), ["visible"])

    def test_rendered_skeleton_uses_real_newlines_and_skips(self) -> None:
        node = ast.parse("class Example:\n    def run(self): pass\n").body[0]
        self.assertIsInstance(node, ast.ClassDef)
        rendered = unitape.render_test_skeleton(Path("sample.py"), node)
        self.assertIn("\nimport unittest\n", rendered)
        self.assertIn('@unittest.skip("TODO: define expected behavior for run")', rendered)
        self.assertNotIn("assertTrue(True)", rendered)
        compile(rendered, "generated_test.py", "exec")

    def test_generate_tests_refuses_overwrite_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "sample.py"
            output = root / "tests"
            source.write_text("class Example:\n    def run(self): pass\n", encoding="utf-8")

            first = unitape.generate_tests(source, output)
            self.assertEqual(len(first), 1)
            with self.assertRaises(FileExistsError):
                unitape.generate_tests(source, output)

    def test_generate_tests_can_overwrite_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "sample.py"
            output = root / "tests"
            source.write_text("class Example:\n    def run(self): pass\n", encoding="utf-8")
            unitape.generate_tests(source, output)
            second = unitape.generate_tests(source, output, overwrite=True)
            self.assertEqual(len(second), 1)


if __name__ == "__main__":
    unittest.main()
