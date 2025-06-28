# main.py
"""
Main entry point for the satellite tracker application.
"""

import json
from datetime import datetime, timezone
from rich import print
from tle import fetch_tle
from orbit import get_position
from plot_earth import plot_satellite, open_image
from visibility import check_visibility, get_orbital_period, predict_passes, get_next_pass_info
from output import format_satellite_data, output_human_readable, output_json, get_input_or_default
from cli import parse_arguments

def main():
    # Parse command line arguments or get interactive input
    config = parse_arguments()
    
    try:
        if not config["json_output"]:
            print("[bold green]Tracking satellite position and visibility...[/bold green]")

        # Fetch TLE and compute satellite position
        line1, line2 = fetch_tle(config["sat_name"])
        pos = get_position(line1, line2)

        # Compute visibility from ground station
        az, el, rng = check_visibility(
            pos['lat'], pos['lon'], pos['alt_km'],
            config["gs_lat"], config["gs_lon"], config["gs_alt"]
        )

        # Calculate orbital period
        orbital_period_minutes = get_orbital_period(line1, line2)

        # Predict passes
        passes = predict_passes(line1, line2, config["gs_lat"], config["gs_lon"], config["gs_alt"], 
                              hours_ahead=config["hours_ahead"], min_elevation=config["min_elevation"])

        # Get next pass information
        next_pass_info = get_next_pass_info(passes)

        # Format the data
        result = format_satellite_data(
            config["sat_name"], pos, config["gs_lat"], config["gs_lon"], config["gs_alt"],
            az, el, rng, orbital_period_minutes, passes, next_pass_info,
            config["hours_ahead"], config["min_elevation"]
        )

        # Output results
        if config["json_output"]:
            output_json(result)
        else:
            output_human_readable(result, config["create_plot"])
            
            # Create and display the satellite position plot
            if config["create_plot"]:
                plot_satellite(pos['lat'], pos['lon'], config["gs_lat"], config["gs_lon"],
                             line1=line1, line2=line2, 
                             show_orbit=config["show_orbit"], 
                             show_visibility=config["show_visibility"],
                             min_elevation=config["min_elevation"])
                print("Satellite position map saved as [bold]sat_position.png[/bold]")
                open_image("sat_position.png")

    except Exception as e:
        if config["json_output"]:
            error_result = {
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
            }
            print(json.dumps(error_result, indent=2))
        else:
            print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
