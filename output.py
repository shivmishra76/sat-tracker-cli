# output.py
"""
Output formatting and display utilities for satellite tracker.
Handles both human-readable and JSON output formats.
"""

import json
from datetime import datetime, timezone
from rich import print


def get_input_or_default(prompt, default):
    """
    Get user input with a default value fallback.
    
    Args:
        prompt: Input prompt text
        default: Default value if no input provided
    
    Returns:
        float: User input or default value
    """
    try:
        value = input(f"{prompt} [{default}]: ").strip()
        return float(value) if value else default
    except ValueError:
        print("[red]Invalid input. Using default.[/red]")
        return default


def format_satellite_data(sat_name, pos, gs_lat, gs_lon, gs_alt, az, el, rng, 
                         orbital_period_minutes, passes, next_pass_info, 
                         hours_ahead, min_elevation):
    """
    Format satellite tracking data into a structured dictionary.
    
    Args:
        sat_name: Satellite name
        pos: Position dictionary from orbit module
        gs_lat, gs_lon, gs_alt: Ground station coordinates
        az, el, rng: Visibility data (azimuth, elevation, range)
        orbital_period_minutes: Orbital period in minutes
        passes: List of predicted passes
        next_pass_info: Next pass information
        hours_ahead: Prediction window in hours
        min_elevation: Minimum elevation threshold
    
    Returns:
        dict: Structured satellite data
    """
    return {
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "satellite": {
            "name": sat_name,
            "position": {
                "latitude": round(pos['lat'], 6),
                "longitude": round(pos['lon'], 6),
                "altitude_km": round(pos['alt_km'], 2),
                "velocity_kms": round(pos['velocity_kms'], 2)
            },
            "orbital_period_minutes": round(orbital_period_minutes, 2)
        },
        "ground_station": {
            "latitude": gs_lat,
            "longitude": gs_lon,
            "altitude_km": gs_alt
        },
        "visibility": {
            "azimuth_degrees": round(float(az), 2),
            "elevation_degrees": round(float(el), 2),
            "range_km": round(float(rng) / 1000, 2),
            "is_visible": bool(el > 0)
        },
        "predictions": {
            "prediction_period_hours": hours_ahead,
            "minimum_elevation_degrees": min_elevation,
            "total_passes": len(passes),
            "passes": passes,
            "next_pass": next_pass_info
        }
    }


def output_json(data):
    """
    Output data in JSON format.
    
    Args:
        data: Dictionary to output as JSON
    """
    print(json.dumps(data, indent=2))


def output_human_readable(data, plot_created=False):
    """
    Output data in human-readable format with rich formatting.
    
    Args:
        data: Formatted satellite data dictionary
        plot_created: Whether a plot was created (default: False)
    """
    sat_data = data["satellite"]
    vis_data = data["visibility"]
    pred_data = data["predictions"]
    
    # Satellite position
    print(f"Latitude:  [cyan]{sat_data['position']['latitude']:.4f}°[/cyan]")
    print(f"Longitude: [cyan]{sat_data['position']['longitude']:.4f}°[/cyan]")
    print(f"Altitude:  [cyan]{sat_data['position']['altitude_km']:.2f} km[/cyan]")
    print(f"Velocity:  [cyan]{sat_data['position']['velocity_kms']:.2f} km/s[/cyan]")
    print(f"Orbital Period: [cyan]{sat_data['orbital_period_minutes']:.1f} minutes[/cyan]")
    
    if plot_created:
        print("Satellite position map saved as [bold]sat_position.png[/bold]")
    
    # Visibility
    print(f"Azimuth:   [yellow]{vis_data['azimuth_degrees']:.2f}°[/yellow]")
    print(f"Elevation: [yellow]{vis_data['elevation_degrees']:.2f}°[/yellow]")
    print(f"Range:     [yellow]{vis_data['range_km']:.2f} km[/yellow]")
    
    if vis_data["is_visible"]:
        print("[green bold]Satellite is currently visible from your ground station.[/green bold]")
    else:
        print("[red bold]Satellite is NOT currently visible from your ground station.[/red bold]")
    
    # Pass predictions
    hours = pred_data["prediction_period_hours"]
    min_el = pred_data["minimum_elevation_degrees"]
    total_passes = pred_data["total_passes"]
    
    print(f"\n[bold]Pass Predictions (next {hours} hours, min elevation {min_el}°):[/bold]")
    print(f"Total passes: [cyan]{total_passes}[/cyan]")
    
    passes = pred_data["passes"]
    if passes:
        for i, sat_pass in enumerate(passes[:5], 1):  # Show first 5 passes
            start_time = datetime.fromisoformat(sat_pass["start_time"].replace("Z", ""))
            end_time = datetime.fromisoformat(sat_pass["end_time"].replace("Z", ""))
            max_el_time = datetime.fromisoformat(sat_pass["max_elevation_time"].replace("Z", ""))
            
            print(f"\n[yellow]Pass {i}:[/yellow]")
            print(f"  Start:    {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  End:      {end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  Duration: {sat_pass['duration_minutes']} minutes")
            print(f"  Max elevation: {sat_pass['max_elevation']}° at {max_el_time.strftime('%H:%M:%S UTC')}")

        next_pass_info = pred_data["next_pass"]
        if next_pass_info:
            time_to_next = next_pass_info['time_to_next_pass_minutes']
            if time_to_next > 0:
                print(f"\n[green bold]Next pass in {time_to_next:.1f} minutes![/green bold]")
            else:
                print(f"\n[green bold]Pass is happening now or just started![/green bold]")
    else:
        print("No passes found in the prediction window.")


def output_error(error_msg, json_output=False):
    """
    Output error message in appropriate format.
    
    Args:
        error_msg: Error message string
        json_output: Whether to output in JSON format
    """
    if json_output:
        error_result = {
            "error": str(error_msg),
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
        print(json.dumps(error_result, indent=2))
    else:
        print(f"[bold red]Error:[/bold red] {error_msg}")
