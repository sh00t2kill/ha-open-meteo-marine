<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Home Assistant Open Meteo Marine Component

This is a Home Assistant custom component for integrating Open Meteo marine weather data.

## Development Guidelines

- Follow Home Assistant integration development best practices
- Use async/await patterns for API calls
- Implement proper error handling and retries
- Follow Home Assistant coding standards
- Use type hints throughout the codebase
- Implement proper configuration validation
- Use Home Assistant's built-in HTTP session for API requests

## Component Structure

- `custom_components/openmeteo_marine/` - Main component directory
- `__init__.py` - Component initialization
- `sensor.py` - Sensor platform implementation  
- `manifest.json` - Component metadata
- `config_flow.py` - Configuration flow for UI setup
- `const.py` - Constants and configuration
- `coordinator.py` - Data update coordinator

## Marine Data Entities

The component should provide sensors for:
- Wave height (m)
- Wave direction (degrees)
- Wave period (s)
- Sea surface temperature (°C)
- Current velocity (m/s)
- Current direction (degrees)

## API Integration

- Use Open Meteo Marine API endpoints
- Implement proper rate limiting
- Handle API errors gracefully
- Cache responses appropriately