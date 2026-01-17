# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-01-17

### Added
- Initial release of Fox Energy integration
- Support for 3-phase Fox Energy meters with individual and total measurements
- Support for single-phase Fox Energy meters
- Automatic network discovery of Fox Energy devices
- Manual IP address configuration
- All available sensor types:
  - Energy consumption (kWh)
  - Active power (W)
  - Current (A)
  - Voltage (V)
  - Reactive power (VAr)
  - Power factor (cos φ)
  - Frequency (Hz)
- Configurable update interval (default: 5 seconds)
- Configurable connection timeout (default: 30 seconds)
- Energy Dashboard integration
- English and Polish translations (via strings.json)
- Comprehensive error handling and logging
- Retry logic for connection failures

### Features
- Multi-language support (English, Polish)
- Config flow with automatic discovery
- Options flow for runtime configuration changes
- Device grouping with proper device info
- Sensor naming with entity names
- Full state class support (measurement, total_increasing)

### Technical
- Async/await implementation for non-blocking operations
- DataUpdateCoordinator for efficient data fetching
- Type hints throughout codebase
- Modular architecture for easy maintenance

### Documentation
- Comprehensive README with setup and troubleshooting guides
- API reference information
- Support links and issue tracking

## Future

### Planned Features
- Web UI for easy configuration
- Statistics export
- Historical data tracking
- Alerts and notifications
- Custom automations support
- Integration with other smart home systems
- Mobile app support
- Performance analytics
