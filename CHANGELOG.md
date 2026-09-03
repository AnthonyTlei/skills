# Changelog

This file records user-visible changes to the maintained skill catalog. The format follows Keep a Changelog, and versions follow Semantic Versioning.

## [Unreleased]

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
