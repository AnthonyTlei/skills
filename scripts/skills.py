#!/usr/bin/env python3
"""Validate and link skills from this repository into an agent harness."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "skills.toml"
ALLOWED_CODEX_FRONTMATTER = {
    "allowed-tools",
    "description",
    "license",
    "metadata",
    "name",
}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class Skill:
    name: str
    harness: str
    version: str
    path: Path


def load_skills() -> list[Skill]:
    with MANIFEST_PATH.open("rb") as manifest_file:
        manifest = tomllib.load(manifest_file)

    if manifest.get("schema_version") != 1:
        raise ValueError("skills.toml must use schema_version = 1")

    skills: list[Skill] = []
    for item in manifest.get("skill", []):
        skills.append(
            Skill(
                name=item["name"],
                harness=item["harness"],
                version=item["version"],
                path=REPO_ROOT / item["path"],
            )
        )
    return skills


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")

    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("SKILL.md frontmatter is not closed") from error

    values: dict[str, str] = {}
    keys: list[str] = []
    for line in lines[1:end]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            raise ValueError(f"unsupported frontmatter line: {line}")
        key, value = match.groups()
        keys.append(key)
        values[key] = (value or "").strip().strip('"').strip("'")
    return values, keys


def validate_relative_links(skill_md: Path) -> list[str]:
    errors: list[str] = []
    text = skill_md.read_text(encoding="utf-8")
    for target in MARKDOWN_LINK_PATTERN.findall(text):
        clean_target = target.split("#", 1)[0]
        if not clean_target or "://" in clean_target or clean_target.startswith("mailto:"):
            continue
        if not (skill_md.parent / clean_target).exists():
            errors.append(f"missing linked file: {target}")
    return errors


def bundled_codex_validator() -> Path | None:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    candidate = codex_home / "skills/.system/skill-creator/scripts/quick_validate.py"
    return candidate if candidate.is_file() else None


def validate_skill(skill: Skill, official_validator: Path | None) -> list[str]:
    errors: list[str] = []
    try:
        relative_path = skill.path.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        return ["manifest path leaves the repository"]

    if not skill.path.is_dir():
        return [f"missing directory: {relative_path}"]
    if skill.path.name != skill.name:
        errors.append("directory name does not match manifest name")
    if not NAME_PATTERN.fullmatch(skill.name):
        errors.append("name must contain lowercase letters, digits, and hyphens only")
    if not VERSION_PATTERN.fullmatch(skill.version):
        errors.append("version must use MAJOR.MINOR.PATCH")

    skill_md = skill.path / "SKILL.md"
    if not skill_md.is_file():
        return errors + ["missing SKILL.md"]

    try:
        frontmatter, keys = parse_frontmatter(skill_md)
    except ValueError as error:
        return errors + [str(error)]

    if len(keys) != len(set(keys)):
        errors.append("frontmatter contains duplicate keys")
    if frontmatter.get("name") != skill.name:
        errors.append("frontmatter name does not match manifest name")
    if not frontmatter.get("description"):
        errors.append("frontmatter description is required")
    if skill.harness == "codex":
        unexpected = sorted(set(keys) - ALLOWED_CODEX_FRONTMATTER)
        if unexpected:
            errors.append(f"unsupported Codex frontmatter keys: {', '.join(unexpected)}")

    errors.extend(validate_relative_links(skill_md))

    if skill.harness == "codex" and official_validator:
        result = subprocess.run(
            [sys.executable, str(official_validator), str(skill.path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = (result.stdout + result.stderr).strip()
            errors.append(f"bundled Codex validator failed: {detail}")
    return errors


def validate_all(skills: list[Skill]) -> int:
    errors_found = False
    seen: set[tuple[str, str]] = set()
    official_validator = bundled_codex_validator()

    for skill in skills:
        identity = (skill.harness, skill.name)
        errors: list[str] = []
        if identity in seen:
            errors.append("duplicate harness and skill name in manifest")
        seen.add(identity)
        errors.extend(validate_skill(skill, official_validator))

        if errors:
            errors_found = True
            print(f"FAIL {skill.harness}/{skill.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {skill.harness}/{skill.name} {skill.version}")

    if not skills:
        print("FAIL manifest contains no skills")
        return 1
    if official_validator:
        print(f"Used bundled Codex validator: {official_validator}")
    else:
        print("Bundled Codex validator not found; repository checks only")
    return int(errors_found)


def path_exists(path: Path) -> bool:
    return os.path.lexists(path)


def default_target(harness: str, skills: list[Skill]) -> Path:
    if harness != "codex":
        raise ValueError(f"no default install directory is defined for {harness}")

    explicit = os.environ.get("CODEX_SKILLS_DIR")
    if explicit:
        return Path(explicit).expanduser()

    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"

    codex_dir = Path.home() / ".codex/skills"
    harness_names = [skill.name for skill in skills if skill.harness == harness]
    if any(path_exists(codex_dir / name) for name in harness_names):
        return codex_dir
    return Path.home() / ".agents/skills"


def skills_for_harness(skills: list[Skill], harness: str) -> list[Skill]:
    selected = [skill for skill in skills if skill.harness == harness]
    if not selected:
        raise ValueError(f"manifest contains no skills for harness: {harness}")
    return selected


def install(skills: list[Skill], harness: str, target: Path, dry_run: bool) -> int:
    selected = skills_for_harness(skills, harness)
    conflicts: list[Path] = []
    for skill in selected:
        destination = target / skill.name
        if path_exists(destination) and not destination.is_symlink():
            conflicts.append(destination)
    if conflicts:
        print("Refusing to replace non-symlink paths:", file=sys.stderr)
        for conflict in conflicts:
            print(f"  {conflict}", file=sys.stderr)
        return 1

    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    for skill in selected:
        source = skill.path.resolve()
        destination = target / skill.name
        if destination.is_symlink() and destination.resolve() == source:
            print(f"OK   {destination} -> {source}")
            continue
        print(f"LINK {destination} -> {source}")
        if not dry_run:
            if destination.is_symlink():
                destination.unlink()
            destination.symlink_to(source, target_is_directory=True)
    return 0


def status(skills: list[Skill], harness: str, target: Path) -> int:
    problems = False
    for skill in skills_for_harness(skills, harness):
        source = skill.path.resolve()
        destination = target / skill.name
        if destination.is_symlink() and destination.resolve() == source:
            print(f"LINKED   {skill.name} -> {source}")
        elif not path_exists(destination):
            problems = True
            print(f"MISSING  {skill.name}")
        elif destination.is_symlink():
            problems = True
            print(f"WRONG    {skill.name} -> {destination.resolve()}")
        else:
            problems = True
            print(f"CONFLICT {skill.name}: {destination}")
    return int(problems)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate", help="validate the manifest and every skill")

    for command in ("install", "status"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("harness", help="harness name from skills.toml")
        subparser.add_argument("--target", type=Path, help="override the install directory")
        if command == "install":
            subparser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        skills = load_skills()
        if args.command == "validate":
            return validate_all(skills)

        target = (args.target or default_target(args.harness, skills)).expanduser().resolve()
        if args.command == "install":
            if validate_all(skills):
                return 1
            return install(skills, args.harness, target, args.dry_run)
        return status(skills, args.harness, target)
    except (KeyError, OSError, ValueError, tomllib.TOMLDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
