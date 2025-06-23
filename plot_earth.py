# plot_earth.py
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import platform
import subprocess
import os

def plot_satellite(sat_lat, sat_lon, gs_lat=None, gs_lon=None, save_path="sat_position.png"):
    plt.figure(figsize=(8, 6))
    m = Basemap(projection='mill', lon_0=0)
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='lightgray', lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')

    # Plot satellite position (red dot)
    x, y = m(sat_lon, sat_lat)
    m.plot(x, y, 'ro', markersize=8, label="Satellite")

    # Plot ground station (green dot), if provided
    if gs_lat is not None and gs_lon is not None:
        xg, yg = m(gs_lon, gs_lat)
        m.plot(xg, yg, 'go', markersize=8, label="Ground Station")

    # Add legend
    plt.legend(loc='lower left')

    plt.title("Satellite and Ground Station Positions on Earth")
    plt.savefig(save_path)
    plt.close()

def open_image(path):
    if platform.system() == 'Darwin':
        subprocess.run(['open', path])
    elif platform.system() == 'Windows':
        os.startfile(path)
    else:
        subprocess.run(['xdg-open', path])
