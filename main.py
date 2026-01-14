import json
import csv
import glob
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict


GPX_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.0"
     creator="{creator}"
     xmlns="http://www.topografix.com/GPX/1/0"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/0
                         http://www.topografix.com/GPX/1/0/gpx.xsd">
<trk><trkseg>
"""

GPX_FOOTER = """</trkseg></trk></gpx>
"""


# ---------- GPX helpers ----------

def write_gpx(
    points: List[Dict],
    output_path: Path,
    creator: str,
    source: str,
):
    with output_path.open("w", encoding="utf-8") as f:
        f.write(GPX_HEADER.format(creator=creator))

        for p in points:
            f.write(
                f'<trkpt lat="{p["lat"]}" lon="{p["lon"]}">'
                f'<time>{p["time"]}</time>'
                f'<src>{source}</src>'
                f'</trkpt>\n'
            )

        f.write(GPX_FOOTER)

    print(f"Exported → {output_path}")


# ---------- Polarsteps JSON ----------

def parse_polarsteps_json(path: Path) -> List[Dict]:
    with path.open() as f:
        data = json.load(f)

    points = []
    for entry in data['locations']:
        points.append(
            {
                "lat": entry["lat"],
                "lon": entry["lon"],
                "time": datetime.fromtimestamp(entry["time"]).isoformat() + "Z",
            }
        )

    # Ensure chronological order
    return sorted(points, key=lambda p: p["time"])


def convert_json(path: Path, creator: str):
    points = parse_polarsteps_json(path)
    output = path.with_name(path.stem + "_converted.gpx")
    write_gpx(points, output, creator, source="polarsteps")


# ---------- InfluxDB CSV ----------

def parse_influx_csv(path: Path) -> List[Dict]:
    points = []

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            if not row or not row[1]:
                continue

            points.append(
                {
                    "time": row[0].strip('"'),
                    "lat": row[1].strip('"'),
                    "lon": row[2].strip('"'),
                }
            )

    return points


def convert_csv(path: Path, creator: str):
    points = parse_influx_csv(path)
    output = path.with_name(path.stem + "_converted.gpx")
    write_gpx(points, output, creator, source="influxdb")


# ---------- CLI / entry point ----------

def get_git_username() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "config", "user.name"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except Exception:
        return input("Input your name (for the GPX header): ")


def main():
    creator = get_git_username()
    print(f"Using creator: {creator}")

    for json_file in map(Path, glob.glob("*.json")):
        print(f"Converting {json_file}")
        convert_json(json_file, creator)

    for csv_file in map(Path, glob.glob("*.csv")):
        print(f"Converting {csv_file}")
        convert_csv(csv_file, creator)


if __name__ == "__main__":
    main()
