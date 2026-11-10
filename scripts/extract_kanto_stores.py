#!/usr/bin/env python3
"""
Extract all Teppay-compatible stores in Tokyo, Kanagawa, Chiba (and Kanto metro area)
from Geofabrik kanto-latest.osm.pbf and save to data/stores.json.
"""
import json
import re
import sys
from datetime import datetime, timezone
import osmium

PBF_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/kanto.osm.pbf"
OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else "data/stores.json"

html = open("index.html", encoding="utf-8").read()
m = re.search(r"const CHAINS_DATA\s*=\s*(\[\{.*?\}\]);", html, re.S)
if not m:
    raise RuntimeError("CHAINS_DATA not found in index.html")
chains_data = json.loads(m.group(1))

# Prepare keyword matcher identical to matchPoiToTeppayChain in index.html
chain_Matchers = []
for idx, c in enumerate(chains_data):
    kws = [kw.lower() for kw in (c.get("match_keywords") or [c["name"]]) if len(kw) >= 2]
    chain_Matchers.append((idx, c["name"], kws))

def match_chain(name: str, brand: str):
    target = f"{name or ''} {brand or ''}".replace("‐", "-").replace("－", "-").strip()
    if not target:
        return None
    lower = target.lower()
    has_joyful_honda = "ジョイフル本田" in lower
    has_seven_bank_only = ("セブン銀行" in lower) and ("セブン-イレブン" not in lower) and ("セブンイレブン" not in lower)
    if has_seven_bank_only:
        return None
    for idx, cname, kws in chain_Matchers:
        for kw in kws:
            if kw in lower:
                if has_joyful_honda and cname != "ジョイフル本田":
                    continue
                return cname
    return None

# Bounding box covering Tokyo, Kanagawa, Chiba (+ southern Saitama/Ibaraki metro)
BBOX = (34.85, 138.90, 36.15, 140.95)  # (south, west, north, east)

POI_KEYS = ("shop", "amenity", "leisure", "craft", "tourism", "office")

stores_map = {}
names_list = []
name_to_idx = {}

def add_poi(tags, lat, lng):
    if not (BBOX[0] <= lat <= BBOX[2] and BBOX[1] <= lng <= BBOX[3]):
        return
    if not any(k in tags for k in POI_KEYS):
        return
    name = tags.get("name") or tags.get("name:ja") or ""
    brand = tags.get("brand") or tags.get("brand:ja") or ""
    if not name and not brand:
        return
    cname = match_chain(name, brand)
    if not cname:
        return
    lat5 = round(lat, 5)
    lng5 = round(lng, 5)
    dedup_key = f"{cname}_{round(lat * 1000)}_{round(lng * 1000)}"
    if dedup_key in stores_map:
        return
    if cname not in name_to_idx:
        name_to_idx[cname] = len(names_list)
        names_list.append(cname)
    ci = name_to_idx[cname]
    display_name = name or brand or cname
    stores_map[dedup_key] = [ci, lat5, lng5, "" if display_name == cname else display_name]

class StoreHandler(osmium.SimpleHandler):
    def node(self, n):
        if len(n.tags) == 0 or not n.location.valid():
            return
        add_poi(n.tags, n.location.lat, n.location.lon)

    def area(self, a):
        if len(a.tags) == 0:
            return
        try:
            # Compute simple centroid from outer ring
            for ring in a.outer_rings():
                lats = [nd.lat for nd in ring if nd.location.valid()]
                lons = [nd.lon for nd in ring if nd.location.valid()]
                if lats and lons:
                    add_poi(a.tags, sum(lats) / len(lats), sum(lons) / len(lons))
                break
        except Exception:
            pass

print("Scanning PBF...", flush=True)
h = StoreHandler()
h.apply_file(PBF_PATH, locations=True)
stores_list = list(stores_map.values())
print(f"Matched {len(stores_list)} stores across {len(names_list)} chains", flush=True)

out = {
    "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "chains": names_list,
    "stores": stores_list,
}
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
