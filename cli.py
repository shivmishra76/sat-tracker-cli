# cli.py
"""
Command line interface and argument parsing for satellite tracker.
"""

import argparse
import sys
from output import get_input_or_default
from rich import print


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        dict: Configuration dictionary with all parameters
    """
    if len(sys.argv) > 1:
        # CLI mode
        parser = argparse.ArgumentParser(description="Track a satellite by name")
        parser.add_argument("name", help="Satellite name (partial matches allowed)")
        parser.add_argument("--gs-lat", type=float, default=40.0, 
                          help="Ground station latitude (degrees)")
        parser.add_argument("--gs-lon", type=float, default=-88.0, 
                          help="Ground station longitude (degrees)")
        parser.add_argument("--gs-alt", type=float, default=0.2, 
                          help="Ground station altitude (km)")
        parser.add_argument("--json", action="store_true", 
                          help="Output results in JSON format")
        parser.add_argument("--hours", type=int, default=24, 
                          help="Hours ahead to predict passes (default: 24)")
        parser.add_argument("--min-elevation", type=float, default=10.0, 
                          help="Minimum elevation for pass prediction (default: 10.0)")
        parser.add_argument("--no-plot", action="store_true", 
                          help="Skip creating the position plot")
        parser.add_argument("--no-orbit", action="store_true",
                          help="Don't show satellite orbit on the map")
        parser.add_argument("--no-visibility", action="store_true",
                          help="Don't show visibility range on the map")
        args = parser.parse_args()

        return {
            "sat_name": args.name,
            "gs_lat": args.gs_lat,
            "gs_lon": args.gs_lon,
            "gs_alt": args.gs_alt,
            "json_output": args.json,
            "hours_ahead": args.hours,
            "min_elevation": args.min_elevation,
            "create_plot": not args.no_plot,
            "show_orbit": not args.no_orbit,
            "show_visibility": not args.no_visibility,
            "interactive": False
        }
    else:
        # Interactive mode
        print("[bold cyan]Satellite Tracker — Interactive Mode[/bold cyan]")
        sat_name = input("Enter satellite name (e.g. starlink, ISS): ").strip()
        gs_lat = get_input_or_default("Ground station latitude", 40.0)
        gs_lon = get_input_or_default("Ground station longitude", -88.0)
        gs_alt = get_input_or_default("Ground station altitude (km)", 0.2)
        
        return {
            "sat_name": sat_name,
            "gs_lat": gs_lat,
            "gs_lon": gs_lon,
            "gs_alt": gs_alt,
            "json_output": False,
            "hours_ahead": 24,
            "min_elevation": 10.0,
            "create_plot": True,
            "show_orbit": True,
            "show_visibility": True,
            "interactive": True
        }
