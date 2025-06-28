# visibility.py
"""
Visibility calculations for satellite tracking.
Handles ground station visibility, orbital mechanics, and pass predictions.
"""

from datetime import datetime, timedelta, timezone
from pymap3d import geodetic2aer
from sgp4.api import Satrec, jday
import pymap3d as pm


def check_visibility(sat_lat, sat_lon, sat_alt_km, gs_lat, gs_lon, gs_alt_km):
    """
    Calculate azimuth, elevation, and range from ground station to satellite.
    
    Args:
        sat_lat: Satellite latitude (degrees)
        sat_lon: Satellite longitude (degrees)
        sat_alt_km: Satellite altitude (km)
        gs_lat: Ground station latitude (degrees)
        gs_lon: Ground station longitude (degrees)
        gs_alt_km: Ground station altitude (km)
    
    Returns:
        tuple: (azimuth, elevation, range) in degrees, degrees, meters
    """
    az, el, rng = geodetic2aer(
        sat_lat, sat_lon, sat_alt_km * 1000,
        gs_lat, gs_lon, gs_alt_km * 1000
    )
    return float(az), float(el), float(rng)


def get_orbital_period(line1, line2):
    """
    Calculate orbital period in minutes from TLE data.
    
    Args:
        line1: First line of TLE data
        line2: Second line of TLE data
    
    Returns:
        float: Orbital period in minutes
    """
    # Extract mean motion from line 2 (revolutions per day)
    mean_motion = float(line2[52:63])
    # Period = 24 hours / revolutions per day * 60 minutes/hour
    period_minutes = (24 * 60) / mean_motion
    return period_minutes


def predict_passes(line1, line2, gs_lat, gs_lon, gs_alt, hours_ahead=24, min_elevation=0):
    """
    Predict satellite passes over ground station.
    
    Args:
        line1: First line of TLE data
        line2: Second line of TLE data
        gs_lat: Ground station latitude (degrees)
        gs_lon: Ground station longitude (degrees)
        gs_alt: Ground station altitude (km)
        hours_ahead: Hours to predict ahead (default: 24)
        min_elevation: Minimum elevation for visibility (degrees, default: 0)
    
    Returns:
        list: List of pass dictionaries with timing and elevation data
    """
    sat = Satrec.twoline2rv(line1, line2)
    passes = []
    
    # Get orbital period for step size
    period_minutes = get_orbital_period(line1, line2)
    step_minutes = max(1, period_minutes / 60)  # Sample at least 60 times per orbit
    
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=hours_ahead)
    
    current_time = start_time
    in_pass = False
    pass_start = None
    max_elevation = 0
    max_el_time = None
    
    while current_time <= end_time:
        jd, fr = jday(current_time.year, current_time.month, current_time.day, 
                     current_time.hour, current_time.minute, 
                     current_time.second + current_time.microsecond*1e-6)
        
        e, r, v = sat.sgp4(jd, fr)
        if e == 0:  # No propagation error
            lat, lon, alt = pm.eci2geodetic(r[0]*1000, r[1]*1000, r[2]*1000, current_time)
            az, el, rng = geodetic2aer(lat, lon, alt, gs_lat, gs_lon, gs_alt*1000)
            el = float(el)  # Convert to float to avoid numpy issues
            
            if el > min_elevation:
                if not in_pass:
                    # Pass is starting
                    in_pass = True
                    pass_start = current_time
                    max_elevation = el
                    max_el_time = current_time
                else:
                    # Continue tracking max elevation
                    if el > max_elevation:
                        max_elevation = el
                        max_el_time = current_time
            else:
                if in_pass:
                    # Pass is ending
                    pass_end = current_time - timedelta(minutes=step_minutes)
                    duration = (pass_end - pass_start).total_seconds() / 60
                    
                    passes.append({
                        "start_time": pass_start.isoformat() + "Z",
                        "end_time": pass_end.isoformat() + "Z",
                        "max_elevation": round(max_elevation, 2),
                        "max_elevation_time": max_el_time.isoformat() + "Z",
                        "duration_minutes": round(duration, 1)
                    })
                    
                    in_pass = False
                    max_elevation = 0
        
        current_time += timedelta(minutes=step_minutes)
    
    return passes


def get_next_pass_info(passes):
    """
    Get information about the next pass.
    
    Args:
        passes: List of pass dictionaries from predict_passes()
    
    Returns:
        dict or None: Next pass information with time remaining
    """
    if not passes:
        return None
    
    next_pass = passes[0]
    start_time = datetime.fromisoformat(next_pass["start_time"].replace("Z", ""))
    time_to_pass = start_time - datetime.now(timezone.utc)
    
    return {
        "time_to_next_pass_minutes": round(time_to_pass.total_seconds() / 60, 1),
        "next_pass": next_pass
    }
