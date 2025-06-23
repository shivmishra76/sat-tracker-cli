# main.py
import argparse
import sys
from tle import fetch_tle
from orbit import get_position
from plot_earth import plot_satellite, open_image
from pymap3d import geodetic2aer
from rich import print

def get_input_or_default(prompt, default):
    try:
        value = input(f"{prompt} [{default}]: ").strip()
        return float(value) if value else default
    except ValueError:
        print("[red]Invalid input. Using default.[/red]")
        return default

def check_visibility(sat_lat, sat_lon, sat_alt_km, gs_lat, gs_lon, gs_alt_km):
    az, el, rng = geodetic2aer(
        sat_lat, sat_lon, sat_alt_km * 1000,
        gs_lat, gs_lon, gs_alt_km * 1000
    )
    return az, el, rng

def main():
    # Choose between CLI and interactive mode
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Track a satellite by name")
        parser.add_argument("name", help="Satellite name (partial matches allowed)")
        parser.add_argument("--gs-lat", type=float, default=40.0, help="Ground station latitude (degrees)")
        parser.add_argument("--gs-lon", type=float, default=-88.0, help="Ground station longitude (degrees)")
        parser.add_argument("--gs-alt", type=float, default=0.2, help="Ground station altitude (km)")
        args = parser.parse_args()

        sat_name = args.name
        gs_lat = args.gs_lat
        gs_lon = args.gs_lon
        gs_alt = args.gs_alt
    else:
        print("[bold cyan]Satellite Tracker — Interactive Mode[/bold cyan]")
        sat_name = input("Enter satellite name (e.g. starlink, ISS): ").strip()
        gs_lat = get_input_or_default("Ground station latitude", 40.0)
        gs_lon = get_input_or_default("Ground station longitude", -88.0)
        gs_alt = get_input_or_default("Ground station altitude (km)", 0.2)

    try:
        print("[bold green]Tracking satellite position and visibility...[/bold green]")

        # Fetch TLE and compute satellite position
        line1, line2 = fetch_tle(sat_name)
        pos = get_position(line1, line2)

        print(f"Latitude:  [cyan]{pos['lat']:.4f}°[/cyan]")
        print(f"Longitude: [cyan]{pos['lon']:.4f}°[/cyan]")
        print(f"Altitude:  [cyan]{pos['alt_km']:.2f} km[/cyan]")
        print(f"Velocity:  [cyan]{pos['velocity_kms']:.2f} km/s[/cyan]")

        # Plot Earth map with satellite + ground station
        plot_satellite(pos['lat'], pos['lon'], gs_lat, gs_lon)
        print("Satellite position map saved as [bold]sat_position.png[/bold]")

        # Compute visibility from ground station
        az, el, rng = check_visibility(
            pos['lat'], pos['lon'], pos['alt_km'],
            gs_lat, gs_lon, gs_alt
        )

        print(f"Azimuth:   [yellow]{az:.2f}°[/yellow]")
        print(f"Elevation: [yellow]{el:.2f}°[/yellow]")
        print(f"Range:     [yellow]{rng / 1000:.2f} km[/yellow]")

        if el > 0:
            print("[green bold]Satellite is currently visible from your ground station.[/green bold]")
        else:
            print("[red bold]Satellite is NOT currently visible from your ground station.[/red bold]")

        # Open the image
        open_image("sat_position.png")

    except Exception as e:
        print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
