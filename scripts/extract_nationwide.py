#!/usr/bin/env python3
"""
Nationwide store extractor for teppay-navi.
Generates data/stores_ring3.json (Chugoku, Shikoku, North Tohoku, Hokuriku)
and data/stores_ring4.json (Kyushu, Okinawa, Hokkaido).
Deduplicates against data/stores.json and data/stores_ring2.json.
Downloads each regional PBF, extracts POIs, and deletes the PBF immediately to save disk.
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
import osmium

# 1. Load chains from index.html
html = open("index.html", encoding="utf-8").read()
m = re.search(r"const CHAINS_DATA\s*=\s*(\[\{.*?\}\]);", html, re.S)
if not m:
    raise RuntimeError("CHAINS_DATA not found in index.html")
chains_data = json.loads(m.group(1))

EXCLUDED_AMENITIES = {
    "parking", "parking_entrance", "parking_space", "bicycle_parking", "motorcycle_parking",
    "post_office", "post_box", "police", "fire_station", "hospital", "dentist", "doctors",
    "school", "kindergarten", "university", "college", "place_of_worship", "toilets", "bench",
    "waste_basket", "recycling", "vending_machine", "atm", "bank", "bus_station", "taxi"
}

FALSE_POSITIVE_SUBSTRINGS = {
    "マルエ": ("マルエツ", "マルエイ", "マルエム", "マルエシ", "マルエ醤油"),
    "松屋": ("西松屋", "小松屋", "若松屋", "鶴松屋", "高松屋", "松屋酒店", "松屋菓舗", "松屋珈琲", "松屋精肉"),
    "天下一": ("天下一品",),
    "ダックス": ("シダックス", "マクダックス", "ダックスフンド"),
    "ココス": ("ココストア", "ココスナカムラ", "ココス中村"),
    "コジマ": ("ペットの専門店コジマ", "ペットの専門店 コジマ", "ペットのコジマ", "コジマ動物病院"),
    "洋服の青山": ("青山フラワーマーケット", "青山学院", "青山一丁目", "青山霊園", "南青山", "北青山", "青山病院", "青山歯科", "青山餃子"),
    "イトーヨーカ堂／アリオ": ("アリオン", "ビアリッツ"),
    "イトーヨーカ堂／ポッポ": ("ゆ〜ポッポ", "ポケふた", "ポッポ駅前屋", "ポッポ保育園"),
    "オータニ": ("ニューオータニ", "ホテルオータニ", "ヘアサロンオータニ"),
    "sanwa": ("鶏三和", "三和公園", "三和クリーニング", "三和交通", "三和銀行", "三和シャッター", "三和シヤッター", "三和電気", "三和工業", "三和不動産"),
    "ジャパン": ("パークジャパン", "ジャパンミート", "ジャパンビバレッジ", "ジャパンレンタカー", "ジャパンネット", "ネクステージ", "ロフトジャパン", "ユニバーサル・スタジオ・ジャパン", "オムニバス・ジャパン"),
    "セリア": ("コンセリア", "ピッツェリア", "トラットリア"),
    "ニトリ": ("ニトリ歯科",),
    "アトレ": ("Quatre", "quatre"),
    "atre": ("Quatre", "quatre"),
    "ペリエ": ("モンペリエ", "Crêperie", "Créperie", "Creperie", "creperie"),
    "PERIE": ("モンペリエ", "Crêperie", "Créperie", "Creperie", "creperie"),
}

KEYWORD_OVERRIDES = {
    "マルエ": ["マルエドラッグ", "クスリのマルエ"],
    "洋服の青山": ["洋服の青山"],
    "sanwa": ["スーパー三和", "フードワン"],
    "オータニ": ["フードオアシスオータニ", "スーパーオータニ"],
    "福原": ["フクハラ", "スーパーフクハラ"],
    "ラッキー": ["ラッキーピエロ", "シティマーケット", "ラッキーマート"],
    "ジャパン": ["ドラッグストアジャパン", "スギ薬局ジャパン"],
}

ASCII_WORD_RE_CACHE = {}
def match_ascii_word(kw_lower: str, text_lower: str) -> bool:
    r = ASCII_WORD_RE_CACHE.get(kw_lower)
    if r is None:
        r = re.compile(r"(?<![a-z0-9])" + re.escape(kw_lower) + r"(?![a-z0-9])")
        ASCII_WORD_RE_CACHE[kw_lower] = r
    return bool(r.search(text_lower))

chain_matchers = []
for idx, c in enumerate(chains_data):
    cname = c["name"]
    raw_kws = KEYWORD_OVERRIDES.get(cname, c.get("match_keywords") or [cname])
    kws = []
    for kw in raw_kws:
        kw_l = kw.lower().replace("‐", "-").replace("－", "-").strip()
        if len(kw_l) >= 2:
            is_ascii = all(ord(ch) < 128 for ch in kw_l)
            kws.append((kw_l, is_ascii))
    chain_matchers.append((idx, cname, kws, FALSE_POSITIVE_SUBSTRINGS.get(cname, ())))

def match_chain(name: str, brand: str):
    target = f"{name or ''} {brand or ''}".replace("‐", "-").replace("－", "-").strip()
    if not target:
        return None
    lower = target.lower()
    if "ジョイフル本田" in lower:
        return "ジョイフル本田"
    if "セブン銀行" in lower and "セブン-イレブン" not in lower and "セブンイレブン" not in lower:
        return None
    for idx, cname, kws, fp_Excludes in chain_matchers:
        if any(ex.lower() in lower for ex in fp_Excludes):
            continue
        for kw_l, is_ascii in kws:
            if is_ascii:
                if match_ascii_word(kw_l, lower):
                    return cname
            else:
                if kw_l in lower:
                    if cname == "松屋" and (brand and brand != "松屋" and "松屋" not in brand):
                        continue
                    return cname
    return None

POI_KEYS = ("shop", "amenity", "leisure", "tourism")

# Load existing store coordinates for deduplication
existing_dedup = set()
for fn in ["data/stores.json", "data/stores_ring2.json", "data/stores_ring3.json"]:
    if os.path.exists(fn):
        try:
            d = json.load(open(fn, encoding="utf-8"))
            ch = d["chains"]
            for r in d["stores"]:
                cname = ch[r[0]]
                lat5, lng5 = r[1], r[2]
                key = f"{cname}_{round(lat5 * 1000)}_{round(lng5 * 1000)}"
                existing_dedup.add(key)
        except Exception as e:
            print(f"Warning reading {fn}: {e}", flush=True)

print(f"Loaded {len(existing_dedup)} existing stores for deduplication.", flush=True)

class ExtractionHandler(osmium.SimpleHandler):
    def __init__(self, names_list, name_to_idx, stores_map):
        super().__init__()
        self.names_list = names_list
        self.name_to_idx = name_to_idx
        self.stores_map = stores_map

    def add_poi(self, tags, lat, lng):
        if not any(k in tags for k in POI_KEYS):
            return
        amenity = tags.get("amenity", "")
        if amenity in EXCLUDED_AMENITIES:
            return
        name = tags.get("name") or tags.get("name:ja") or ""
        brand = tags.get("brand") or tags.get("brand:ja") or ""
        if not name and not brand:
            return
        if any(w in name for w in ("駐車場", "駐輪場", "銀行ATM", "内郵便局", "交番", "小学校", "中学校", "保育園", "歯科", "クリニック", "病院")):
            return
        cname = match_chain(name, brand)
        if not cname:
            return
        lat5 = round(lat, 5)
        lng5 = round(lng, 5)
        dedup_key = f"{cname}_{round(lat * 1000)}_{round(lng * 1000)}"
        if dedup_key in existing_dedup or dedup_key in self.stores_map:
            return
        if cname not in self.name_to_idx:
            self.name_to_idx[cname] = len(self.names_list)
            self.names_list.append(cname)
        ci = self.name_to_idx[cname]
        display_name = name or brand or cname
        self.stores_map[dedup_key] = [ci, lat5, lng5, "" if display_name == cname else display_name]

    def node(self, n):
        if len(n.tags) == 0 or not n.location.valid():
            return
        self.add_poi(n.tags, n.location.lat, n.location.lon)

    def area(self, a):
        if len(a.tags) == 0:
            return
        try:
            for ring in a.outer_rings():
                lats = [nd.lat for nd in ring if nd.location.valid()]
                lons = [nd.lon for nd in ring if nd.location.valid()]
                if lats and lons:
                    self.add_poi(a.tags, sum(lats) / len(lats), sum(lons) / len(lons))
                break
        except Exception:
            pass

def process_region(region_name, names_list, name_to_idx, stores_map):
    pbf_path = f"/tmp/{region_name}.osm.pbf"
    url = f"https://download.geofabrik.de/asia/japan/{region_name}-latest.osm.pbf"
    print(f"\n--- Downloading {region_name} PBF ---", flush=True)
    t0 = time.time()
    subprocess.run(["curl", "-fSL", "--retry", "3", "-o", pbf_path, url], check=True)
    size_mb = os.path.getsize(pbf_path) / (1024 * 1024)
    print(f"Downloaded {region_name} ({size_mb:.1f}MB) in {time.time()-t0:.1f}s", flush=True)

    print(f"Scanning {region_name}...", flush=True)
    t1 = time.time()
    handler = ExtractionHandler(names_list, name_to_idx, stores_map)
    handler.apply_file(pbf_path, locations=True)
    print(f"Scanned {region_name} in {time.time()-t1:.1f}s. Total collected: {len(stores_map)}", flush=True)

    try:
        os.remove(pbf_path)
        print(f"Cleaned up {pbf_path}", flush=True)
    except Exception as e:
        print(f"Cleanup error: {e}", flush=True)

def extract_ring(ring_num, regions, out_path):
    print(f"\n==========================================")
    print(f"Starting extraction for Ring {ring_num} -> {out_path}")
    print(f"Regions: {', '.join(regions)}")
    print(f"==========================================")

    names_list = []
    name_to_idx = {}
    stores_map = {}

    for region in regions:
        process_region(region, names_list, name_to_idx, stores_map)

    stores_list = list(stores_map.values())
    print(f"\n[Ring {ring_num} Summary] Matched {len(stores_list)} stores across {len(names_list)} chains.", flush=True)

    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "chains": names_list,
        "stores": stores_list,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Successfully saved to {out_path} ({os.path.getsize(out_path)/1024:.1f} KB)", flush=True)

    # Add to existing dedup for next rings
    for r in stores_list:
        cname = names_list[r[0]]
        key = f"{cname}_{round(r[1] * 1000)}_{round(r[2] * 1000)}"
        existing_dedup.add(key)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if target in ("ring3", "all"):
        # Ring 3: Shikoku, Chugoku, North Tohoku, Hokuriku (Chubu)
        extract_ring(3, ["shikoku", "chugoku", "tohoku", "chubu"], "data/stores_ring3.json")

    if target in ("ring4", "all"):
        # Ring 4: Kyushu/Okinawa, Hokkaido
        extract_ring(4, ["kyushu", "hokkaido"], "data/stores_ring4.json")

    print("\nExtraction complete!", flush=True)
