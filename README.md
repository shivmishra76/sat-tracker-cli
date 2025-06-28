# 🛰️ Satellite Tracker CLI

A comprehensive command-line tool for tracking satellites in real-time. Get satellite positions, visibility information, orbital predictions, and beautiful visualizations - all from your terminal.

## ✨ Features

- **Real-time Satellite Tracking**: Track any satellite by name using live TLE data
- **Visibility Calculations**: Know when and where to look for satellites
- **Pass Predictions**: Get upcoming visible passes with precise timing
- **Interactive Visualizations**: Beautiful Earth map with satellite orbit and visibility zones
- **Multiple Output Formats**: Human-readable or JSON output for automation
- **Flexible Input**: Command-line arguments or interactive mode

## 🚀 Quick Start

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd sat_tracker_cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

**Track the International Space Station (ISS):**
```bash
python main.py ISS
```

**Track a satellite with custom ground station location:**
```bash
python main.py "HUBBLE SPACE TELESCOPE" --gs-lat 37.7749 --gs-lon -122.4194 --gs-alt 0.1
```

**Get JSON output for automation:**
```bash
python main.py ISS --json --hours 12 --min-elevation 10
```

**Interactive mode (no command line arguments):**
```bash
python main.py
```

## 📋 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `name` | Satellite name (partial matches allowed) | Interactive prompt |
| `--gs-lat` | Ground station latitude (degrees) | 40.0 |
| `--gs-lon` | Ground station longitude (degrees) | -88.0 |
| `--gs-alt` | Ground station altitude (km) | 0.2 |
| `--json` | Output in JSON format | False |
| `--hours` | Hours ahead for pass predictions | 24 |
| `--min-elevation` | Minimum elevation for visible passes (degrees) | 10 |

## 📊 Output Information

The tracker provides comprehensive information about the satellite:

### Position Data
- Current latitude, longitude, and altitude
- Velocity in km/s
- Timestamp (UTC)

### Visibility Information
- Azimuth and elevation from your location
- Range (distance) to satellite
- Whether currently visible above horizon

### Orbital Information
- Orbital period in minutes
- Predicted visible passes in the next 24 hours (or custom timeframe)
- Next pass details with precise timing

### Visual Map
- Interactive Earth map showing:
  - Satellite's current position
  - Orbital trajectory (1.5 hours)
  - Your ground station location
  - Visibility circle
  - Line of sight to satellite

## 🌍 Examples

### Track the ISS from New York
```bash
python main.py ISS --gs-lat 40.7128 --gs-lon -74.0060 --gs-alt 0.01
```

### Get Hubble passes for the next 48 hours
```bash
python main.py "HUBBLE" --hours 48 --min-elevation 15
```

### Export data for analysis
```bash
python main.py "STARLINK" --json > starlink_data.json
```

### Interactive mode for beginners
```bash
python main.py
# Follow the prompts to enter satellite name and location
```

## 🔧 Technical Details

### Data Sources
- **TLE Data**: Retrieved from Celestrak's satellite database
- **Orbital Calculations**: Uses SGP4 propagation model
- **Coordinate Transformations**: Precise geodetic calculations

### Key Libraries
- `sgp4`: Satellite position calculations
- `pymap3d`: Coordinate transformations
- `matplotlib`: Visualization and mapping
- `rich`: Beautiful terminal output
- `requests`: TLE data fetching

### File Structure
```
sat_tracker_cli/
├── main.py           # Main entry point
├── cli.py            # Command line interface
├── tle.py            # TLE data fetching
├── orbit.py          # Orbital calculations
├── visibility.py     # Visibility and pass predictions
├── plot_earth.py     # Visualization and mapping
├── output.py         # Output formatting
├── utils.py          # Utility functions
└── requirements.txt  # Dependencies
```

## 📋 Sample Output

### Human-Readable Format
```
🛰️ Satellite: ISS (ZARYA)
📍 Position: 42.1234°N, -71.5678°W, 408.2 km altitude
🚀 Velocity: 7.66 km/s
⏰ Time: 2025-06-28 15:30:00 UTC

🏠 Ground Station: 40.0000°N, -88.0000°W, 0.2 km
👁️ Visibility: Azimuth 125.4°, Elevation 45.2°, Range 856.3 km
✅ Currently visible above horizon

🌍 Orbital Period: 92.8 minutes

📅 Upcoming Passes (next 24 hours):
  🌟 Pass 1: Jun 28, 20:15 - 20:23 UTC (Max elevation: 67°)
  🌟 Pass 2: Jun 29, 05:42 - 05:48 UTC (Max elevation: 34°)
  ⏰ Next pass in: 4 hours 45 minutes
```

### JSON Format
```json
{
  "satellite": {
    "name": "ISS (ZARYA)",
    "position": {
      "latitude": 42.1234,
      "longitude": -71.5678,
      "altitude_km": 408.2,
      "velocity_km_s": 7.66
    },
    "timestamp": "2025-06-28T15:30:00Z"
  },
  "ground_station": {
    "latitude": 40.0,
    "longitude": -88.0,
    "altitude_km": 0.2
  },
  "visibility": {
    "azimuth_deg": 125.4,
    "elevation_deg": 45.2,
    "range_km": 856.3,
    "is_visible": true
  },
  "orbital_info": {
    "period_minutes": 92.8
  },
  "predictions": {
    "hours_ahead": 24,
    "min_elevation": 10,
    "passes": [
      {
        "start_time": "2025-06-28T20:15:00Z",
        "end_time": "2025-06-28T20:23:00Z",
        "max_elevation": 67,
        "duration_minutes": 8
      }
    ],
    "next_pass": {
      "start_time": "2025-06-28T20:15:00Z",
      "time_until": "4 hours 45 minutes"
    }
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Troubleshooting

### Common Issues

1. **"Satellite not found"**: Try using partial names or check the satellite name spelling
2. **No visible passes**: Try increasing the prediction timeframe with `--hours` or lowering `--min-elevation`
3. **Map not displaying**: Ensure matplotlib and basemap are properly installed

### Need Help?

- Check satellite names at [Celestrak](https://celestrak.com/NORAD/elements/)
- For coordinates, use [GPS Coordinates](https://www.gps-coordinates.net/)
- Report issues in the project repository

---

**Happy satellite tracking! 🛰️✨**