import os, json, urllib.request
import pandas as pd
from flask import Flask, render_template, url_for, jsonify, request

# create and configure the app
app = Flask(__name__)

paths = {
    2017: {
        "pickup_count": "pickup_count_2017.csv",
        "dropoff_count": "dropoff_count_2017.csv",
        "pickup_dropoff_mapping": "pickup_dropoff_mapping_2017.csv",
    },
    2018: {
        "pickup_count": "pickup_count_2018.csv",
        "dropoff_count": "dropoff_count_2018.csv",
        "pickup_dropoff_mapping": "pickup_dropoff_mapping_2018.csv",
    },
    2019: {
        "pickup_count": "pickup_count_2019.csv",
        "dropoff_count": "dropoff_count_2019.csv",
        "pickup_dropoff_mapping": "pickup_dropoff_mapping_2019.csv",
    },
}


@app.route("/")
def index():
    with urllib.request.urlopen(
        "https://data.cityofnewyork.us/resource/755u-8jsi.geojson"
    ) as url:
        zones = json.loads(url.read().decode())

    return render_template("index.html", data=zones)


@app.route("/<int:zone>/<int:year>", methods=["GET"])
def process_data(zone, year):
    # load in preprocessed data for quick access
    pickup_count = pd.read_csv(paths[year].get("pickup_count"))
    dropoff_count = pd.read_csv(paths[year].get("dropoff_count"))
    pickup_dropoff_mapping = pd.read_csv(paths[year].get("pickup_dropoff_mapping"))

    picked_up = dropped_off = 0

    query = pickup_count.loc[pickup_count["pulocationid"] == zone]
    if not query.empty:
        picked_up = query["totalcount"].item()

    query = dropoff_count.loc[dropoff_count["dolocationid"] == zone]
    if not query.empty:
        dropped_off = query["totalcount"].item()

    do_query = pickup_dropoff_mapping.loc[
        pickup_dropoff_mapping["dolocationid"] == zone
    ]
    pu_query = pickup_dropoff_mapping.loc[
        pickup_dropoff_mapping["pulocationid"] == zone
    ]

    message = {
        "pickup": picked_up,
        "dropoff": dropped_off,
        "pickup_zones": do_query.loc[:, ["pulocationid", "totalcount"]].values.tolist(),
        "dropoff_zones": pu_query.loc[
            :, ["dolocationid", "totalcount"]
        ].values.tolist(),
    }
    return jsonify(message)  # serialize and use JSON headers


if __name__ == "__main__":
    app.run(debug=True)
