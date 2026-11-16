#!/usr/bin/env python3
"""
Automated Verification and Ingestion Engine for Store Addition Requests.
Reads pending requests from Google Sheet (via Apps Script Web App or gsheets CLI),
verifies chain validity, existence, geocoding consistency, and duplicate status,
and automatically updates stores datasets for HIGH-confidence entries.
"""
import json
import math
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "1emw7e7aW_9NXGT7PNbaSS1QihyTqqdNepkkNSLo-e_M")
SHEET_NAME = "Requests"
APPS_SCRIPT_URL = os.getenv(
    "APPS_SCRIPT_URL",
    "https://script.google.com/macros/s/AKfycbzCKjGijNvxx7WhiKHvDKdiq3gazAudxTQ8LnF86LxuMS-Jw5Z-64fbjdqyldXeiBKR_A/exec"
)

# 1. Load chains data from index.html
with open("index.html", encoding="utf-8") as f:
    html = f.read()
m = re.search(r"const CHAINS_DATA\s*=\s*(\[\{.*?\}\]);", html, re.S)
if not m:
    raise RuntimeError("CHAINS_DATA not found in index.html")
CHAINS_DATA = json.loads(m.group(1))

# Build lookup by name and alias -> returns canonical chain name
CHAIN_LOOKUP = {}
for c in CHAINS_DATA:
    cname = c["name"]
    CHAIN_LOOKUP[cname.lower().replace("‐", "-").replace("－", "-").strip()] = cname
    for kw in c.get("match_keywords", []):
        CHAIN_LOOKUP[kw.lower().replace("‐", "-").replace("－", "-").strip()] = cname

