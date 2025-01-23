# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Implemented `assemble_transcript` function in `utils/transcript_utils.py` to process JSON data and assemble transcripts with speaker information and timing.
- Added tests in `tests/test_transcript_assembly.py` to validate the functionality of `assemble_transcript`, including handling of empty data and structured output.
- Updated project plan in `docs/project_plan.md` to include steps for adding an endpoint for transcript assembly and collecting metadata.
- Adjusted `.gitignore` to remove unnecessary exclusions for documentation files.

### Changed
- Refined the logic in `assemble_transcript` to correctly map indices from `results` to `speakerRanges` and include `startMs` and `endMs` in the output.
- Updated test data and expected results in `tests/test_transcript_assembly.py` to align with the new functionality and JSON structure.

### Fixed
- Resolved issues with incorrect index mapping in `assemble_transcript` that caused errors during test execution.

---

## [0.1.0] - YYYY-MM-DD
- Initial release with basic project setup and initial implementation of URL validation and JSON parsing.


