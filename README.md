# Home Assistant Open Meteo Marine Component

A custom Home Assistant integration that provides marine weather data from the Open-Meteo Marine API.

## Features

This integration provides the following marine weather sensors:
- **Wave Height** (m) - Current wave height
- **Wave Direction** (°) - Direction waves are coming from
- **Wave Period** (s) - Time between successive wave peaks
- **Sea Surface Temperature** (°C) - Current sea temperature
- **Current Velocity** (m/s) - Ocean current speed
- **Current Direction** (°) - Ocean current direction

## Installation

### Manual Installation

1. Download this repository
2. Copy the `custom_components/openmeteo_marine` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Go to Configuration → Integrations
5. Click the "+" button and search for "Open Meteo Marine"
6. Follow the configuration steps

### HACS Installation

1. Add this repository to HACS as a custom repository
2. Install the integration through HACS
3. Restart Home Assistant
4. Configure the integration through the UI

## Configuration

The integration is configured through the Home Assistant UI:

1. Go to Configuration → Integrations
2. Click the "+" button
3. Search for "Open Meteo Marine"
4. Enter your coordinates:
   - **Latitude**: Latitude of the location (-90 to 90)
   - **Longitude**: Longitude of the location (-180 to 180)
   - **Update Interval**: How often to fetch data (15-1440 minutes, default: 60)

## API Information

This integration uses the [Open-Meteo Marine API](https://open-meteo.com/en/docs/marine-weather-api) which provides:
- Free access (no API key required)
- Global marine weather data
- Hourly updates
- Rate limiting: reasonable usage expected

## Entity Names

Entities will be created with the format:
- `sensor.open_meteo_marine_wave_height`
- `sensor.open_meteo_marine_wave_direction`
- `sensor.open_meteo_marine_wave_period`
- `sensor.open_meteo_marine_sea_surface_temperature`
- `sensor.open_meteo_marine_current_velocity`
- `sensor.open_meteo_marine_current_direction`

## Development

### Requirements

- Python 3.11+
- Home Assistant Core
- httpx >= 0.24.0

### Testing

```bash
# Install development dependencies
pip install -r requirements_dev.txt

# Run tests
python -m pytest

# Run linting
python -m pylint custom_components/openmeteo_marine/
python -m black custom_components/openmeteo_marine/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the linter and tests
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This integration is not affiliated with Open-Meteo. Marine weather data is provided by the Open-Meteo Marine API and should be used for informational purposes only. Always consult official marine weather services for critical decisions.