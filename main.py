# main.py
from tle import fetch_tle
from orbit import get_position
from plot_earth import plot_satellite, open_image
import argparse

def main():
    parser = argparse.ArgumentParser(description="Track a satellite by name")
    parser.add_argument("name", help="Satellite name (partial matches allowed)")
    args = parser.parse_args()

    try:
        line1, line2 = fetch_tle(args.name)
        pos = get_position(line1, line2)

        print(f"Latitude:  {pos['lat']:.4f}°")
        print(f"Longitude: {pos['lon']:.4f}°")
        print(f"Altitude:  {pos['alt_km']:.2f} km")
        print(f"Velocity:  {pos['velocity_kms']:.2f} km/s")

        plot_satellite(pos['lat'], pos['lon'])
        print("Satellite position map saved as sat_position.png")
        open_image("sat_position.png")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
