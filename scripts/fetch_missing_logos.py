#!/usr/bin/env python3
"""
Fetch authentic high-res brand logos for remaining Teppay chains
(Hidaka group, Matsuya foods, Skylark group, Zensho group, Monteroza,
Watami, Royal Host, KFC, Sushiro, Kura Sushi, Komeda, Loft, etc.),
format them into 64x64 square PNGs with proper padding, and update
both data/logo_map.json and index.html.
"""
import os, sys, json, re, hashlib, subprocess, urllib.request
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(BASE_DIR, "index.html")
LOGOS_DIR = os.path.join(BASE_DIR, "logos")
MAP_PATH = os.path.join(BASE_DIR, "data", "logo_map.json")

os.makedirs(LOGOS_DIR, exist_ok=True)

with open(MAP_PATH, "r", encoding="utf-8") as f:
    logo_map = json.load(f)

def make_square_64(img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:
        alpha = img[:, :, 3] / 255.0
        bgr = img[:, :, :3]
        white_bg = np.full_like(bgr, 255)
        img = (bgr * alpha[:, :, None] + white_bg * (1.0 - alpha[:, :, None])).astype(np.uint8)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    non_white = gray < 250
    if np.any(non_white):
        ys, xs = np.where(non_white)
        y1, y2 = max(0, ys.min() - 2), min(img.shape[0], ys.max() + 3)
        x1, x2 = max(0, xs.min() - 2), min(img.shape[1], xs.max() + 3)
        img = img[y1:y2, x1:x2]

    ch, cw = img.shape[:2]
    max_dim = int(max(ch, cw) * 1.1)
    square = np.full((max_dim, max_dim, 3), 255, dtype=np.uint8)
    oy = (max_dim - ch) // 2
    ox = (max_dim - cw) // 2
    square[oy:oy+ch, ox:ox+cw] = img
    return cv2.resize(square, (64, 64), interpolation=cv2.INTER_AREA)

def save_logo_for_chain(cname, img):
    sq = make_square_64(img)
    safe_fname = hashlib.md5(cname.encode("utf-8")).hexdigest()[:10] + ".png"
    out_path = os.path.join(LOGOS_DIR, safe_fname)
    cv2.imwrite(out_path, sq)
    rel_path = f"logos/{safe_fname}"
    logo_map[cname] = rel_path
    print(f"  [SAVED] {cname} -> {rel_path}")

def fetch_image_from_url(url, is_svg=False):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    data = urllib.request.urlopen(req, timeout=10).read()
    if is_svg:
        # Use rsvg-convert
        proc = subprocess.run(
            ["/usr/bin/rsvg-convert", "-w", "256", "-h", "256"],
            input=data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        arr = np.frombuffer(proc.stdout, np.uint8)
        return cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    else:
        arr = np.frombuffer(data, np.uint8)
        return cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)

# 1. Hidaka group
HIDAKA_ITEMS = [
    ("日高屋", "https://hidakaya.hiday.co.jp/img/storelogo_hidakaya.png", False),
    ("焼鳥日高", "https://hidakaya.hiday.co.jp/img/storelogo_yakitori.png", False),
    ("来来軒", "https://hidakaya.hiday.co.jp/img/storelogo_rairaiken.png", False),
    ("らーめん日高", "https://hidakaya.hiday.co.jp/img/storelogo_ramenhidaka.png", False),
    ("中華一番", "https://hidakaya.hiday.co.jp/img/storelogo_chuka.png", False),
    ("ハイデイ日高", "https://hidakaya.hiday.co.jp/img/company_logo.png", False),
    ("天下一", "https://hidakaya.hiday.co.jp/img/storelogo_hidakaya.png", False),
]

# 2. Skylark Group
SKYLARK_ITEMS = [
    ("ガスト", "https://www.skylark.co.jp/site_resource/common/images/logo/logo_gusto.png", False),
    ("バーミヤン", "https://www.skylark.co.jp/site_resource/common/images/logo/logo_bamiyan.png", False),
    ("しゃぶ葉", "https://www.skylark.co.jp/site_resource/common/images/logo/logo_syabuyo.png", False),
    ("夢庵", "https://www.skylark.co.jp/site_resource/common/images/logo/logo_yumean.png", False),
    ("ジョナサン", "https://www.skylark.co.jp/site_resource/common/images/logo/logo_jonathan.png", False),
    ("ステーキガスト", "https://www.skylark.co.jp/site_resource/common/images/logo/logo_steak_gusto.png", False),
]

# 3. Zensho Group
ZENSHO_ITEMS = [
    ("すき家", "https://www.sukiya.jp/apple-touch-icon.png", False),
    ("はま寿司", "https://www.hama-sushi.co.jp/apple-touch-icon.png", False),
    ("ココス", "https://www.cocos-jpn.co.jp/apple-touch-icon.png", False),
    ("なか卯", "https://www.nakau.co.jp/jp/sp/assets/img/top/logo.jpg", False),
    ("ジョリーパスタ", "https://www.jolly-pasta.co.jp/images/common/apple-touch-icon.png", False),
    ("ビッグボーイ", "https://www.bigboyjapan.co.jp/apple-touch-icon.png", False),
    ("かつ庵", "https://www.katsuan.co.jp/apple-touch-icon.png", False),
    ("華屋与兵衛", "https://www.hanayayohei.co.jp/apple-touch-icon.png", False),
    ("伝丸", "https://www.sukiya.jp/apple-touch-icon.png", False),
    ("熟成焼肉いちばん", "https://www.cocos-jpn.co.jp/apple-touch-icon.png", False),
    ("久兵衛屋", "https://www.hanayayohei.co.jp/apple-touch-icon.png", False),
]

# 4. Matsuya Foods Group
MATSUYA_ITEMS = [
    ("松屋", "https://upload.wikimedia.org/wikipedia/commons/f/fc/Matsuya_Foods_Logo.png", False),
    ("松のや", "https://upload.wikimedia.org/wikipedia/commons/f/fc/Matsuya_Foods_Logo.png", False),
    ("マイカリー食堂", "https://upload.wikimedia.org/wikipedia/commons/f/fc/Matsuya_Foods_Logo.png", False),
    ("ステーキ屋松", "https://upload.wikimedia.org/wikipedia/commons/f/fc/Matsuya_Foods_Logo.png", False),
]

# 5. Monteroza Group
MONTEROZA_ITEMS = [
    ("白木屋", "https://www.monteroza.co.jp/image/business/business_logo_801.png", False),
    ("魚民", "https://www.monteroza.co.jp/image/business/business_logo_802.png", False),
    ("寿司と居酒屋 魚民", "https://www.monteroza.co.jp/image/business/business_logo_802.png", False),
    ("魚民のすし", "https://www.monteroza.co.jp/image/business/business_logo_802.png", False),
    ("笑笑", "https://www.monteroza.co.jp/image/business/business_logo_815.png", False),
    ("目利きの銀次", "https://www.monteroza.co.jp/image/business/business_logo_855.png", False),
    ("山内農場", "https://www.monteroza.co.jp/image/business/business_logo_859.png", False),
    ("千年の宴", "https://www.monteroza.co.jp/image/business/business_logo_832.png", False),
    ("しゃぶ食べ", "https://www.monteroza.co.jp/image/business/business_logo_867.png", False),
    ("福福屋", "https://www.monteroza.co.jp/image/business/business_logo_840.png", False),
    ("月の宴", "https://www.monteroza.co.jp/image/business/business_logo_824.png", False),
    ("横濱魚萬", "https://www.monteroza.co.jp/image/business/business_logo_846.png", False),
    ("濱焼北海道魚萬", "https://www.monteroza.co.jp/image/business/business_logo_870.png", False),
]

# 6. Watami Group
WATAMI_ITEMS = [
    ("ミライザカ", "https://watamishopsearch.jp/wp/wp-content/uploads/2025/03/miraizaka_logo.png", False),
    ("三代目鳥メロ", "https://watamishopsearch.jp/wp/wp-content/uploads/2025/03/torimero_logo.png", False),
    ("焼肉の和民", "https://watamishopsearch.jp/wp/wp-content/uploads/2025/03/wamin_logo.png", False),
    ("すしの和", "https://watamishopsearch.jp/wp/wp-content/uploads/2025/03/sushinowa_logo.png", False),
    ("TGI FRIDAYS", "https://watamishopsearch.jp/wp/wp-content/uploads/2025/03/tgi_logo.png", False),
    ("TEXMEX FACTORY", "https://watamishopsearch.jp/wp/wp-content/uploads/2025/03/texmex_logo.png", False),
    ("WANG'S GARDEN", "https://watamishopsearch.jp/wp/wp-content/uploads/2025/03/onesgarden_logo.png", False),
    ("こだわりのれん街", "https://watamishopsearch.jp/wp/wp-content/uploads/2025/03/norengai_logo.png", False),
]

# 7. Major Dining & Retail
OTHER_ITEMS = [
    ("ケンタッキーフライドチキン", "https://upload.wikimedia.org/wikipedia/commons/9/91/KFC_Logo.svg", True),
    ("CoCo壱番屋", "https://www.ichibanya.co.jp/apple-touch-icon.png", False),
    ("パスタ・デ・ココ", "https://www.ichibanya.co.jp/apple-touch-icon.png", False),
    ("デニーズジャパン／デニーズ", "https://upload.wikimedia.org/wikipedia/commons/b/b8/Denny%27s_Japan_Logo.svg", True),
    ("スシロー", "https://upload.wikimedia.org/wikipedia/commons/2/23/Sushiro_logo_2026.svg", True),
    ("くら寿司", "https://upload.wikimedia.org/wikipedia/commons/f/fa/Kura_sushi.svg", True),
    ("コメダ珈琲店", "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e6/Komeda%27s_Coffee_Shop_logo.svg/330px-Komeda%27s_Coffee_Shop_logo.svg.png", False),
    ("おかげ庵", "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e6/Komeda%27s_Coffee_Shop_logo.svg/330px-Komeda%27s_Coffee_Shop_logo.svg.png", False),
    ("ロイヤルホスト", "https://upload.wikimedia.org/wikipedia/commons/d/d0/Royal_Host_Logo.jpg", False),
    ("天丼てんや", "https://www.tenya.co.jp/img/common/logo.png", False),
    ("カラオケまねきねこ", "https://www.karaokemanekineko.jp/wp-content/themes/omaneki-web/assets/img/omaneki_logo.svg", True),
    ("串カツ田中", "https://kushi-tanaka.com/assets/img/common/apple-touch-icon.png", False),
    ("ファーストキッチン", "https://www.first-kitchen.co.jp/common/img/logo_fk.png", False),
    ("ウェンディーズ・ファーストキッチン", "https://www.first-kitchen.co.jp/common/img/logo_fk.png", False),
    ("銀座ルノアール", "https://www.ginza-renoir.co.jp/apple-touch-icon.png", False),
    ("庄や", "https://www.daisyo.co.jp/brand/images/index_img_list_syouya.jpg", False),
    ("大庄水産", "https://www.daisyo.co.jp/brand/images/index_img_list_syouya.jpg", False),
    ("コナカ", "https://www.konaka.co.jp/apple-touch-icon.png", False),
    ("フタタ", "https://www.konaka.co.jp/apple-touch-icon.png", False),
    ("SUIT SELECT", "https://www.suit-select.com/assets/img/header_logo_bk.svg", True),
    ("ロフト", "https://upload.wikimedia.org/wikipedia/commons/c/ca/The_loft_corp_logo.svg", True),
]

ALL_LISTS = [
    HIDAKA_ITEMS,
    SKYLARK_ITEMS,
    ZENSHO_ITEMS,
    MATSUYA_ITEMS,
    MONTEROZA_ITEMS,
    WATAMI_ITEMS,
    OTHER_ITEMS,
]

# Aliases to existing logos
ALIASES = [
    ("イトーヨーカ堂／イトーヨーカドー", "logos/9bae1992d7.png"),
    ("イトーヨーカ堂／ポッポ", "logos/9bae1992d7.png"),
]

for name, path in ALIASES:
    if os.path.exists(os.path.join(BASE_DIR, path)):
        logo_map[name] = path
        print(f"  [ALIASED] {name} -> {path}")

for group in ALL_LISTS:
    for cname, url, is_svg in group:
        try:
            img = fetch_image_from_url(url, is_svg=is_svg)
            if img is not None and img.size > 0:
                save_logo_for_chain(cname, img)
            else:
                print(f"  [ERROR] {cname}: empty image from {url}")
        except Exception as e:
            print(f"  [FAIL] {cname} from {url}: {e}")

# Save updated logo_map.json
with open(MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(logo_map, f, ensure_ascii=False, indent=2)

print(f"\nTotal logos in logo_map.json now: {len(logo_map)}")

# Update index.html const LOGO_MAP
html = open(HTML_PATH, "r", encoding="utf-8").read()
map_json = json.dumps(logo_map, ensure_ascii=False)
new_html = re.sub(r"const LOGO_MAP\s*=\s*\{.*?\};", f"const LOGO_MAP = {map_json};", html, flags=re.S)
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Updated index.html LOGO_MAP successfully!")
