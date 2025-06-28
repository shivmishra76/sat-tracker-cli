# plot_earth.py
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import platform
import subprocess
import os
import numpy as np
from datetime import datetime, timedelta, timezone
from sgp4.api import Satrec, jday
import pymap3d as pm
from rich import print

def plot_satellite(sat_lat, sat_lon, gs_lat=None, gs_lon=None, save_path="sat_position.png", 
                  line1=None, line2=None, show_orbit=True, show_visibility=True, min_elevation=10.0):
    """
    Plot satellite position with optional orbit and visibility features.
    
    Args:
        sat_lat, sat_lon: Satellite coordinates
        gs_lat, gs_lon: Ground station coordinates
        save_path: Output file path
        line1, line2: TLE lines for orbit calculation
        show_orbit: Whether to show satellite orbit
        show_visibility: Whether to show visibility circle
        min_elevation: Minimum elevation for visibility circle
    """
    plt.figure(figsize=(12, 8))
    m = Basemap(projection='mill', lon_0=0)
    m.drawcoastlines(color='gray', linewidth=0.5)
    m.drawcountries(color='gray', linewidth=0.3)
    m.fillcontinents(color='lightgray', lake_color='lightblue')
    m.drawmapboundary(fill_color='lightblue')
    
    # Add grid lines
    m.drawparallels(np.arange(-90, 91, 30), labels=[1,0,0,0], fontsize=8, color='gray', alpha=0.5)
    m.drawmeridians(np.arange(-180, 181, 60), labels=[0,0,0,1], fontsize=8, color='gray', alpha=0.5)

    # Plot satellite orbit if TLE data is provided
    if show_orbit and line1 is not None and line2 is not None:
        try:
            orbit_lats, orbit_lons = calculate_orbit_path(line1, line2)
            # Handle longitude wrapping for better visualization
            orbit_x, orbit_y = m(orbit_lons, orbit_lats)
            m.plot(orbit_x, orbit_y, 'b-', linewidth=2, alpha=0.7, label="Satellite Orbit")
        except Exception as e:
            print(f"[yellow]Warning: Could not plot orbit: {e}[/yellow]")

    # Plot visibility circle around ground station
    if show_visibility and gs_lat is not None and gs_lon is not None:
        try:
            vis_lats, vis_lons = calculate_visibility_circle(gs_lat, gs_lon, min_elevation)
            vis_x, vis_y = m(vis_lons, vis_lats)
            m.plot(vis_x, vis_y, 'g--', linewidth=1.5, alpha=0.6, 
                   label=f"Visibility Range (>{min_elevation}°)")
            # Fill the visibility area with light green using scatter
            m.scatter(vis_x, vis_y, c='green', alpha=0.1, s=1)
        except Exception as e:
            print(f"[yellow]Warning: Could not plot visibility circle: {e}[/yellow]")

    # Plot satellite position (red dot)
    x, y = m(sat_lon, sat_lat)
    m.plot(x, y, 'ro', markersize=10, label="Satellite", markeredgecolor='black', markeredgewidth=1)

    # Plot ground station (green dot), if provided
    if gs_lat is not None and gs_lon is not None:
        xg, yg = m(gs_lon, gs_lat)
        m.plot(xg, yg, 'gs', markersize=10, label="Ground Station", markeredgecolor='black', markeredgewidth=1)
        
        # Draw line from ground station to satellite
        m.plot([xg, x], [yg, y], 'r--', linewidth=1, alpha=0.8, label="Line of Sight")

    # Add legend
    plt.legend(loc='lower left', fontsize=10, framealpha=0.9)

    plt.title("Satellite Tracking Map with Orbit and Visibility", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def open_image(path):
    if platform.system() == 'Darwin':
        subprocess.run(['open', path])
    elif platform.system() == 'Windows':
        os.startfile(path)
    else:
        subprocess.run(['xdg-open', path])

def calculate_orbit_path(line1, line2, hours=1.5, points=100):
    """
    Calculate satellite orbit path for visualization.
    
    Args:
        line1, line2: TLE lines
        hours: How many hours of orbit to calculate
        points: Number of points along the orbit
    
    Returns:
        tuple: (latitudes, longitudes) arrays
    """
    sat = Satrec.twoline2rv(line1, line2)
    
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=hours)
    
    lats, lons = [], []
    
    for i in range(points):
        time_offset = (end_time - start_time) * i / (points - 1)
        current_time = start_time + time_offset
        
        jd, fr = jday(current_time.year, current_time.month, current_time.day,
                     current_time.hour, current_time.minute,
                     current_time.second + current_time.microsecond*1e-6)
        
        e, r, v = sat.sgp4(jd, fr)
        if e == 0:  # No propagation error
            lat, lon, alt = pm.eci2geodetic(r[0]*1000, r[1]*1000, r[2]*1000, current_time)
            lats.append(float(lat))
            lons.append(float(lon))
    
    return np.array(lats), np.array(lons)

def calculate_visibility_circle(gs_lat, gs_lon, min_elevation=10.0, earth_radius_km=6371):
    """
    Calculate visibility circle around ground station.
    
    Args:
        gs_lat, gs_lon: Ground station coordinates
        min_elevation: Minimum elevation angle in degrees
        earth_radius_km: Earth radius in km
    
    Returns:
        tuple: (latitudes, longitudes) arrays for visibility circle
    """
    # Calculate horizon distance based on minimum elevation
    # For simplicity, we'll use a rough approximation
    if min_elevation <= 0:
        # Horizon distance for 0° elevation
        horizon_distance_km = np.sqrt(2 * earth_radius_km * 400)  # Assuming ~400km altitude
    else:
        # Approximate distance for given elevation angle
        sat_altitude_km = 400  # Typical LEO altitude
        horizon_distance_km = sat_altitude_km / np.tan(np.radians(min_elevation))
    
    # Convert to angular distance
    angular_distance = horizon_distance_km / earth_radius_km
    
    # Create circle points
    angles = np.linspace(0, 2*np.pi, 100)
    circle_lats = []
    circle_lons = []
    
    for angle in angles:
        # Calculate point on circle
        lat_rad = np.radians(gs_lat)
        lon_rad = np.radians(gs_lon)
        
        new_lat = np.arcsin(np.sin(lat_rad) * np.cos(angular_distance) +
                           np.cos(lat_rad) * np.sin(angular_distance) * np.cos(angle))
        
        new_lon = lon_rad + np.arctan2(np.sin(angle) * np.sin(angular_distance) * np.cos(lat_rad),
                                      np.cos(angular_distance) - np.sin(lat_rad) * np.sin(new_lat))
        
        circle_lats.append(np.degrees(new_lat))
        circle_lons.append(np.degrees(new_lon))
    
    return np.array(circle_lats), np.array(circle_lons)
