# Changelog

This file records user-visible changes to the maintained skill catalog. The format follows Keep a Changelog, and versions follow Semantic Versioning.

## [Unreleased]

## [0.7.0] - 2026-09-03

### Added

- Added the original `right-size-tests` Codex skill for choosing proportionate automated and manual verification.
- Added explicit limits on duplicate coverage, full-suite reruns, timeout retries, assertion weakening, and premature automation of exploratory work.
- Documented the testing guidance and Codex behavior reports used to shape the policy.

## [0.6.0] - 2026-09-03

### Added

- Added the original `feature-map` Codex skill for project-owned capability, actor, flow, dependency, lifecycle, implementation, and verification maps.
- Added a standard-library CLI for non-destructive initialization, structural validation, deterministic rendering, and generated-output freshness checks.
- Added project templates, optional AGENTS guidance, reference documentation, realistic fixtures, and regression tests.

### Changed

- Documented the provenance and license boundary for original skill packages alongside upstream adaptations.

## [0.5.0] - 2026-09-03

### Added

- Added a root MIT license, third-party notices, and package-level license files for every adapted skill.
- Recorded the two upstream sources, authors, pinned revisions, file hashes, and adaptation boundaries.
- Added a public-facing catalog, installation guide, credits, and license summary to the README.

### Changed

- Renamed the catalog from `anthony-skills` to `agent-skills`.
- Added common secret-bearing local file patterns to `.gitignore`.

### Security

- Pinned both GitHub Actions dependencies to reviewed commit SHAs.

## [0.4.0] - 2026-09-03

### Changed

- Made Linear Free the hard compatibility target for every Linear-capable skill.
- Added fail-closed Free-plan, quota, billing, trial, and AI-credit guards to `to-tickets` and `to-spec`.
- Required local fallback when a Linear capability is paid, unavailable, or unclear.

## [0.3.0] - 2026-09-03

### Added

- Added an adapted `to-spec` skill from Matt Pocock's MIT-licensed skills repository.
- Added local specification publishing under `docs/specs/` with a review gate, evidence boundaries, stable requirement identifiers, and a verification matrix.
- Added conditional Linear project-document publishing with duplicate detection and read-back verification.

## [0.2.0] - 2026-09-03

### Changed

- Made project-local Markdown tickets the default output for `to-tickets`.
- Limited Linear publication to repositories with an unambiguous existing Linear project association.
- Standardized local ticket sets under `docs/tickets/` with a batch index, stable ticket identifiers, explicit dependencies, acceptance criteria, and verification instructions.

## [0.1.0] - 2026-09-03

### Added

- Imported the initial Codex catalog: `blast-radius`, `bro`, `how`, `teach`, `technical-writing`, `to-tickets`, `unslop`, and `why`.
- Added a harness-aware manifest, validator, safe symlink installer, status check, and CI validation.
- Added architecture, maintenance, and provenance documentation.

### Fixed

- Replaced the unsupported `disable-model-invocation` field in `unslop` with valid Codex metadata while keeping implicit invocation enabled.
