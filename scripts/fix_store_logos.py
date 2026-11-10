#!/usr/bin/env python3
"""
Fix mismatched store logos and purge bogus JR East cropped logos from other categories.
"""
import os, sys, json, re, hashlib, subprocess
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(BASE_DIR, "index.html")
LOGOS_DIR = os.path.join(BASE_DIR, "logos")
MAP_PATH = os.path.join(BASE_DIR, "data", "logo_map.json")

os.makedirs(LOGOS_DIR, exist_ok=True)

with open(MAP_PATH, "r", encoding="utf-8") as f:
    logo_map = json.load(f)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

chains = json.loads(re.search(r"const CHAINS_DATA\s*=\s*(\[\{.*?\}\]);", html, re.S).group(1))

def get_commons_url(filename):
    fn = filename.replace(" ", "_")
    m = hashlib.md5(fn.encode("utf-8")).hexdigest()
    return f"https://upload.wikimedia.org/wikipedia/commons/{m[0]}/{m[0:2]}/{fn}"

# List of authentic brand definitions: (chain_names, commons_filename_or_url, is_svg)
AUTHENTIC_DEFINITIONS = [
    # Convenience
    (["セブン‐イレブン"], "7-eleven_logo.svg", True),
    (["ローソン", "ナチュラルローソン", "ローソンストア100"], "Lawson.svg", True),
    (["ファミリーマート"], "FamilyMart_Logo_(2016-).svg", True),
    (["ミニストップ"], "Ministop_logo.svg", True),
    (["デイリーヤマザキ"], "Daily_yamazaki_logo.svg", True),
    (["ポプラ"], "Poplar_convenience_store_logo.svg", True),

    # Drugstores
    (["ウエルシア薬局"], "Welcia_Holdings_logo.svg", True),
    (["スギ薬局", "スギドラッグ"], "Sugi_Pharmacy_Logo.png", False),
    (["トモズ"], "Tomod's_logo.svg", True),

    # Supermarkets & Home Centers
    (["イトーヨーカ堂／イトーヨーカドー"], "Ito-Yokado_logo.svg", True),
    (["ヨーク／ヨークマート", "ヨーク／ヨークフーズ", "ヨーク／ヨークプライス", "ヨーク／コンフォートマーケット", "ヨークベニマル"], "Seven_&_i_Holdings_Logo.svg", True),
    (["オーケー"], "OK_Store_logo.svg", True),
    (["成城石井"], "Seijo_Ishii_logo.svg", True),
    (["コーナン"], "Kohnan_Shoji_logo.svg", True),
    (["コメリ"], "Komeri_logo.svg", True),
    (["ビバホーム", "ビバホームプロ"], "Viva_Home_logo.svg", True),
    (["島忠ホームズ"], "Shimachu_logo.svg", True),

    # Electronics
    (["ノジマ"], "Nojima_logo2.svg", True),
    (["ビックカメラ"], "Bic_Camera_Logo.svg", True),
    (["ヤマダデンキ"], "Yamada_Denki_Logo.svg", True),
    (["ケーズデンキ"], "K's_Holdings_logo.svg", True),
    (["エディオン"], "Edion_logo.svg", True),
    (["コジマ"], "Kojima_logo.svg", True),
    (["ソフマップ"], "Sofmap_logo.svg", True),

    # Books
    (["TSUTAYA", "TSUTAYA BOOKSTORE", "蔦屋書店"], "TSUTAYA_logo.svg", True),
    (["丸善"], "Maruzen_logo.svg", True),
    (["ジュンク堂書店"], "Junkudo_logo.svg", True),
]

def make_square_64(img_path, out_path):
    img = Image.open(img_path).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    w, h = img.size
    max_d = int(max(w, h) * 1.15)
    square = Image.new("RGBA", (max_d, max_d), (255, 255, 255, 255))
    offset = ((max_d - w) // 2, (max_d - h) // 2)
    square.paste(img, offset, mask=img.split()[3])
    final_img = square.resize((64, 64), Image.Resampling.LANCZOS)
    final_img.save(out_path, format="PNG")

# 1. Download and convert each authentic logo
authentic_chains_all = set()
updated_reports = []

for c_names, fn_or_url, is_svg in AUTHENTIC_DEFINITIONS:
    url = fn_or_url if fn_or_url.startswith("http") else get_commons_url(fn_or_url)
    temp_dl = "/tmp/dl_temp"
    png_src = "/tmp/png_temp.png"
    try:
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", url, "-o", temp_dl], check=True, timeout=15)
        if is_svg:
            subprocess.run(["rsvg-convert", "-w", "256", "-h", "256", temp_dl, "-o", png_src], check=True)
        else:
            png_src = temp_dl

        for cname in c_names:
            authentic_chains_all.add(cname)
            safe_fname = hashlib.md5(cname.encode("utf-8")).hexdigest()[:10] + ".png"
            out_path = os.path.join(LOGOS_DIR, safe_fname)
            make_square_64(png_src, out_path)
            rel_path = f"logos/{safe_fname}"
            old_val = logo_map.get(cname)
            logo_map[cname] = rel_path
            updated_reports.append((cname, old_val, rel_path))
            print(f"AUTHENTIC LOGO SAVED: {cname} -> {rel_path} (previous: {old_val})")
    except Exception as e:
        print(f"ERROR downloading/converting {fn_or_url} for {c_names}: {e}")

# 2. Purge suspect categories' remaining bogus JR East cropped mappings
suspect_categories = {"コンビニエンスストア", "ドラッグストア・薬局", "スーパーマーケット・ホームセンター", "家電", "本", "服飾"}
keep_chains = authentic_chains_all.union({"コナカ", "フタタ", "SUIT SELECT"})

purged = []
for c in chains:
    name = c["name"]
    cat = c.get("category")
    if cat in suspect_categories and name in logo_map and name not in keep_chains:
        old_val = logo_map[name]
        del logo_map[name]
        purged.append((name, cat, old_val))

print(f"\nTotal authentic logos added/updated: {len(updated_reports)}")
print(f"Total bogus mappings purged: {len(purged)}")

# 3. Save updated data/logo_map.json
with open(MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(logo_map, f, ensure_ascii=False, indent=2)

# 4. Update LOGO_MAP in index.html
new_json_str = json.dumps(logo_map, ensure_ascii=False)
html = re.sub(r"const LOGO_MAP\s*=\s*\{.*?\};", f"const LOGO_MAP = {new_json_str};", html, flags=re.S)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Done updating index.html!")
