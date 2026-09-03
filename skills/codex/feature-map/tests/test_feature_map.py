from __future__ import annotations

import importlib.util
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent.parent
SCRIPT = PACKAGE / "scripts/feature_map.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures/valid-project"
SPEC = importlib.util.spec_from_file_location("feature_map", SCRIPT)
assert SPEC and SPEC.loader
FEATURE_MAP = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = FEATURE_MAP
SPEC.loader.exec_module(FEATURE_MAP)


class FeatureMapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "project"
        shutil.copytree(FIXTURE, self.repo)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments, "--repo", str(self.repo)],
            text=True,
            capture_output=True,
            check=False,
        )

    def project(self):
        return FEATURE_MAP.load_project(self.repo)

    def errors(self) -> list:
        return [item for item in self.project().diagnostics if item.level == "error"]

    def feature_path(self, feature_id: str) -> Path:
        return next((self.repo / "docs/feature-map/features").rglob(f"{feature_id}-*.md"))

    def rewrite_metadata(self, path: Path, change) -> None:
        record, issues = FEATURE_MAP.parse_record(path, "feature")
        self.assertFalse(issues)
        assert record
        metadata = dict(record.metadata)
        change(metadata)
        content = "---\n" + json.dumps(metadata, indent=2) + "\n---\n\n" + record.body + "\n"
        path.write_text(content, encoding="utf-8")

    def test_valid_fixture_discovers_records_and_accepts_symbol_fragments(self) -> None:
        project = self.project()
        self.assertEqual([], [item for item in project.diagnostics if item.level == "error"])
        self.assertEqual(["ACC-001", "PAY-001", "PAY-002"], sorted(item.id for item in project.features))
        self.assertEqual(["FLOW-CHECKOUT", "FLOW-PAYMENT-RETRY"], sorted(item.id for item in project.flows))

    def test_malformed_frontmatter_reports_exact_json_line(self) -> None:
        path = self.feature_path("ACC-001")
        text = path.read_text(encoding="utf-8").replace('"title": "Password sign-in",', '"title": ,')
        path.write_text(text, encoding="utf-8")
        _, issues = FEATURE_MAP.parse_record(path, "feature")
        self.assertEqual(1, len(issues))
        self.assertIn("invalid frontmatter JSON", issues[0].message)
        self.assertIsNotNone(issues[0].line)

    def test_duplicate_id_fails(self) -> None:
        source = self.feature_path("PAY-001")
        duplicate = source.with_name("PAY-099-duplicate.md")
        shutil.copy2(source, duplicate)
        self.assertTrue(any("duplicate id PAY-001" in item.message for item in self.errors()))

    def test_broken_dependency_and_flow_reference_fail(self) -> None:
        self.rewrite_metadata(self.feature_path("PAY-001"), lambda value: value.update(depends_on=["ACC-999"]))
        flow = self.repo / "docs/feature-map/flows/FLOW-CHECKOUT.md"
        record, issues = FEATURE_MAP.parse_record(flow, "flow")
        self.assertFalse(issues)
        assert record
        metadata = dict(record.metadata)
        metadata["steps"] = [{"feature": "PAY-999", "outcome": "Missing."}]
        flow.write_text("---\n" + json.dumps(metadata, indent=2) + "\n---\n", encoding="utf-8")
        messages = [item.message for item in self.errors()]
        self.assertIn("unknown dependency: ACC-999", messages)
        self.assertTrue(any("references unknown feature: PAY-999" in message for message in messages))

    def test_invalid_enum_fails(self) -> None:
        self.rewrite_metadata(self.feature_path("PAY-001"), lambda value: value.update(verification="probably"))
        self.assertTrue(any("verification must be one of" in item.message for item in self.errors()))

    def test_verification_claims_require_consistent_last_verified_evidence(self) -> None:
        path = self.feature_path("PAY-001")
        self.rewrite_metadata(path, lambda value: value.pop("last_verified"))
        self.assertTrue(any("test-verified verification requires last_verified" in item.message for item in self.errors()))
        self.rewrite_metadata(
            path,
            lambda value: value.update(
                verification="unverified",
                last_verified={"date": "2026-09-03", "methods": ["manual check"]},
            ),
        )
        self.assertTrue(any("unverified features must not contain last_verified" in item.message for item in self.errors()))

    def test_active_flow_using_removed_feature_warns(self) -> None:
        self.rewrite_metadata(self.feature_path("PAY-001"), lambda value: value.update(lifecycle="removed"))
        warnings = [item.message for item in self.project().diagnostics if item.level == "warning"]
        self.assertTrue(any("active flow references removed feature: PAY-001" in message for message in warnings))

    def test_render_is_deterministic_and_check_detects_staleness(self) -> None:
        first = self.run_cli("render")
        self.assertEqual(0, first.returncode, first.stdout + first.stderr)
        paths = [self.repo / path for path in FEATURE_MAP.render_outputs(self.project())]
        snapshot = {path: path.read_bytes() for path in paths}
        second = self.run_cli("render")
        self.assertEqual(0, second.returncode, second.stdout + second.stderr)
        self.assertIn("0 file(s) changed", second.stdout)
        self.assertEqual(snapshot, {path: path.read_bytes() for path in paths})
        self.assertEqual(0, self.run_cli("check").returncode)
        overview = self.repo / "FEATURE_MAP.md"
        overview.write_text(overview.read_text(encoding="utf-8") + "stale\n", encoding="utf-8")
        stale = self.run_cli("check")
        self.assertNotEqual(0, stale.returncode)
        self.assertIn("generated file is stale", stale.stdout)

    def test_render_preflights_every_output_before_writing(self) -> None:
        self.assertEqual(0, self.run_cli("render").returncode)
        overview = self.repo / "FEATURE_MAP.md"
        overview.write_text("sentinel\n", encoding="utf-8")
        generated = self.repo / "docs/feature-map/generated"
        shutil.rmtree(generated)
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        generated.symlink_to(outside, target_is_directory=True)
        result = self.run_cli("render")
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("sentinel\n", overview.read_text(encoding="utf-8"))
        self.assertEqual([], list(outside.iterdir()))

    def test_init_is_non_destructive_and_agents_integration_is_explicit(self) -> None:
        empty = Path(self.temp.name) / "empty"
        empty.mkdir()
        empty_repo = self.repo
        self.repo = empty
        created = self.run_cli(
            "init",
            "--project-name",
            "Fresh Project",
            "--scope",
            "Public API",
            "--scope-path",
            "src",
        )
        self.assertEqual(0, created.returncode, created.stdout + created.stderr)
        self.assertTrue((empty / "FEATURE_MAP.md").is_file())
        self.assertEqual(0o644, stat.S_IMODE((empty / "FEATURE_MAP.md").stat().st_mode))
        self.assertTrue((empty / "docs/feature-map/features/.gitkeep").is_file())
        self.assertTrue((empty / "docs/feature-map/flows/.gitkeep").is_file())
        self.assertFalse((empty / "AGENTS.md").exists())
        existing = self.run_cli(
            "init", "--project-name", "Overwrite", "--scope", "Everything"
        )
        self.assertNotEqual(0, existing.returncode)
        config = json.loads((empty / "docs/feature-map/config.json").read_text(encoding="utf-8"))
        self.assertEqual("Fresh Project", config["project"]["name"])
        self.repo = empty_repo

    def test_init_rejects_invalid_scope_before_writing(self) -> None:
        empty = Path(self.temp.name) / "invalid-scope"
        empty.mkdir()
        prior = self.repo
        self.repo = empty
        result = self.run_cli(
            "init",
            "--project-name",
            "Invalid Project",
            "--scope",
            "Unsafe scope",
            "--scope-path",
            "../outside",
        )
        self.assertNotEqual(0, result.returncode)
        self.assertFalse((empty / "docs/feature-map").exists())
        self.repo = prior

    def test_init_can_append_agents_guidance_once(self) -> None:
        empty = Path(self.temp.name) / "agents-project"
        empty.mkdir()
        (empty / "AGENTS.md").write_text("# Project rules\n", encoding="utf-8")
        prior = self.repo
        self.repo = empty
        created = self.run_cli(
            "init",
            "--project-name",
            "Agent Project",
            "--scope",
            "CLI",
            "--integrate-agents",
        )
        self.assertEqual(0, created.returncode, created.stdout + created.stderr)
        agents = (empty / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("# Project rules", agents)
        self.assertEqual(1, agents.count("## Feature map"))
        self.repo = prior

    def test_dependency_cycle_policy_changes_warning_to_error(self) -> None:
        self.rewrite_metadata(self.feature_path("ACC-001"), lambda value: value.update(depends_on=["PAY-001"]))
        project = self.project()
        self.assertTrue(any(item.level == "warning" and "dependency cycle" in item.message for item in project.diagnostics))
        config_path = self.repo / "docs/feature-map/config.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["dependency_cycle_policy"] = "error"
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        self.assertTrue(any(item.level == "error" and "dependency cycle" in item.message for item in self.project().diagnostics))


if __name__ == "__main__":
    unittest.main()
