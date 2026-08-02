# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced `/transcript/assemble` endpoint to include metadata collection for chapters, outcomes, and action items.
- Updated tests in `tests/test_transcript_assembly_endpoint.py` to validate the inclusion of metadata in the response.
- Planned a new endpoint to process structured transcripts through Anthropic's API for generating TLDR and meeting outcomes.

### Changed
- Refactored the `assemble_transcript_endpoint` in `api/index.py` to integrate metadata extraction and return a comprehensive response.

### Fixed
- Improved error handling in the `/transcript/assemble` endpoint to manage invalid URLs and JSON parsing errors more effectively.

---

## [0.1.0] - YYYY-MM-DD
- Initial release with basic project setup and initial implementation of URL validation and JSON parsing.


