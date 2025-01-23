# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Implemented `/transcript/assemble` endpoint in `api/index.py` to process URLs, fetch JSON data, and return structured transcripts.
- Added tests in `tests/test_transcript_assembly_endpoint.py` to validate the functionality of the `/transcript/assemble` endpoint, including handling of valid and invalid URLs.
- Updated project plan in `docs/project_plan.md` to reflect the completion of Step 7 and outline future steps.

### Changed
- Refactored URL validation and JSON fetching logic into a shared function `validate_and_fetch_url` in `api/index.py`.
- Adjusted import paths in `api/index.py` to ensure correct module loading.

### Fixed
- Resolved issues with incorrect module imports that caused test failures.

---

## [0.1.0] - YYYY-MM-DD
- Initial release with basic project setup and initial implementation of URL validation and JSON parsing.


