#!/usr/bin/env python3
"""Validate and render project-owned feature maps without project dependencies."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SCHEMA_VERSION = 1
MAP_DIR = Path("docs/feature-map")
CONFIG_PATH = MAP_DIR / "config.json"
FEATURES_DIR = MAP_DIR / "features"
FLOWS_DIR = MAP_DIR / "flows"
GENERATED_DIR = MAP_DIR / "generated"
OVERVIEW_PATH = Path("FEATURE_MAP.md")

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PREFIX_RE = re.compile(r"^[A-Z][A-Z0-9]*$")
FEATURE_ID_RE = re.compile(r"^([A-Z][A-Z0-9]*)-[0-9]{3,}$")
FLOW_ID_RE = re.compile(r"^FLOW-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

LIFECYCLES = {"proposed", "active", "deprecated", "removed"}
IMPLEMENTATIONS = {"absent", "partial", "complete", "unknown"}
VERIFICATIONS = {"unverified", "code-traced", "test-verified", "runtime-verified"}
FLOW_TYPES = {"user", "operator", "system"}
COVERAGES = {"unknown", "partial", "complete-for-declared-scope"}

FEATURE_REQUIRED = (
    "schema_version",
    "id",
    "title",
    "domain",
    "capability",
    "summary",
    "actors",
    "surfaces",
    "lifecycle",
    "implementation",
    "verification",
    "entry_points",
    "depends_on",
    "code_refs",
    "test_refs",
    "spec_refs",
    "decision_refs",
)
FLOW_REQUIRED = (
    "schema_version",
    "id",
    "title",
    "type",
    "summary",
    "primary_actor",
    "supporting_actors",
    "lifecycle",
    "entry_points",
    "steps",
    "external_systems",
)
FEATURE_LIST_FIELDS = (
    "actors",
    "surfaces",
    "entry_points",
    "depends_on",
    "code_refs",
    "test_refs",
    "spec_refs",
    "decision_refs",
)
FLOW_LIST_FIELDS = ("supporting_actors", "entry_points", "steps", "external_systems")


@dataclass(frozen=True)
class Diagnostic:
    level: str
    path: Path
    message: str
    line: int | None = None

    def format(self, repo: Path) -> str:
        try:
            shown = self.path.relative_to(repo)
        except ValueError:
            shown = self.path
        location = f"{shown}:{self.line}" if self.line else str(shown)
        return f"{self.level.upper()} {location}: {self.message}"


@dataclass(frozen=True)
class Record:
    kind: str
    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def id(self) -> str:
        value = self.metadata.get("id")
        return value if isinstance(value, str) else ""


@dataclass
class ProjectMap:
    repo: Path
    config: dict[str, Any]
    features: list[Record]
    flows: list[Record]
    diagnostics: list[Diagnostic]


def error(path: Path, message: str, line: int | None = None) -> Diagnostic:
    return Diagnostic("error", path, message, line)


def warning(path: Path, message: str, line: int | None = None) -> Diagnostic:
    return Diagnostic("warning", path, message, line)


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    handle = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", dir=path.parent, delete=False
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_path, mode)
        os.replace(temp_path, path)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise


def json_object(path: Path) -> tuple[dict[str, Any], list[Diagnostic]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, [error(path, "file does not exist")]
    except OSError as exc:
        return {}, [error(path, f"cannot read file: {exc}")]
    except json.JSONDecodeError as exc:
        return {}, [error(path, f"invalid JSON: {exc.msg} at column {exc.colno}", exc.lineno)]
    if not isinstance(value, dict):
        return {}, [error(path, "top-level JSON value must be an object")]
    return value, []


def parse_record(path: Path, kind: str) -> tuple[Record | None, list[Diagnostic]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [error(path, f"cannot read file: {exc}")]
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None, [error(path, "record must start with a line containing only ---", 1)]
    try:
        closing = lines.index("---", 1)
    except ValueError:
        return None, [error(path, "JSON frontmatter is not closed with ---", 1)]
    raw = "\n".join(lines[1:closing])
    try:
        metadata = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, [
            error(path, f"invalid frontmatter JSON: {exc.msg} at column {exc.colno}", exc.lineno + 1)
        ]
    if not isinstance(metadata, dict):
        return None, [error(path, "frontmatter JSON must be an object", 2)]
    body = "\n".join(lines[closing + 1 :]).strip()
    return Record(kind, path, metadata, body), []


def string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value)


def validate_string(record: Record, field: str, diagnostics: list[Diagnostic]) -> None:
    if not isinstance(record.metadata.get(field), str) or not record.metadata[field].strip():
        diagnostics.append(error(record.path, f"{field} must be a non-empty string"))


def validate_list(record: Record, field: str, diagnostics: list[Diagnostic]) -> None:
    value = record.metadata.get(field)
    if not isinstance(value, list):
        diagnostics.append(error(record.path, f"{field} must be an array"))
        return
    if any(not isinstance(item, str) or not item for item in value):
        diagnostics.append(error(record.path, f"{field} must contain non-empty strings"))
    if len(value) != len(set(item for item in value if isinstance(item, str))):
        diagnostics.append(error(record.path, f"{field} contains duplicates"))


def safe_reference(repo: Path, record: Record, field: str, reference: str) -> Diagnostic | None:
    path_part = reference.split("#", 1)[0]
    if not path_part:
        return error(record.path, f"{field} contains an empty path: {reference!r}")
    pure = PurePosixPath(path_part)
    if pure.is_absolute() or ".." in pure.parts or "://" in path_part:
        return error(record.path, f"{field} must use a safe repository-relative path: {reference}")
    target = (repo / Path(*pure.parts)).resolve()
    try:
        target.relative_to(repo)
    except ValueError:
        return error(record.path, f"{field} leaves the repository: {reference}")
    if not target.is_file():
        return error(record.path, f"{field} references a missing file: {reference}")
    return None


def safe_output_path(repo: Path, relative: Path) -> Path:
    target = repo / relative
    try:
        target.parent.resolve().relative_to(repo)
    except ValueError as exc:
        raise ValueError(f"output parent leaves the repository: {relative}") from exc
    if os.path.lexists(target) and target.is_symlink():
        raise ValueError(f"refusing symlink output: {relative}")
    return target


def validate_config(repo: Path, config: dict[str, Any], diagnostics: list[Diagnostic]) -> None:
    path = repo / CONFIG_PATH
    if config.get("schema_version") != SCHEMA_VERSION:
        diagnostics.append(error(path, f"schema_version must be {SCHEMA_VERSION}"))

    project = config.get("project")
    if not isinstance(project, dict) or not isinstance(project.get("name"), str) or not project["name"].strip():
        diagnostics.append(error(path, "project.name must be a non-empty string"))
    elif not isinstance(project.get("summary", ""), str):
        diagnostics.append(error(path, "project.summary must be a string"))

    scope = config.get("scope")
    if not isinstance(scope, dict):
        diagnostics.append(error(path, "scope must be an object"))
    else:
        if not isinstance(scope.get("description"), str) or not scope["description"].strip():
            diagnostics.append(error(path, "scope.description must be a non-empty string"))
        if not string_list(scope.get("paths")):
            diagnostics.append(error(path, "scope.paths must contain repository-relative paths"))
        elif any(PurePosixPath(item).is_absolute() or ".." in PurePosixPath(item).parts for item in scope["paths"]):
            diagnostics.append(error(path, "scope.paths must remain inside the repository"))
        coverage = scope.get("coverage")
        if coverage not in COVERAGES:
            diagnostics.append(error(path, f"scope.coverage must be one of: {', '.join(sorted(COVERAGES))}"))
        elif coverage != "complete-for-declared-scope":
            diagnostics.append(warning(path, f"map coverage is {coverage!r}; generated views are not a complete inventory"))

    domains = config.get("domains")
    if not isinstance(domains, list):
        diagnostics.append(error(path, "domains must be an array"))
    else:
        seen_ids: set[str] = set()
        seen_prefixes: set[str] = set()
        for index, domain in enumerate(domains):
            label = f"domains[{index}]"
            if not isinstance(domain, dict):
                diagnostics.append(error(path, f"{label} must be an object"))
                continue
            domain_id = domain.get("id")
            prefix = domain.get("prefix")
            if not isinstance(domain_id, str) or not SLUG_RE.fullmatch(domain_id):
                diagnostics.append(error(path, f"{label}.id must be a lowercase slug"))
            elif domain_id in seen_ids:
                diagnostics.append(error(path, f"duplicate domain id: {domain_id}"))
            else:
                seen_ids.add(domain_id)
            if not isinstance(prefix, str) or not PREFIX_RE.fullmatch(prefix):
                diagnostics.append(error(path, f"{label}.prefix must contain uppercase letters and digits"))
            elif prefix in seen_prefixes:
                diagnostics.append(error(path, f"duplicate domain prefix: {prefix}"))
            else:
                seen_prefixes.add(prefix)
            if not isinstance(domain.get("title"), str) or not domain["title"].strip():
                diagnostics.append(error(path, f"{label}.title must be a non-empty string"))

    actors = config.get("actors")
    if not isinstance(actors, list):
        diagnostics.append(error(path, "actors must be an array"))
    else:
        seen_actors: set[str] = set()
        for index, actor in enumerate(actors):
            label = f"actors[{index}]"
            if not isinstance(actor, dict):
                diagnostics.append(error(path, f"{label} must be an object"))
                continue
            actor_id = actor.get("id")
            if not isinstance(actor_id, str) or not SLUG_RE.fullmatch(actor_id):
                diagnostics.append(error(path, f"{label}.id must be a lowercase slug"))
            elif actor_id in seen_actors:
                diagnostics.append(error(path, f"duplicate actor id: {actor_id}"))
            else:
                seen_actors.add(actor_id)
            for field in ("title", "type"):
                if not isinstance(actor.get(field), str) or not actor[field].strip():
                    diagnostics.append(error(path, f"{label}.{field} must be a non-empty string"))

    surfaces = config.get("surfaces")
    if not isinstance(surfaces, list) or any(
        not isinstance(item, str) or not SLUG_RE.fullmatch(item) for item in surfaces
    ):
        diagnostics.append(error(path, "surfaces must contain lowercase slugs"))
    elif len(surfaces) != len(set(surfaces)):
        diagnostics.append(error(path, "surfaces contains duplicates"))

    if config.get("dependency_cycle_policy", "warning") not in {"warning", "error"}:
        diagnostics.append(error(path, "dependency_cycle_policy must be warning or error"))
    retired = config.get("retired_ids", [])
    if not isinstance(retired, list) or any(
        not isinstance(item, str) or not FEATURE_ID_RE.fullmatch(item) for item in retired
    ):
        diagnostics.append(error(path, "retired_ids must contain feature IDs"))
    elif len(retired) != len(set(retired)):
        diagnostics.append(error(path, "retired_ids contains duplicates"))


def declared_values(config: dict[str, Any], key: str) -> set[str]:
    values = config.get(key, [])
    if not isinstance(values, list):
        return set()
    result: set[str] = set()
    for value in values:
        if isinstance(value, dict) and isinstance(value.get("id"), str):
            result.add(value["id"])
        elif isinstance(value, str):
            result.add(value)
    return result


def domain_prefixes(config: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    values = config.get("domains", [])
    if isinstance(values, list):
        for value in values:
            if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(value.get("prefix"), str):
                result[value["id"]] = value["prefix"]
    return result


def validate_feature(repo: Path, record: Record, config: dict[str, Any], diagnostics: list[Diagnostic]) -> None:
    metadata = record.metadata
    for field in FEATURE_REQUIRED:
        if field not in metadata:
            diagnostics.append(error(record.path, f"missing required field: {field}"))
    if metadata.get("schema_version") != SCHEMA_VERSION:
        diagnostics.append(error(record.path, f"schema_version must be {SCHEMA_VERSION}"))
    for field in ("id", "title", "domain", "capability", "summary", "lifecycle", "implementation", "verification"):
        if field in metadata:
            validate_string(record, field, diagnostics)
    for field in FEATURE_LIST_FIELDS:
        if field in metadata:
            validate_list(record, field, diagnostics)

    feature_id = metadata.get("id")
    match = FEATURE_ID_RE.fullmatch(feature_id) if isinstance(feature_id, str) else None
    if isinstance(feature_id, str) and not match:
        diagnostics.append(error(record.path, "id must match PREFIX-001 with at least three digits"))
    domain = metadata.get("domain")
    prefixes = domain_prefixes(config)
    if isinstance(domain, str):
        if domain not in prefixes:
            diagnostics.append(error(record.path, f"undeclared domain: {domain}"))
        elif match and match.group(1) != prefixes[domain]:
            diagnostics.append(error(record.path, f"id prefix {match.group(1)} does not match domain prefix {prefixes[domain]}"))
        try:
            folder_domain = record.path.relative_to(repo / FEATURES_DIR).parts[0]
            if folder_domain != domain:
                diagnostics.append(error(record.path, f"record is under domain folder {folder_domain!r}, not {domain!r}"))
        except (ValueError, IndexError):
            diagnostics.append(error(record.path, "feature record is outside the features directory"))

    actors = declared_values(config, "actors")
    for actor in metadata.get("actors", []) if isinstance(metadata.get("actors"), list) else []:
        if isinstance(actor, str) and actor not in actors:
            diagnostics.append(error(record.path, f"undeclared actor: {actor}"))
    surfaces = declared_values(config, "surfaces")
    for surface in metadata.get("surfaces", []) if isinstance(metadata.get("surfaces"), list) else []:
        if isinstance(surface, str) and surface not in surfaces:
            diagnostics.append(error(record.path, f"undeclared surface: {surface}"))

    for field, allowed in (
        ("lifecycle", LIFECYCLES),
        ("implementation", IMPLEMENTATIONS),
        ("verification", VERIFICATIONS),
    ):
        value = metadata.get(field)
        if isinstance(value, str) and value not in allowed:
            diagnostics.append(error(record.path, f"{field} must be one of: {', '.join(sorted(allowed))}"))

    for field in ("code_refs", "test_refs", "spec_refs", "decision_refs"):
        values = metadata.get(field)
        if isinstance(values, list):
            for reference in values:
                if isinstance(reference, str):
                    issue = safe_reference(repo, record, field, reference)
                    if issue:
                        diagnostics.append(issue)

    verification = metadata.get("verification")
    if verification == "code-traced" and not metadata.get("code_refs"):
        diagnostics.append(error(record.path, "code-traced verification requires code_refs"))
    if verification == "test-verified" and not metadata.get("test_refs"):
        diagnostics.append(error(record.path, "test-verified verification requires test_refs"))
    last_verified = metadata.get("last_verified")
    if verification == "unverified" and last_verified is not None:
        diagnostics.append(error(record.path, "unverified features must not contain last_verified"))
    elif verification in {"code-traced", "test-verified", "runtime-verified"} and not isinstance(last_verified, dict):
        diagnostics.append(error(record.path, f"{verification} verification requires last_verified"))
    elif last_verified is not None:
        if not isinstance(last_verified, dict):
            diagnostics.append(error(record.path, "last_verified must be an object"))
        else:
            date = last_verified.get("date")
            methods = last_verified.get("methods")
            if not isinstance(date, str) or not DATE_RE.fullmatch(date) or not string_list(methods):
                diagnostics.append(error(record.path, "last_verified requires a YYYY-MM-DD date and non-empty methods"))

    lifecycle = metadata.get("lifecycle")
    implementation = metadata.get("implementation")
    if lifecycle == "proposed" and not metadata.get("code_refs"):
        diagnostics.append(warning(record.path, "proposed feature has no code references"))
    if lifecycle == "active" and implementation in {"partial", "complete"} and verification == "unverified":
        diagnostics.append(warning(record.path, "implemented active feature is unverified"))
    if implementation == "complete" and not metadata.get("test_refs"):
        diagnostics.append(warning(record.path, "complete implementation has no test references"))
    if verification == "runtime-verified" and not any(
        metadata.get(field) for field in ("code_refs", "test_refs", "spec_refs", "decision_refs")
    ):
        diagnostics.append(warning(record.path, "runtime-verified feature has no repository evidence references"))
    if ({"integration", "webhook"} & set(metadata.get("surfaces", []))) and not any(
        metadata.get(field) for field in ("code_refs", "test_refs", "spec_refs", "decision_refs")
    ):
        diagnostics.append(warning(record.path, "external-facing feature has no repository evidence references"))


def validate_flow(record: Record, config: dict[str, Any], diagnostics: list[Diagnostic]) -> None:
    metadata = record.metadata
    for field in FLOW_REQUIRED:
        if field not in metadata:
            diagnostics.append(error(record.path, f"missing required field: {field}"))
    if metadata.get("schema_version") != SCHEMA_VERSION:
        diagnostics.append(error(record.path, f"schema_version must be {SCHEMA_VERSION}"))
    for field in ("id", "title", "type", "summary", "primary_actor", "lifecycle"):
        if field in metadata:
            validate_string(record, field, diagnostics)
    for field in FLOW_LIST_FIELDS:
        if field in metadata:
            value = metadata[field]
            if not isinstance(value, list):
                diagnostics.append(error(record.path, f"{field} must be an array"))
            elif field != "steps" and any(not isinstance(item, str) or not item for item in value):
                diagnostics.append(error(record.path, f"{field} must contain non-empty strings"))

    flow_id = metadata.get("id")
    if isinstance(flow_id, str) and not FLOW_ID_RE.fullmatch(flow_id):
        diagnostics.append(error(record.path, "id must start with FLOW- and use uppercase hyphenated words"))
    flow_type = metadata.get("type")
    if isinstance(flow_type, str) and flow_type not in FLOW_TYPES:
        diagnostics.append(error(record.path, f"type must be one of: {', '.join(sorted(FLOW_TYPES))}"))
    lifecycle = metadata.get("lifecycle")
    if isinstance(lifecycle, str) and lifecycle not in LIFECYCLES:
        diagnostics.append(error(record.path, f"lifecycle must be one of: {', '.join(sorted(LIFECYCLES))}"))

    actors = declared_values(config, "actors")
    primary = metadata.get("primary_actor")
    if isinstance(primary, str) and primary not in actors:
        diagnostics.append(error(record.path, f"undeclared primary actor: {primary}"))
    supporting = metadata.get("supporting_actors")
    if isinstance(supporting, list):
        if len(supporting) != len(set(item for item in supporting if isinstance(item, str))):
            diagnostics.append(error(record.path, "supporting_actors contains duplicates"))
        for actor in supporting:
            if isinstance(actor, str) and actor not in actors:
                diagnostics.append(error(record.path, f"undeclared supporting actor: {actor}"))
        if primary in supporting:
            diagnostics.append(error(record.path, "primary_actor must not also be a supporting actor"))

    steps = metadata.get("steps")
    if isinstance(steps, list):
        if not steps:
            diagnostics.append(error(record.path, "steps must not be empty"))
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                diagnostics.append(error(record.path, f"steps[{index}] must be an object"))
                continue
            if not isinstance(step.get("feature"), str) or not step["feature"]:
                diagnostics.append(error(record.path, f"steps[{index}].feature must be a feature ID"))
            if not isinstance(step.get("outcome"), str) or not step["outcome"].strip():
                diagnostics.append(error(record.path, f"steps[{index}].outcome must be a non-empty string"))


def dependency_cycles(features: dict[str, Record]) -> list[list[str]]:
    graph = {
        feature_id: sorted(
            dependency
            for dependency in record.metadata.get("depends_on", [])
            if isinstance(dependency, str) and dependency in features
        )
        for feature_id, record in features.items()
    }
    state: dict[str, int] = {}
    stack: list[str] = []
    found: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for dependency in graph[node]:
            if state.get(dependency, 0) == 0:
                visit(dependency)
            elif state.get(dependency) == 1:
                start = stack.index(dependency)
                cycle = stack[start:] + [dependency]
                rotations = [tuple(cycle[index:-1] + cycle[:index] + [cycle[index]]) for index in range(len(cycle) - 1)]
                found.add(min(rotations))
        stack.pop()
        state[node] = 2

    for feature_id in sorted(graph):
        if state.get(feature_id, 0) == 0:
            visit(feature_id)
    return [list(cycle) for cycle in sorted(found)]


def load_project(repo_arg: str | Path) -> ProjectMap:
    repo = Path(repo_arg).expanduser().resolve()
    diagnostics: list[Diagnostic] = []
    config, config_diagnostics = json_object(repo / CONFIG_PATH)
    diagnostics.extend(config_diagnostics)
    if not config_diagnostics:
        validate_config(repo, config, diagnostics)

    features: list[Record] = []
    flows: list[Record] = []
    for kind, directory, destination in (
        ("feature", repo / FEATURES_DIR, features),
        ("flow", repo / FLOWS_DIR, flows),
    ):
        if not directory.is_dir():
            diagnostics.append(error(directory, "directory does not exist"))
            continue
        for path in sorted(directory.rglob("*.md")):
            record, issues = parse_record(path, kind)
            diagnostics.extend(issues)
            if record:
                destination.append(record)

    if not config_diagnostics:
        for record in features:
            validate_feature(repo, record, config, diagnostics)
        for record in flows:
            validate_flow(record, config, diagnostics)

    records_by_id: dict[str, Record] = {}
    for record in features + flows:
        if not record.id:
            continue
        if record.id in records_by_id:
            diagnostics.append(
                error(record.path, f"duplicate id {record.id}; first declared in {records_by_id[record.id].path.relative_to(repo)}")
            )
        else:
            records_by_id[record.id] = record

    feature_by_id = {record.id: record for record in features if record.id}
    retired = config.get("retired_ids", []) if isinstance(config, dict) else []
    if isinstance(retired, list):
        for feature_id in sorted(set(feature_by_id) & set(item for item in retired if isinstance(item, str))):
            diagnostics.append(error(feature_by_id[feature_id].path, f"feature id is retired and may not be reused: {feature_id}"))

    for record in features:
        dependencies = record.metadata.get("depends_on", [])
        if not isinstance(dependencies, list):
            continue
        for dependency in dependencies:
            if not isinstance(dependency, str):
                continue
            if dependency == record.id:
                diagnostics.append(error(record.path, "feature may not depend on itself"))
            elif dependency not in feature_by_id:
                diagnostics.append(error(record.path, f"unknown dependency: {dependency}"))

    for record in flows:
        steps = record.metadata.get("steps", [])
        if not isinstance(steps, list):
            continue
        for index, step in enumerate(steps):
            if not isinstance(step, dict) or not isinstance(step.get("feature"), str):
                continue
            feature_id = step["feature"]
            feature = feature_by_id.get(feature_id)
            if not feature:
                diagnostics.append(error(record.path, f"steps[{index}] references unknown feature: {feature_id}"))
            elif record.metadata.get("lifecycle") == "active" and feature.metadata.get("lifecycle") == "removed":
                diagnostics.append(warning(record.path, f"active flow references removed feature: {feature_id}"))

    cycle_level = "error" if config.get("dependency_cycle_policy") == "error" else "warning"
    for cycle in dependency_cycles(feature_by_id):
        owner = feature_by_id[cycle[0]].path
        diagnostic = Diagnostic(cycle_level, owner, f"dependency cycle: {' -> '.join(cycle)}")
        diagnostics.append(diagnostic)

    diagnostics.sort(key=lambda item: (str(item.path), item.line or 0, item.level, item.message))
    return ProjectMap(repo, config, features, flows, diagnostics)


def table(headers: list[str], rows: Iterable[Iterable[str]]) -> str:
    def cell(value: str) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    rendered = [f"| {' | '.join(cell(value) for value in headers)} |"]
    rendered.append(f"| {' | '.join('---' for _ in headers)} |")
    materialized = [list(row) for row in rows]
    if materialized:
        rendered.extend(f"| {' | '.join(cell(value) for value in row)} |" for row in materialized)
    else:
        rendered.append(f"| {' | '.join('—' for _ in headers)} |")
    return "\n".join(rendered)


def generated_header(title: str) -> str:
    return f"# {title}\n\n> Generated by `$feature-map`. Edit canonical records under `docs/feature-map/`, then render again.\n"


def title_map(config: dict[str, Any], key: str) -> dict[str, str]:
    result: dict[str, str] = {}
    values = config.get(key, [])
    if isinstance(values, list):
        for value in values:
            if isinstance(value, dict) and isinstance(value.get("id"), str):
                result[value["id"]] = str(value.get("title", value["id"]))
    return result


def render_outputs(project: ProjectMap) -> dict[Path, str]:
    config = project.config
    features = sorted(project.features, key=lambda record: record.id)
    flows = sorted(project.flows, key=lambda record: record.id)
    domains = title_map(config, "domains")
    actors = title_map(config, "actors")
    feature_by_id = {record.id: record for record in features}
    dependents: dict[str, list[str]] = defaultdict(list)
    for record in features:
        for dependency in record.metadata.get("depends_on", []):
            if isinstance(dependency, str):
                dependents[dependency].append(record.id)

    project_data = config.get("project", {}) if isinstance(config.get("project"), dict) else {}
    scope = config.get("scope", {}) if isinstance(config.get("scope"), dict) else {}
    overview = [generated_header("Feature map")]
    overview.append(f"**Project:** {project_data.get('name', 'Unnamed project')}\n")
    if project_data.get("summary"):
        overview.append(str(project_data["summary"]) + "\n")
    overview.append(f"**Declared scope:** {scope.get('description', 'Not declared')}\n")
    overview.append(f"**Coverage:** `{scope.get('coverage', 'unknown')}`\n")
    overview.append(
        table(
            ["Canonical features", "Canonical flows", "Domains", "Actors"],
            [[str(len(features)), str(len(flows)), str(len(domains)), str(len(actors))]],
        )
        + "\n"
    )
    overview.append("## Views\n")
    for name, label in (
        ("by-domain.md", "By domain"),
        ("by-actor.md", "By actor"),
        ("flows.md", "Flows"),
        ("maturity.md", "Maturity"),
        ("dependencies.md", "Dependencies"),
        ("verification.md", "Verification"),
    ):
        overview.append(f"- [{label}](docs/feature-map/generated/{name})")
    overview.append("\nCoverage applies only to the declared scope. Generated views do not strengthen implementation or verification claims.\n")

    by_domain = [generated_header("Features by domain")]
    grouped_domains: dict[str, dict[str, list[Record]]] = defaultdict(lambda: defaultdict(list))
    for record in features:
        grouped_domains[str(record.metadata.get("domain", "unknown"))][str(record.metadata.get("capability", "Unclassified"))].append(record)
    for domain_id in sorted(grouped_domains, key=lambda value: (domains.get(value, value).lower(), value)):
        by_domain.append(f"## {domains.get(domain_id, domain_id)} (`{domain_id}`)\n")
        for capability in sorted(grouped_domains[domain_id], key=str.lower):
            by_domain.append(f"### {capability}\n")
            rows = []
            for record in sorted(grouped_domains[domain_id][capability], key=lambda item: item.id):
                relative = record.path.relative_to(project.repo).as_posix()
                rows.append([
                    f"[{record.id}](../features/{relative.split('/features/', 1)[1]})",
                    str(record.metadata.get("title", "")),
                    str(record.metadata.get("lifecycle", "")),
                    str(record.metadata.get("implementation", "")),
                ])
            by_domain.append(table(["ID", "Feature", "Lifecycle", "Implementation"], rows) + "\n")
    if not features:
        by_domain.append("No canonical features are recorded.\n")

    by_actor = [generated_header("Features by actor")]
    grouped_actors: dict[str, list[Record]] = defaultdict(list)
    for record in features:
        for actor in record.metadata.get("actors", []):
            if isinstance(actor, str):
                grouped_actors[actor].append(record)
    for actor_id in sorted(grouped_actors, key=lambda value: (actors.get(value, value).lower(), value)):
        by_actor.append(f"## {actors.get(actor_id, actor_id)} (`{actor_id}`)\n")
        by_actor.append(
            table(
                ["ID", "Feature", "Domain", "Surfaces"],
                [
                    [
                        record.id,
                        str(record.metadata.get("title", "")),
                        str(record.metadata.get("domain", "")),
                        ", ".join(record.metadata.get("surfaces", [])) or "—",
                    ]
                    for record in sorted(grouped_actors[actor_id], key=lambda item: item.id)
                ],
            )
            + "\n"
        )
    if not grouped_actors:
        by_actor.append("No actor-feature relationships are recorded.\n")

    flow_view = [generated_header("Flows")]
    for flow in flows:
        flow_view.append(f"## {flow.metadata.get('title', flow.id)} (`{flow.id}`)\n")
        flow_view.append(
            f"{flow.metadata.get('summary', '')}\n\nPrimary actor: `{flow.metadata.get('primary_actor', '')}` · Type: `{flow.metadata.get('type', '')}` · Lifecycle: `{flow.metadata.get('lifecycle', '')}`\n"
        )
        steps = []
        for index, step in enumerate(flow.metadata.get("steps", []), start=1):
            if not isinstance(step, dict):
                continue
            feature_id = str(step.get("feature", ""))
            feature_title = feature_by_id.get(feature_id).metadata.get("title", "") if feature_id in feature_by_id else ""
            steps.append([str(index), feature_id, str(feature_title), str(step.get("outcome", ""))])
        flow_view.append(table(["Step", "Feature", "Capability", "Outcome"], steps) + "\n")
    if not flows:
        flow_view.append("No canonical flows are recorded.\n")

    maturity = [generated_header("Feature maturity")]
    maturity.append(
        table(
            ["ID", "Feature", "Lifecycle", "Implementation", "Verification"],
            [
                [
                    record.id,
                    str(record.metadata.get("title", "")),
                    str(record.metadata.get("lifecycle", "")),
                    str(record.metadata.get("implementation", "")),
                    str(record.metadata.get("verification", "")),
                ]
                for record in features
            ],
        )
        + "\n"
    )

    dependencies = [generated_header("Feature dependencies")]
    dependencies.append(
        table(
            ["Feature", "Depends on", "Depended on by"],
            [
                [
                    record.id,
                    ", ".join(record.metadata.get("depends_on", [])) or "—",
                    ", ".join(sorted(dependents.get(record.id, []))) or "—",
                ]
                for record in features
            ],
        )
        + "\n"
    )

    verification = [generated_header("Verification evidence")]
    verification.append(
        table(
            ["ID", "Verification", "Code refs", "Test refs", "Last verified"],
            [
                [
                    record.id,
                    str(record.metadata.get("verification", "")),
                    str(len(record.metadata.get("code_refs", []))),
                    str(len(record.metadata.get("test_refs", []))),
                    str(record.metadata.get("last_verified", {}).get("date", "—"))
                    if isinstance(record.metadata.get("last_verified", {}), dict)
                    else "—",
                ]
                for record in features
            ],
        )
        + "\n"
    )

    return {
        OVERVIEW_PATH: "\n".join(overview).rstrip() + "\n",
        GENERATED_DIR / "by-domain.md": "\n".join(by_domain).rstrip() + "\n",
        GENERATED_DIR / "by-actor.md": "\n".join(by_actor).rstrip() + "\n",
        GENERATED_DIR / "flows.md": "\n".join(flow_view).rstrip() + "\n",
        GENERATED_DIR / "maturity.md": "\n".join(maturity).rstrip() + "\n",
        GENERATED_DIR / "dependencies.md": "\n".join(dependencies).rstrip() + "\n",
        GENERATED_DIR / "verification.md": "\n".join(verification).rstrip() + "\n",
    }


def print_diagnostics(project: ProjectMap, extra: list[Diagnostic] | None = None) -> tuple[int, int]:
    diagnostics = project.diagnostics + (extra or [])
    diagnostics.sort(key=lambda item: (str(item.path), item.line or 0, item.level, item.message))
    for diagnostic in diagnostics:
        print(diagnostic.format(project.repo))
    errors = sum(item.level == "error" for item in diagnostics)
    warnings = sum(item.level == "warning" for item in diagnostics)
    print(f"Summary: {errors} error(s), {warnings} warning(s)")
    return errors, warnings


def command_validate(args: argparse.Namespace) -> int:
    project = load_project(args.repo)
    errors, _ = print_diagnostics(project)
    return int(errors > 0)


def command_render(args: argparse.Namespace) -> int:
    project = load_project(args.repo)
    errors, _ = print_diagnostics(project)
    if errors:
        print("Render skipped because validation failed.", file=sys.stderr)
        return 1
    outputs = render_outputs(project)
    targets: dict[Path, Path] = {}
    for relative in outputs:
        try:
            targets[relative] = safe_output_path(project.repo, relative)
        except ValueError as exc:
            print(f"ERROR {relative}: {exc}", file=sys.stderr)
            return 1
    changed = 0
    for relative, content in outputs.items():
        target = targets[relative]
        previous = target.read_text(encoding="utf-8") if target.is_file() else None
        if previous != content:
            atomic_write(target, content)
            changed += 1
            print(f"WROTE {relative}")
    print(f"Render complete: {changed} file(s) changed")
    return 0


def command_check(args: argparse.Namespace) -> int:
    project = load_project(args.repo)
    stale: list[Diagnostic] = []
    if not any(item.level == "error" for item in project.diagnostics):
        for relative, expected in render_outputs(project).items():
            try:
                target = safe_output_path(project.repo, relative)
            except ValueError as exc:
                stale.append(error(project.repo / relative, str(exc)))
                continue
            if not target.is_file():
                stale.append(error(target, "generated file is missing; run render"))
            elif target.read_text(encoding="utf-8") != expected:
                stale.append(error(target, "generated file is stale; run render"))
    errors, _ = print_diagnostics(project, stale)
    return int(errors > 0)


def command_init(args: argparse.Namespace) -> int:
    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir():
        print(f"ERROR {repo}: repository directory does not exist", file=sys.stderr)
        return 1
    conflicts = [path for path in (repo / OVERVIEW_PATH, repo / MAP_DIR) if os.path.lexists(path)]
    if conflicts:
        print("Refusing to overwrite an existing feature map:", file=sys.stderr)
        for conflict in conflicts:
            print(f"  {conflict}", file=sys.stderr)
        return 1
    agents_path = repo / "AGENTS.md"
    if args.integrate_agents and os.path.lexists(agents_path) and (
        agents_path.is_symlink() or not agents_path.is_file()
    ):
        print(f"ERROR {agents_path}: refusing to replace a symlink or non-file AGENTS path", file=sys.stderr)
        return 1

    assets = Path(__file__).resolve().parent.parent / "assets"
    template = assets / "project-template"
    config, issues = json_object(template / "config.json")
    if issues:
        print(issues[0].format(repo), file=sys.stderr)
        return 1
    config["project"]["name"] = args.project_name
    config["project"]["summary"] = args.summary
    config["scope"]["description"] = args.scope
    config["scope"]["paths"] = args.scope_path or ["."]

    preflight: list[Diagnostic] = []
    validate_config(repo, config, preflight)
    preflight_errors = [item for item in preflight if item.level == "error"]
    if preflight_errors:
        for diagnostic in preflight_errors:
            print(diagnostic.format(repo), file=sys.stderr)
        return 1

    (repo / FEATURES_DIR).mkdir(parents=True)
    (repo / FLOWS_DIR).mkdir(parents=True)
    atomic_write(repo / FEATURES_DIR / ".gitkeep", "")
    atomic_write(repo / FLOWS_DIR / ".gitkeep", "")
    atomic_write(repo / CONFIG_PATH, json.dumps(config, indent=2, ensure_ascii=False) + "\n")
    for name in ("README.md", "glossary.md"):
        atomic_write(repo / MAP_DIR / name, (template / name).read_text(encoding="utf-8"))

    if args.integrate_agents:
        snippet = (assets / "AGENTS-feature-map-snippet.md").read_text(encoding="utf-8").strip()
        existing = agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
        if re.search(r"(?m)^## Feature map\s*$", existing):
            print("SKIP AGENTS.md already contains a Feature map section")
        else:
            combined = (existing.rstrip() + "\n\n" if existing.strip() else "") + snippet + "\n"
            atomic_write(agents_path, combined)
            print("WROTE AGENTS.md")

    project = load_project(repo)
    errors, _ = print_diagnostics(project)
    if errors:
        return 1
    for relative, content in render_outputs(project).items():
        atomic_write(safe_output_path(repo, relative), content)
        print(f"WROTE {relative}")
    print("Initialized an empty feature map with unknown coverage.")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subparsers = root.add_subparsers(dest="command", required=True)
    for name, handler in (
        ("validate", command_validate),
        ("render", command_render),
        ("check", command_check),
    ):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("--repo", default=".", help="project repository root")
        subparser.set_defaults(handler=handler)
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--repo", default=".", help="project repository root")
    init_parser.add_argument("--project-name", required=True)
    init_parser.add_argument("--summary", default="")
    init_parser.add_argument("--scope", required=True, help="bounded product scope")
    init_parser.add_argument("--scope-path", action="append", help="repository-relative path in scope")
    init_parser.add_argument("--integrate-agents", action="store_true", help="append optional AGENTS guidance")
    init_parser.set_defaults(handler=command_init)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
