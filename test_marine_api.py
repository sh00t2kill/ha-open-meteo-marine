#!/usr/bin/env python3
"""
Quick test script for Open Meteo Marine API integration.
This script tests the API functionality without requiring Home Assistant.
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Any, Dict


class TestOpenMeteoMarine:
    """Test class for Open Meteo Marine API."""
    
    def __init__(self, latitude: float, longitude: float):
        """Initialize with coordinates."""
        self.latitude = latitude
        self.longitude = longitude
        self.api_base_url = "https://marine-api.open-meteo.com/v1/marine"
        self._client = httpx.AsyncClient(timeout=30.0)

    async def fetch_marine_data(self) -> Dict[str, Any]:
        """Fetch marine data from Open Meteo API."""
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": [
                "wave_height",
                "wave_direction", 
                "wave_period",
                "sea_surface_temperature",
                "ocean_current_velocity",
                "ocean_current_direction"
            ],
            "timezone": "auto",
        }

        try:
            print(f"🌊 Fetching marine data for coordinates: {self.latitude}, {self.longitude}")
            print(f"📡 API URL: {self.api_base_url}")
            print(f"📋 Parameters: {json.dumps(params, indent=2)}")
            print("=" * 50)
            
            response = await self._client.get(self.api_base_url, params=params)
            response.raise_for_status()
            data = response.json()

            print(f"✅ API Response Status: {response.status_code}")
            print(f"📊 Raw API Response:")
            print(json.dumps(data, indent=2))
            print("=" * 50)

            if "current" not in data:
                raise ValueError("Invalid API response: missing current data")

            current_data = data["current"]
            
            # Parse the data into a more usable format (same as coordinator)
            parsed_data = {}
            
            if "wave_height" in current_data:
                parsed_data["wave_height"] = current_data["wave_height"]
            
            if "wave_direction" in current_data:
                parsed_data["wave_direction"] = current_data["wave_direction"]
                
            if "wave_period" in current_data:
                parsed_data["wave_period"] = current_data["wave_period"]
                
            if "sea_surface_temperature" in current_data:
                parsed_data["sea_surface_temperature"] = current_data["sea_surface_temperature"]
                
            if "ocean_current_velocity" in current_data:
                parsed_data["current_velocity"] = current_data["ocean_current_velocity"]
                
            if "ocean_current_direction" in current_data:
                parsed_data["current_direction"] = current_data["ocean_current_direction"]

            parsed_data["last_updated"] = datetime.now().isoformat()
            parsed_data["attribution"] = "Data provided by Open-Meteo Marine API"
            
            return parsed_data

        except httpx.RequestError as err:
            raise Exception(f"Error requesting data: {err}") from err
        except httpx.HTTPStatusError as err:
            raise Exception(f"HTTP error occurred: {err}") from err
        except Exception as err:
            raise Exception(f"Unexpected error: {err}") from err

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    def format_results(self, data: Dict[str, Any]) -> str:
        """Format the results for display."""
        result = "🌊 MARINE WEATHER DATA\n"
        result += "=" * 30 + "\n"
        
        sensors = {
            "wave_height": ("🌊 Wave Height", "m"),
            "wave_direction": ("🧭 Wave Direction", "°"),
            "wave_period": ("⏱️ Wave Period", "s"),
            "sea_surface_temperature": ("🌡️ Sea Surface Temperature", "°C"),
            "current_velocity": ("💨 Current Velocity", "m/s"),
            "current_direction": ("🧭 Current Direction", "°"),
        }
        
        for key, (name, unit) in sensors.items():
            value = data.get(key)
            if value is not None:
                result += f"{name}: {value} {unit}\n"
            else:
                result += f"{name}: No data\n"
        
        result += f"\n📅 Last Updated: {data.get('last_updated', 'Unknown')}\n"
        result += f"📍 Coordinates: {self.latitude}, {self.longitude}\n"
        
        return result


async def test_coordinates(latitude: float, longitude: float):
    """Test a specific set of coordinates."""
    print(f"\n🚀 Testing coordinates: {latitude}, {longitude}")
    print("=" * 60)
    
    tester = TestOpenMeteoMarine(latitude, longitude)
    
    try:
        data = await tester.fetch_marine_data()
        print("\n📋 PARSED DATA:")
        print(json.dumps(data, indent=2))
        print("\n" + tester.format_results(data))
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        await tester.close()


async def main():
    """Main test function."""
    print("🧪 Open Meteo Marine API Test Script")
    print("=" * 60)
    
    # Test locations with marine data
    test_locations = [
        (40.7128, -74.0060),    # New York Harbor
        (51.5074, -0.1278),     # London Thames
        (35.6762, 139.6503),    # Tokyo Bay
        (37.7749, -122.4194),   # San Francisco Bay
        (-33.8908, 151.2743),   # Bondi Beach, Sydney
    ]
    
    print(f"🌊 Testing {len(test_locations)} marine locations...")
    
    for lat, lon in test_locations:
        await test_coordinates(lat, lon)
        print("\n" + "="*60)
    
    # Interactive test
    print("\n🎯 INTERACTIVE TEST")
    print("Enter your own coordinates to test:")
    
    try:
        lat_input = input("Enter latitude (-90 to 90): ").strip()
        lon_input = input("Enter longitude (-180 to 180): ").strip()
        
        if lat_input and lon_input:
            lat = float(lat_input)
            lon = float(lon_input)
            
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                await test_coordinates(lat, lon)
            else:
                print("❌ Invalid coordinates! Latitude must be -90 to 90, longitude -180 to 180")
    
    except (ValueError, KeyboardInterrupt):
        print("\n👋 Skipping interactive test")
    
    print("\n✅ Test completed!")


if __name__ == "__main__":
    # Install required package if not available
    try:
        import httpx
    except ImportError:
        print("❌ httpx not found. Install it with: pip install httpx")
        exit(1)
    
    asyncio.run(main())