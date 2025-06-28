# Satellite Tracker - Enhanced Features Summary

## 🚀 What We've Added

### 1. **Organized Code Structure**
- **`main.py`**: Simplified main entry point 
- **`visibility.py`**: Visibility calculations and pass predictions
- **`output.py`**: Output formatting (JSON and human-readable)
- **`cli.py`**: Command line argument parsing
- **`plot_earth.py`**: Enhanced visualization with orbit and visibility

### 2. **Enhanced Calculations & Predictions**
- **Orbital Period Calculation**: Shows how long one orbit takes
- **Pass Predictions**: Predicts when satellite will be visible from ground station
- **Next Pass Information**: Shows time until next visible pass
- **Visibility Range**: Calculates azimuth, elevation, and range

### 3. **JSON Output Support** 
```bash
python main.py ISS --json --hours 6
```
- Computer-friendly structured output
- Includes all satellite data, predictions, and metadata
- Perfect for automation and integration with other tools

### 4. **Enhanced Interactive Map Visualization**
- **Satellite Orbit Path**: Shows the satellite's trajectory over 1.5 hours
- **Visibility Circle**: Shows the area where satellite can be seen above minimum elevation
- **Line of Sight**: Direct line from ground station to satellite
- **Enhanced Styling**: Better colors, grid lines, and labels

### 5. **Flexible Command Line Options**
```bash
# Basic usage
python main.py ISS

# With custom settings
python main.py ISS --gs-lat 37.7749 --gs-lon -122.4194 --hours 12 --min-elevation 5

# Control visualization
python main.py ISS --no-orbit          # Hide orbit
python main.py ISS --no-visibility     # Hide visibility circle
python main.py ISS --no-plot          # Skip map entirely

# JSON output
python main.py ISS --json
```

### 6. **Prediction Features**
- Predicts satellite passes up to any number of hours ahead
- Configurable minimum elevation threshold
- Shows pass duration, maximum elevation, and timing
- Calculates time remaining until next pass

## 🎯 Example Outputs

### Human-Readable Output:
```
Latitude:  -21.5368°
Longitude: -108.3982°
Altitude:  421.94 km
Velocity:  7.66 km/s
Orbital Period: 92.9 minutes
Azimuth:   201.18°
Elevation: -29.27°
Range:     6998.11 km

Pass Predictions (next 24 hours, min elevation 10.0°):
Total passes: 3

Pass 1:
  Start:    2025-06-29 06:16:49 UTC
  End:      2025-06-29 06:21:28 UTC
  Duration: 4.6 minutes
  Max elevation: 57.63° at 06:18:22 UTC

Next pass in 791.1 minutes!
```

### JSON Output:
```json
{
  "timestamp": "2025-06-28T18:29:21.343186+00:00Z",
  "satellite": {
    "name": "ISS",
    "position": {
      "latitude": -1.15186,
      "longitude": -123.866105,
      "altitude_km": 417.58,
      "velocity_kms": 7.66
    },
    "orbital_period_minutes": 92.88
  },
  "predictions": {
    "prediction_period_hours": 6,
    "minimum_elevation_degrees": 10.0,
    "total_passes": 0,
    "passes": [],
    "next_pass": null
  }
}
```

## 🗺️ Enhanced Map Features
The satellite tracking map now includes:
- **Blue orbit line**: Shows satellite's path over 1.5 hours
- **Green dashed circle**: Visibility range from ground station
- **Red line**: Direct line of sight to satellite
- **Grid lines**: For better coordinate reference
- **Multiple markers**: Satellite (red circle) and ground station (green square)

Perfect for both manual analysis and automated satellite tracking workflows! 🛰️
