#!/usr/bin/env python3
"""
Extract logos from screenshots in /home/antigravity/image*.png
and save cropped square logos to logos/ and mapping to data/logo_map.json.
"""
import glob, os, json, re, hashlib
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(BASE_DIR, "index.html")
OUT_DIR = os.path.join(BASE_DIR, "logos")
MAP_PATH = os.path.join(BASE_DIR, "data", "logo_map.json")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MAP_PATH), exist_ok=True)

html = open(HTML_PATH, encoding="utf-8").read()
chains = json.loads(re.search(r"const CHAINS_DATA\s*=\s*(\[\{.*?\}\]);", html, re.S).group(1))

image_mapping = [
    ("/home/antigravity/image.png", 0, 9),
    ("/home/antigravity/image_2.png", 9, 19),
    ("/home/antigravity/image_3.png", 19, 29),
    ("/home/antigravity/image_4.png", 39, 49),
    ("/home/antigravity/image_5.png", 49, 59),
    ("/home/antigravity/image_6.png", 59, 69),
    ("/home/antigravity/image_7.png", 69, 79),
    ("/home/antigravity/image_8.png", 79, 88),
    ("/home/antigravity/image_9.png", 88, 96),
    ("/home/antigravity/image_10.png", 106, 116),
    ("/home/antigravity/image_11.png", 116, 126),
    ("/home/antigravity/image_12.png", 126, 136),
    ("/home/antigravity/image_13.png", 136, 146),
]

def tight_crop_logo(card):
    bh, bw = card.shape[:2]
    logo_area = card[int(bh * 0.08):int(bh * 0.56), int(bw * 0.08):int(bw * 0.92)].copy()
    lah, law = logo_area.shape[:2]
    logo_area[:int(lah * 0.25), int(law * 0.75):] = [255, 255, 255]
    gray = cv2.cvtColor(logo_area, cv2.COLOR_BGR2GRAY)
    non_white = gray < 248
    if not np.any(non_white):
        return cv2.resize(logo_area, (64, 64))
    ys, xs = np.where(non_white)
    y1, y2 = max(0, ys.min() - 4), min(lah, ys.max() + 5)
    x1, x2 = max(0, xs.min() - 4), min(law, xs.max() + 5)
    cropped = logo_area[y1:y2, x1:x2]
    ch, cw = cropped.shape[:2]
    max_dim = max(ch, cw)
    square = np.full((max_dim, max_dim, 3), 255, dtype=np.uint8)
    oy = (max_dim - ch) // 2
    ox = (max_dim - cw) // 2
    square[oy:oy+ch, ox:ox+cw] = cropped
    return cv2.resize(square, (64, 64), interpolation=cv2.INTER_AREA)

# Preserve existing map if any
logo_map = {}
if os.path.exists(MAP_PATH):
    try:
        logo_map = json.load(open(MAP_PATH, encoding="utf-8"))
    except Exception:
        pass

for img_path, start_idx, end_idx in image_mapping:
    if not os.path.exists(img_path):
        continue
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 248, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cards = []
    for c in contours:
        x, y, bw, bh = cv2.boundingRect(c)
        if 100 < bw < 300 and 100 < bh < 400:
            cards.append((x, y, bw, bh))
    cards.sort(key=lambda r: (r[1] // 50, r[0]))
    expected = end_idx - start_idx
    for c_idx, (x, y, bw, bh) in enumerate(cards[:expected]):
        chain = chains[start_idx + c_idx]
        cname = chain["name"]
        card = img[y:y+bh, x:x+bw]
        logo = tight_crop_logo(card)
        safe_fname = hashlib.md5(cname.encode("utf-8")).hexdigest()[:10] + ".png"
        cv2.imwrite(os.path.join(OUT_DIR, safe_fname), logo)
        logo_map[cname] = f"logos/{safe_fname}"

with open(MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(logo_map, f, ensure_ascii=False, indent=2)

print(f"Extracted logos for {len(logo_map)} chains")
