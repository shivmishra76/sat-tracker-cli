# plot_earth.py
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import platform
import subprocess
import os

def plot_satellite(lat, lon, save_path="sat_position.png"):
    plt.figure(figsize=(8, 6))
    m = Basemap(projection='mill', lon_0=0)
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='lightgray', lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')

    x, y = m(lon, lat)
    m.plot(x, y, 'ro', markersize=8)  # red dot for satellite

    plt.title("Satellite Position on Earth")
    plt.savefig(save_path)
    plt.close()

def open_image(path):
    if platform.system() == 'Darwin':
        subprocess.run(['open', path])
    elif platform.system() == 'Windows':
        os.startfile(path)
    else:
        subprocess.run(['xdg-open', path])