# 2. Helper: Haversine distance in meters
def haversine_meters(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

# 3. Helper: Geocode address using GSI (国土地理院) API
def geocode_gsi(address):
    if not address or len(address.strip()) < 2:
        return None
    try:
        url = "https://msearch.gsi.go.jp/address-search/AddressSearch?q=" + urllib.parse.quote(address)
        req = urllib.request.Request(url, headers={"User-Agent": "TeppayVerifier/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            res = json.loads(r.read().decode("utf-8"))
            if res and len(res) > 0:
                coords = res[0]["geometry"]["coordinates"] # [lon, lat]
                return coords[1], coords[0]
    except Exception as e:
        print(f"Geocoding error for '{address}': {e}", file=sys.stderr)
    return None

# 4. Helper: Find which store file a lat/lon belongs to
def get_target_file(lat, lon):
    if 34.50 <= lat <= 38.60 and 137.30 <= lon <= 141.25:
        return "data/stores.json"
    elif 33.80 <= lat <= 38.60 and 134.50 <= lon <= 141.20:
        return "data/stores_ring2.json"
    elif lon < 134.50 and lat > 32.0:
        return "data/stores_ring3.json"
    else:
        return "data/stores_ring4.json"

# 5. Helper: Read existing stores to check for duplicates
EXISTING_STORES = [] # list of (cname, lat, lon, name, file)
for fn in ["data/stores.json", "data/stores_ring2.json", "data/stores_ring3.json", "data/stores_ring4.json"]:
    if os.path.exists(fn):
        try:
            with open(fn, encoding="utf-8") as fp:
                d = json.load(fp)
                ch = d.get("chains", [])
                for s in d.get("stores", []):
                    cname = ch[s[0]] if s[0] < len(ch) else ""
                    name = s[3] if len(s) > 3 else ""
                    EXISTING_STORES.append((cname, s[1], s[2], name, fn))
        except Exception as e:
            print(f"Error loading {fn}: {e}", file=sys.stderr)

print(f"Loaded {len(EXISTING_STORES)} existing stores across all regions.")

def check_duplicate(cname, lat, lon):
    for ecname, elat, elon, ename, efn in EXISTING_STORES:
        if ecname == cname:
            dist = haversine_meters(lat, lon, elat, elon)
            if dist < 150:  # within 150m is duplicate
                return True, dist, ename, efn
    return False, 0, "", ""

def match_chain(input_chain):
    if not input_chain:
        return None
    s = input_chain.strip().lower().replace("‐", "-").replace("－", "-")
    if s in CHAIN_LOOKUP:
        return CHAIN_LOOKUP[s]
    for k, v in CHAIN_LOOKUP.items():
        if k in s or s in k:
            return v
    return None

def verify_request(req):
    raw_chain = req.get("chain_name", "").strip()
    raw_name = req.get("store_name", "").strip()
    raw_lat = req.get("lat")
    raw_lon = req.get("lon")
    raw_addr = req.get("address", "").strip()
    raw_note = req.get("note", "").strip()

    cname = match_chain(raw_chain)
    if not cname:
        return "REJECTED", f"対象外チェーン: '{raw_chain}' はteppay対象店舗に見つかりませんでした。", None

    try:
        lat = float(raw_lat)
        lon = float(raw_lon)
    except (TypeError, ValueError):
        lat, lon = None, None

    if (lat is None or lon is None) and raw_addr:
        geo = geocode_gsi(raw_addr)
        if geo:
            lat, lon = geo

    if lat is None or lon is None:
        return "REJECTED", "位置情報（緯度経度または有効な住所）が指定されていません。", None

    if not (24.0 <= lat <= 46.0 and 122.0 <= lon <= 154.0):
        return "REJECTED", f"日本国内の座標ではありません: ({lat}, {lon})", None

    is_dup, dist, dup_name, dup_file = check_duplicate(cname, lat, lon)
    if is_dup:
        return "REJECTED", f"既に登録済みです（至近 {dist:.0f}m に {cname} {dup_name} が存在）", None

    confidence = "HIGH"
    verification_notes = []

    if raw_addr:
        geo = geocode_gsi(raw_addr)
        if geo:
            geo_dist = haversine_meters(lat, lon, geo[0], geo[1])
            if geo_dist > 3000:
                confidence = "LOW"
                verification_notes.append(f"住所座標と指定ピンに{geo_dist/1000:.1f}kmの乖離")
            elif geo_dist > 800:
                confidence = "MEDIUM"
                verification_notes.append(f"住所座標と指定ピンに{geo_dist:.0f}mのズレ")
            else:
                verification_notes.append(f"住所座標一致({geo_dist:.0f}m以内)")
        else:
            verification_notes.append("住所の直接ジオコーディング未確認")

    clean_name = raw_name
    if not clean_name:
        clean_name = cname
    elif not clean_name.startswith(cname) and not cname in clean_name:
        clean_name = f"{cname} {clean_name}"

    clean_data = {
        "cname": cname,
        "name": clean_name,
        "lat": round(lat, 5),
        "lon": round(lon, 5),
        "target_file": get_target_file(lat, lon)
    }

    if confidence == "HIGH":
        return "APPROVED", f"実在・座標検証OK ({'; '.join(verification_notes) or '直接座標指定'})", clean_data
    elif confidence == "MEDIUM":
        return "NEEDS_REVIEW", f"要確認: {'; '.join(verification_notes)}", clean_data
    else:
        return "REJECTED", f"判定不可: {'; '.join(verification_notes)}", None

def fetch_requests():
    """Fetches requests either via APPS_SCRIPT_URL or gsheets CLI"""
    if APPS_SCRIPT_URL:
        print(f"Fetching requests via Apps Script Web App: {APPS_SCRIPT_URL}")
        try:
            req = urllib.request.Request(APPS_SCRIPT_URL, headers={"User-Agent": "TeppayVerifier/1.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                res = json.loads(r.read().decode("utf-8"))
                if res.get("status") == "success":
                    return "apps_script", res.get("data", [])
        except Exception as e:
            print(f"Error fetching via Apps Script URL: {e}", file=sys.stderr)

    print(f"Fetching requests via gsheets CLI from {SPREADSHEET_ID}...")
    cmd = ["gsheets", "readonly", "read", SPREADSHEET_ID, f"{SHEET_NAME}!A1:J100", "--json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error reading spreadsheet: {res.stderr}", file=sys.stderr)
        return "error", []

    rows = json.loads(res.stdout)
    items = []
    for idx, row in enumerate(rows[1:], start=2):
        while len(row) < 10:
            row.append("")
        items.append({
            "row_index": idx,
            "timestamp": row[0],
            "chain_name": row[1],
            "store_name": row[2],
            "lat": row[3],
            "lon": row[4],
            "address": row[5],
            "note": row[6],
            "status": row[7],
            "verification_log": row[8],
            "processed_at": row[9]
        })
    return "gsheets_cli", items

def update_row_status(mode, row_index, decided_status, reason, now_str):
    if mode == "apps_script" and APPS_SCRIPT_URL:
        try:
            payload = json.dumps({
                "action": "update_status",
                "row_index": row_index,
                "status": decided_status,
                "reason": reason
            }).encode("utf-8")
            req = urllib.request.Request(APPS_SCRIPT_URL, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                pass
            return
        except Exception as e:
            print(f"Error updating row via Apps Script: {e}", file=sys.stderr)

    # Fallback to gsheets CLI
    update_range = f"{SHEET_NAME}!H{row_index}:J{row_index}"
    safe_reason = reason.replace(",", "，")
    val_str = f"{decided_status},{safe_reason},{now_str}"
    subprocess.run(["gsheets", "mutate", "write", SPREADSHEET_ID, update_range, val_str], check=True)

def process_sheet_requests():
    mode, items = fetch_requests()
    if not items:
        print("No request rows found.")
        return 0

    approved_count = 0
    updated_files = set()

    for item in items:
        status = (item.get("status") or "").strip()
        if status not in ("PENDING", ""):
            continue

        row_idx = item["row_index"]
        chain = item.get("chain_name") or ""
        sname = item.get("store_name") or ""
        lat = item.get("lat")
        lon = item.get("lon")

        print(f"\nProcessing Row {row_idx}: {chain} - {sname} ({lat}, {lon})")
        decided_status, reason, clean_data = verify_request(item)
        print(f"  Decision: {decided_status} -> {reason}")

        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        if decided_status == "APPROVED" and clean_data:
            target_fn = clean_data["target_file"]
            cname = clean_data["cname"]
            try:
                with open(target_fn, "r", encoding="utf-8") as f:
                    store_data = json.load(f)

                if cname not in store_data["chains"]:
                    store_data["chains"].append(cname)
                file_cid = store_data["chains"].index(cname)

                store_entry = [file_cid, clean_data["lat"], clean_data["lon"], clean_data["name"]]
                store_data["stores"].append(store_entry)

                with open(target_fn, "w", encoding="utf-8") as f:
                    json.dump(store_data, f, ensure_ascii=False, separators=(",", ":"))

                updated_files.add(target_fn)
                approved_count += 1
                EXISTING_STORES.append((cname, clean_data["lat"], clean_data["lon"], clean_data["name"], target_fn))
                print(f"  -> Successfully added to {target_fn} (cid={file_cid})!")
            except Exception as e:
                print(f"  -> Error appending to {target_fn}: {e}", file=sys.stderr)
                decided_status = "ERROR"
                reason = f"File write error: {e}"

        update_row_status(mode, row_idx, decided_status, reason, now_str)

    print(f"\nFinished. Approved & ingested: {approved_count} stores. Updated files: {list(updated_files)}")
    return approved_count

if __name__ == "__main__":
    count = process_sheet_requests()
    # Output to GitHub Actions environment if running in CI
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
            gh_out.write(f"approved_count={count}\n")
