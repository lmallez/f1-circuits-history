import csv
import sys
from datetime import datetime
import plotly.express as px

start_year = 1950
end_year = 2022


def read_file(year: int):
    with open("data/{}.csv".format(year)) as infile:
        reader = csv.reader(infile)
        lines = [line for line in reader]
        circuits = [
            {b: f for b, f in zip(lines[0], line)} for line in lines[1:]
        ]
        meta = {"year": year, "decade": round(year, -1)}
        for circuit in circuits:
            circuit["lat"] = float(circuit["lat"])
            circuit["lon"] = float(circuit["lon"])
            circuit |= meta
        return circuits


def figure(circuits, animation_frame=None, range_color=1.0):
    return px.density_mapbox(
        circuits,
        lat="lat",
        lon="lon",
        radius=20,
        mapbox_style="carto-darkmatter",
        animation_frame=animation_frame,
        hover_name="name",
        hover_data=["location", "country"],
        center={"lat": 15, "lon": 5},
        zoom=1.75,
        title="F1 Tracks{}".format(
            " by {}".format(animation_frame) if animation_frame else ""
        ),
        range_color=[0, range_color / 2],
    )


if __name__ == "__main__":
    circuits = []
    for i in range(start_year, end_year + 1):
        circuits += read_file(i)

    figure(circuits, animation_frame="year").write_html("{}/year.html".format(sys.argv[1]))
    figure(circuits, animation_frame="decade", range_color=10).write_html("out/decade.html")
    figure(circuits, range_color=(end_year - start_year) / 2).write_html("out/all.html")
