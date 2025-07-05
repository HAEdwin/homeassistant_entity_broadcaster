# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-07-05

### Added
- Initial release of Entity Broadcaster integration
- Real-time UDP broadcasting of entity state changes
- Multi-entity selection support
- Configurable UDP port (1024-65535)
- Network-wide broadcasting capability
- JSON message format for structured data
- Options flow for post-installation configuration
- Config flow with multi-step setup (name, entities, network)
- Port availability validation
- Example UDP client for testing
- HACS compatibility

### Features
- **Config Flow**: Multi-step configuration process
  - Name configuration with uniqueness validation
  - Entity selection with searchable dropdown
  - Network configuration with port validation
- **Broadcasting**: Automatic UDP broadcasts on entity state changes
- **Options Flow**: Modify settings after initial setup
- **Error Handling**: Comprehensive validation and error messages
- **Documentation**: Complete README with examples and use cases

[Unreleased]: https://github.com/HAEdwin/entity_broadcaster/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/HAEdwin/entity_broadcaster/releases/tag/v1.0.0
