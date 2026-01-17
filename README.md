# Fox Energy Integration for Home Assistant

A custom Home Assistant integration for Fox Energy meters (3-phase and single-phase variants).

## Features

- **Automatic Discovery**: Automatically discovers Fox Energy devices on your network
- **Manual Configuration**: Supports manual IP address entry as fallback
- **3-Phase Support**: Full support for 3-phase meters with phase-specific and total measurements
- **Single-Phase Support**: Complete support for single-phase meters
- **Real-time Monitoring**: 
  - Energy consumption (kWh)
  - Active power (W)
  - Current (A)
  - Voltage (V)
  - Reactive power (VAr)
  - Power factor (cos φ)
  - Frequency (Hz)
- **Multiple Languages**: English and Polish support
- **Energy Dashboard Integration**: Compatible with Home Assistant's Energy Dashboard

## Installation

### Via HACS

1. Add this repository to HACS as a custom repository:
   - Go to HACS → Integrations → ⋯ → Custom repositories
   - URL: `https://github.com/corapoid/homeassistant-fox-energy-monitor`
   - Category: Integration

2. Install the Fox Energy integration from HACS

3. Restart Home Assistant

### Manual Installation

1. Clone/download this repository
2. Copy `custom_components/fox_energy` to your `<config_dir>/custom_components/` directory
3. Restart Home Assistant

## Configuration

### Automatic Discovery

1. Go to Settings → Integrations → Create Integration
2. Search for "Fox Energy"
3. The integration will automatically scan your network for Fox Energy devices
4. Select discovered devices to add, or manually enter an IP address

### Manual Configuration

1. Go to Settings → Integrations → Create Integration
2. Search for "Fox Energy"
3. Enter the IP address of your Fox Energy meter
4. (Optional) Enter a custom device name
5. Click Submit

## Supported Devices

- **Fox Energy 3** - 3-phase meter
- **Fox Energy 1** - Single-phase meter
- Any F&F Fox Energy meter compatible with REST API

## Usage

Once configured, the integration will create sensors for:

### 3-Phase Meters (19-24 sensors per device)
- Energy Import L1, L2, L3, and Total (kWh)
- Active Power L1, L2, L3, and Total (W)
- Current L1, L2, L3, and Total (A)
- Voltage L1, L2, L3 (V)
- Reactive Power L1, L2, L3 (VAr)
- Power Factor L1, L2, L3
- Frequency L1, L2, L3 (Hz)

### Single-Phase Meters (7 sensors per device)
- Energy Import (kWh)
- Active Power (W)
- Current (A)
- Voltage (V)
- Reactive Power (VAr)
- Power Factor
- Frequency (Hz)

## Energy Dashboard

To use Fox Energy in Home Assistant's Energy Dashboard:

1. Go to Settings → Integrations
2. Select Fox Energy device
3. Use "Energy Import Total" (for 3-phase) or "Energy Import" (for single-phase) as your main consumption

## Configuration Options

- **Update Interval**: Frequency of data updates (default: 5 seconds)
- **Connection Timeout**: Request timeout in seconds (default: 30 seconds)

## Troubleshooting

### Device not discovered
- Ensure your Fox Energy meter is connected to the network
- Verify the device is reachable on the same network as Home Assistant
- Check that the device's IP is within the scanned subnet (192.168.x.x)
- Try manual configuration with the device's IP address

### Cannot connect to device
- Verify the IP address is correct
- Ping the device to ensure network connectivity
- Check if the device's web interface is accessible via browser
- Verify firewall rules allow access to port 80

### Sensors showing unknown
- Check Home Assistant logs for errors
- Verify the device is responding to API requests
- Try restarting the integration

## API Reference

The integration uses Fox Energy REST API:

- `GET /0000/get_current_parameters` - Current voltage, current, power, frequency
- `GET /0000/get_total_energy` - Total energy consumption (import/export)

For more information, see: http://fox-updater.fhome.pl/rest_api_doc/

## License

MIT License - see LICENSE file for details

## Support

For issues, feature requests, or questions:
- GitHub Issues: https://github.com/corapoid/homeassistant-fox-energy-monitor/issues
- Forum: https://community.home-assistant.io/

## Changelog

### v0.1.0
- Initial release
- Support for 3-phase and single-phase Fox Energy meters
- Automatic network discovery
- Energy Dashboard integration
- English and Polish translations