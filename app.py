lz
thehowtoproject123
Online

aditya — 8/20/25, 2:30 PM
Hello, Are you still searching for a Team? I'm looking for members
lz — 8/21/25, 9:59 AM
I am. What are you interested in? Or otherwise put: members for what? 🙂

See you tomorrow!
aditya — 8/22/25, 1:51 PM
Hi Lukas, Sorry for the late reply. I'm planning to work on the the SBB challenge.
aditya — 8/22/25, 4:32 PM
Yes, I'll reach in 15 mins
aditya — 8/22/25, 5:00 PM
Hey I've reached here
lz — 8/22/25, 5:02 PM
I'm still in front of the aula.
lz — Yesterday at 9:12 PM
def get_rampe_treppe_url(bps_name: str) -> str:
    return f"https://data.sbb.ch/api/explore/v2.1/catalog/datasets/rampe-treppe/records?select=typ%2Cnutzung%2Chandlauf%2Cgeopos&where=bps_name%3D"{bps_name}""
This works.
async def get_treppen_and_ramps(bps_name: str):

    url = get_rampe_treppe_url(bps_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            results = data["results"]
            return results
This is how we can make the call. Check also out the according test:
import json

import aiohttp
import pytest

from src.mapunfold import get_rampe_treppe_url


@pytest.mark.asyncio
async def test_async_call():
    with open('tests/bps_names.json', 'r') as file:
        bps_names = json.load(file)

    name = bps_names[6]["bps_name"]
    url = get_rampe_treppe_url(name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            data = await resp.json()
            results = data["results"]
            assert len(results) > 0
I 'll continue to push to the branch night for now.
aditya — Yesterday at 10:28 PM
absl-py==2.2.2
annotated-types==0.7.0
anyio==4.10.0
astunparse==1.6.3
attrs==25.3.0
beautifulsoup4==4.13.4
Expand
requirements.txt
6 KB
lz — Yesterday at 11:17 PM
Any luck with the queries?
I am checking out ollama now. pytorch didn't run on my machine in 5 minutes. So I uninstalled it and try to find another solution.
If you get it to work, we could document that it only runs on a strong machine.
aditya — 11:50 AM
# app.py
# Flask app for wheelchair-friendly route planner

from flask import Flask, render_template, request
import os
import math
Expand
app.py
7 KB
﻿
aditya
aditya08189
# app.py
# Flask app for wheelchair-friendly route planner

from flask import Flask, render_template, request
import os
import math
import networkx as nx
import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
import osmnx as ox

# -------- Config --------
POI_PATH = "datasets.geojson"     # Your POI file
CATEGORY_FIELD = "category"
BUFFER_METERS = 25
RAMP_SEARCH_METERS = 60
NETWORK_TYPE = "walk"
# ------------------------

app = Flask(__name__)

# ---------------- Utility functions ----------------
def load_pois(path: str, category_field: str) -> gpd.GeoDataFrame:
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
        lat_col = next((c for c in df.columns if c.lower() in ("lat","latitude","y")), None)
        lon_col = next((c for c in df.columns if c.lower() in ("lon","long","longitude","x")), None)
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs="EPSG:4326")
    else:
        gdf = gpd.read_file(path)
        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)
        elif gdf.crs.to_epsg()!=4326:
            gdf = gdf.to_crs("EPSG:4326")
    gdf[category_field] = gdf[category_field].astype(str).str.lower().str.strip()
    return gdf

def shortest_path_route(G, start_latlon, end_latlon, weight="length"):
    slat, slon = start_latlon
    elat, elon = end_latlon
    orig = ox.distance.nearest_nodes(G, slon, slat)
    dest = ox.distance.nearest_nodes(G, elon, elat)
    route_nodes = nx.shortest_path(G, orig, dest, weight=weight)
    coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route_nodes]
    route_length_m = 0.0
    for u, v in zip(route_nodes[:-1], route_nodes[1:]):
        edge_data = G.get_edge_data(u, v)
        if isinstance(edge_data, dict):
            edge_data = edge_data[0] if 0 in edge_data else list(edge_data.values())[0]
        route_length_m += float(edge_data.get("length",0))
    return coords, route_length_m

