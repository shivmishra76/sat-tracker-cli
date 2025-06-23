# orbit.py
from sgp4.api import Satrec
from sgp4.api import jday
from datetime import datetime
import pymap3d as pm

def get_position(line1, line2):
    sat = Satrec.twoline2rv(line1, line2)

    now = datetime.utcnow()
    jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second + now.microsecond*1e-6)

    e, r, v = sat.sgp4(jd, fr)
    if e != 0:
        raise RuntimeError("Propagation error")

    # r = [x, y, z] in km (ECI frame)
    lat, lon, alt = pm.eci2geodetic(r[0]*1000, r[1]*1000, r[2]*1000, now)
    return {
        "lat": float(lat),
        "lon": float(lon),
        "alt_km": float(alt) / 1000,
        "velocity_kms": float(sum(x**2 for x in v) ** 0.5)
    }

