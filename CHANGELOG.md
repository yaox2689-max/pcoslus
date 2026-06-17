# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Nothing yet

## [0.2.0] - 2026-06-18

### Added
- Web UI frontend with Next.js + Tailwind CSS
- Decision recording in frontend (user can record final decision)
- Identity Experiment for validating Identity influence
- Decision Influence Rate metric
- Mismatch Analysis framework
- 7 Identity candidates discovered from real decisions

### Changed
- Improved similarity engine with direction-based comparison
- Enhanced prompt to include decision patterns
- Updated Identity with values inferred from actual decisions

### Fixed
- Similarity calculation bug (100% when recommendations differed)
- Value alignment now shows conflicts, not just alignment

## [0.1.0] - 2026-06-17

### Added
- Initial release
- Core decision engine with Fast/Slow thinking modes
- Identity Core with value conflict analysis
- World Model with belief system and confidence scores
- Multi-model support (DeepSeek, Kimi, Qwen, MIMO)
- Decision Journal with intermediate state tracking
- Runtime Trace logging
- Web Dashboard for visualization
- Decision Workflow CLI tool
- 27 benchmark scenarios
- 20 disagreement test scenarios
- Comprehensive design documentation

### Technical
- FastAPI backend with SQLite storage
- Next.js frontend with warm, friendly design
- Topic-based belief retrieval
- JSON-enforced LLM output
- Retry logic for API rate limits

## [0.0.1] - 2026-06-17

### Added
- Project initialization
- Design documents and architecture specs

[Unreleased]: https://github.com/yaox2689-max/pcos/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/yaox2689-max/pcos/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/yaox2689-max/pcos/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/yaox2689-max/pcos/releases/tag/v0.0.1