def points_along_route(pois_wgs84: gpd.GeoDataFrame, route_coords, buffer_m=BUFFER_METERS, category_field=CATEGORY_FIELD):
    route_line_wgs = LineString([(lon, lat) for lat, lon in route_coords])
    route_gdf = gpd.GeoDataFrame([{"id":1}], geometry=[route_line_wgs], crs="EPSG:4326")
    route_m = route_gdf.to_crs(3857)
    pois_m = pois_wgs84.to_crs(3857)
    line_m = route_m.geometry.iloc[0]
    route_buffer = line_m.buffer(buffer_m)
    hits = pois_m[pois_m.intersects(route_buffer)].copy()
    if hits.empty:
        return gpd.GeoDataFrame(columns=[category_field,"distance_m","s_along_m","geometry"], crs="EPSG:4326")
    hits["distance_m"] = hits.geometry.distance(line_m)
    hits["s_along_m"] = hits.geometry.apply(lambda g: float(line_m.project(g)))
    hits = hits.to_crs("EPSG:4326")
    hits.sort_values("s_along_m", inplace=True)
    return hits[[category_field,"distance_m","s_along_m","geometry"]]

def pair_stairs_with_ramps(pois_along: gpd.GeoDataFrame, ramp_search_m=RAMP_SEARCH_METERS):
    if pois_along.empty:
        return []
    m = pois_along.to_crs(3857).copy()
    pairs = []
    ramps = m[m[CATEGORY_FIELD]=="ramp"].copy()
    for idx,row in m.iterrows():
        if row[CATEGORY_FIELD]!="stairs": continue
        p = row.geometry
        if ramps.empty:
            pairs.append({"stairs_idx":idx,"ramp_idx":None,"ramp_distance_m":None})
            continue
        ramps["dist"] = ramps.geometry.distance(p)
        nearby = ramps[ramps["dist"]<=ramp_search_m]
        best = nearby.iloc[nearby["dist"].argmin()] if not nearby.empty else ramps.iloc[ramps["dist"].argmin()]
        pairs.append({"stairs_idx":idx,"ramp_idx":best.name,"ramp_distance_m":float(best["dist"])})
    return pairs

def build_custom_instructions(route_len_m, pois_along, pairs):
    steps = []
    steps.append(f"1. Start your journey. The total distance is about {int(route_len_m)} meters.")
    step_num = 2

    for idx, row in pois_along.iterrows():
        cat = row[CATEGORY_FIELD]
        dist = int(row["s_along_m"]) if pd.notna(row["s_along_m"]) else None

        if cat == "stairs":
            pair = next((p for p in pairs if p["stairs_idx"]==idx), None)
            if pair and pair["ramp_idx"] is not None:
                steps.append(f"{step_num}. Around {dist} meters ahead there are stairs. Use the nearby ramp instead (within {int(pair['ramp_distance_m'])} m).")
            else:
                steps.append(f"{step_num}. Around {dist} meters ahead there are stairs, but no ramp nearby.")
        elif cat == "ramp":
            steps.append(f"{step_num}. At about {dist} meters, you will find a ramp for easier access.")
        elif cat == "ticket counter":
            steps.append(f"{step_num}. Around {dist} meters you pass a ticket counter.")
        elif cat == "waiting room":
            steps.append(f"{step_num}. At {dist} meters there is a waiting room available.")
        else:
            steps.append(f"{step_num}. At {dist} meters, you pass a {cat}.")
        step_num += 1

    steps.append(f"{step_num}. Continue until you reach your destination after about {int(route_len_m)} meters.")
    return "\n".join(steps)
# ---------------------------------------------------

@app.route("/", methods=["GET","POST"])
def index():
    instructions = None
    if request.method=="POST":
        start_lat = float(request.form["start_lat"])
        start_lon = float(request.form["start_lon"])
        end_lat = float(request.form["end_lat"])
        end_lon = float(request.form["end_lon"])

        # load pois
        pois = load_pois(POI_PATH, CATEGORY_FIELD)

        # graph
        G = ox.graph_from_point((start_lat,start_lon), dist=2000, network_type=NETWORK_TYPE)
        route_coords, route_len_m = shortest_path_route(G, (start_lat,start_lon), (end_lat,end_lon))

        # pois along
        pois_along = points_along_route(pois, route_coords)
        pairs = pair_stairs_with_ramps(pois_along)

        instructions = build_custom_instructions(route_len_m, pois_along, pairs)

    return render_template("index2.html", instructions=instructions)

if __name__=="__main__":
    app.run(debug=True)
app.py
7 KB