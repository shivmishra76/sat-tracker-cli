# tle.py
import requests

CELESTRAK_URL = "https://celestrak.com/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

def fetch_tle(name):
    response = requests.get(CELESTRAK_URL)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch TLEs: {response.status_code}")

    lines = response.text.strip().split("\n")
    name = name.lower()

    matches = []
    for i in range(0, len(lines) - 2, 3):
        sat_name = lines[i].strip()
        if name in sat_name.lower():
            matches.append((sat_name, lines[i+1].strip(), lines[i+2].strip()))

    if not matches:
        raise ValueError(f"Satellite '{name}' not found.")

    if len(matches) == 1:
        return matches[0][1], matches[0][2]

    print("Multiple matches found:")
    for idx, (sat_name, _, _) in enumerate(matches[:10]):  # show top 10
        print(f"{idx + 1}. {sat_name}")

    while True:
        choice = input(f"Select a satellite by number (1-{min(len(matches),10)}): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(matches[:10]):
                return matches[idx][1], matches[idx][2]
        print("Invalid choice, please try again.")
