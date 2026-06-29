#!/usr/bin/env python3
"""Regression tests for spec-parse.py."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = SCRIPT_DIR / "fixtures"


def load_spec_parse():
    module_name = "spec_parse"
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_DIR / "spec-parse.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load spec-parse.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


spec_parse = load_spec_parse()


class SpecParseTests(unittest.TestCase):
    def parse_fixture(self, name: str):
        path = FIXTURES_DIR / name
        return spec_parse.parse_spec(path)

    def requirement_titles(self, result) -> list[str]:
        return [req.title for req in result.requirements]

    def requirement_types(self, result) -> list[str]:
        return [req.type for req in result.requirements]

    def test_acceptance_section_bullets_are_functional(self):
        result = self.parse_fixture("acceptance_section.md")
        export_req = next(req for req in result.requirements if "export" in req.title.lower())
        duplicate_req = next(req for req in result.requirements if "duplicate" in req.title.lower())

        self.assertEqual(export_req.type, "functional")
        self.assertEqual(duplicate_req.type, "functional")
        self.assertEqual(export_req.group, "Feature / Acceptance Criteria")

    def test_implementation_notes_bullets_are_ignored(self):
        result = self.parse_fixture("acceptance_section.md")
        titles = self.requirement_titles(result)
        self.assertNotIn("Use pandas for export formatting", titles)

    def test_non_goal_section_bullets_are_non_goal(self):
        result = self.parse_fixture("non_goal_section.md")
        social = next(req for req in result.requirements if "Social login" in req.title)
        blockchain = next(req for req in result.requirements if "Blockchain" in req.title)

        self.assertEqual(social.type, "non_goal")
        self.assertEqual(blockchain.type, "non_goal")

    def test_narrative_requirement_in_normal_section(self):
        result = self.parse_fixture("non_goal_section.md")
        auth_req = next(req for req in result.requirements if "duplicate invitations" in req.title)
        self.assertEqual(auth_req.type, "functional")
        self.assertEqual(auth_req.title, "The system must block duplicate invitations.")

    def test_willow_false_positive_is_not_extracted(self):
        result = self.parse_fixture("false_positive_willow.md")
        titles = self.requirement_titles(result)
        self.assertEqual(titles, ["The unsupported export path should be removed before release."])

    def test_compound_narrative_splits_into_atomic_requirements(self):
        result = self.parse_fixture("compound_narrative.md")
        titles = self.requirement_titles(result)
        self.assertEqual(len(titles), 2)
        self.assertIn("The API must reject invalid tokens", titles)
        self.assertIn("must log all failures.", titles)

    def test_checklist_items_stay_atomic(self):
        result = self.parse_fixture("checklist_atomic.md")
        titles = self.requirement_titles(result)
        self.assertEqual(len(titles), 2)
        self.assertIn(
            "Read and normalize the package purpose, audience, and trigger modes.",
            titles,
        )
        self.assertIn(
            "Capture packaging gaps, ambiguities, and release risks for v0.1.0.",
            titles,
        )

    def test_acceptance_signals_are_cue_based_only(self):
        result = self.parse_fixture("acceptance_section.md")
        duplicate_req = next(req for req in result.requirements if "duplicate" in req.title.lower())
        export_req = next(req for req in result.requirements if "export" in req.title.lower())

        self.assertEqual(duplicate_req.acceptance_signals, ["duplicate case handled"])
        self.assertEqual(export_req.acceptance_signals, ["export path implemented"])
        for req in result.requirements:
            for signal in req.acceptance_signals:
                self.assertNotEqual(signal, req.source_excerpt)

    def test_json_envelope_shape(self):
        result = self.parse_fixture("checklist_atomic.md")
        payload = json.loads(spec_parse.to_json(result))

        self.assertEqual(set(payload), {"source", "parsed_at", "groups", "requirements"})
        self.assertIsInstance(payload["groups"], list)
        self.assertIsInstance(payload["requirements"], list)

        requirement = payload["requirements"][0]
        self.assertEqual(
            set(requirement),
            {
                "id",
                "title",
                "group",
                "source_excerpt",
                "acceptance_signals",
                "priority",
                "type",
            },
        )

    def test_cli_missing_file_exits_nonzero(self):
        exit_code = spec_parse.main(["/tmp/does-not-exist-spec-parse.md"])
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()