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

# Non-retail amenity/shop values to ignore (parking lots, post offices, schools, police, hospitals, etc.)
EXCLUDED_AMENITIES = {
    "parking", "parking_entrance", "parking_space", "bicycle_parking", "motorcycle_parking",
    "post_office", "post_box", "police", "fire_station", "hospital", "dentist", "doctors",
    "school", "kindergarten", "university", "college", "place_of_worship", "toilets", "bench",
    "waste_basket", "recycling", "vending_machine", "atm", "bank", "bus_station", "taxi"
}

# Explicit false-positive guards per chain or global
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

# Chains where keywords must be more specific to avoid matching generic words
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
                    # For exact short chain names like "松屋", "ジャパン", avoid matching inside longer compound names unless brand matches
                    if cname == "松屋" and (brand and brand != "松屋" and "松屋" not in brand):
                        continue
                    return cname
    return None

# Bounding box covering Tokyo, Kanagawa, Chiba (+ southern Saitama/Ibaraki metro)
BBOX = (34.85, 138.90, 36.15, 140.95)  # (south, west, north, east)
POI_KEYS = ("shop", "amenity", "leisure", "tourism")

stores_map = {}
names_list = []
name_to_idx = {}

def add_poi(tags, lat, lng):
    if not (BBOX[0] <= lat <= BBOX[2] and BBOX[1] <= lng <= BBOX[3]):
        return
    if not any(k in tags for k in POI_KEYS):
        return
    amenity = tags.get("amenity", "")
    if amenity in EXCLUDED_AMENITIES:
        return
    name = tags.get("name") or tags.get("name:ja") or ""
    brand = tags.get("brand") or tags.get("brand:ja") or ""
    if not name and not brand:
        return
    # Skip parking / station entrances with store names
    if any(w in name for w in ("駐車場", "駐輪場", "銀行ATM", "内郵便局", "交番", "小学校", "中学校", "保育園", "歯科", "クリニック", "病院")):
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
            for ring in a.outer_rings():
                lats = [nd.lat for nd in ring if nd.location.valid()]
                lons = [nd.lon for nd in ring if nd.location.valid()]
                if lats and lons:
                    add_poi(a.tags, sum(lats) / len(lats), sum(lons) / len(lons))
                break
        except Exception:
            pass

if __name__ == "__main__":
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
