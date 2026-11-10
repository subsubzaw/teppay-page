import re

with open("index.html", "r", encoding="utf-8") as f:
    c = f.read()

# --------------------------------------------------------------------------
# 1. Update place names / stations to orthodox metropolitan hubs
# --------------------------------------------------------------------------
# Placeholder in input
c = c.replace('placeholder="駅名・地名（例: 新宿, 志津駅, 横浜, 船橋）"',
              'placeholder="駅名・地名（例: 新宿, 渋谷, 横浜, 吉祥寺）"')

# AREA_COORDS map: orthodox metropolitan hubs
old_area_coords = """    const AREA_COORDS = {
      "志津駅": { lat: 35.717455, lng: 140.144992, label: "志津駅周辺" },
      "八千代市": { lat: 35.723722, lng: 140.118437, label: "八千代・村上駅周辺" },
      "武蔵小杉": { lat: 35.576208, lng: 139.659918, label: "武蔵小杉駅周辺" },
      "佐倉市": { lat: 35.709299, lng: 140.226001, label: "佐倉駅周辺" },
      "津田沼駅": { lat: 35.691238, lng: 140.020584, label: "津田沼・船橋周辺" }
    };"""

new_area_coords = """    const AREA_COORDS = {
      "新宿": { lat: 35.690921, lng: 139.700258, label: "新宿駅周辺" },
      "渋谷": { lat: 35.658034, lng: 139.701636, label: "渋谷駅周辺" },
      "東京駅": { lat: 35.681236, lng: 139.767125, label: "東京駅周辺" },
      "池袋": { lat: 35.729503, lng: 139.710900, label: "池袋駅周辺" },
      "横浜": { lat: 35.465786, lng: 139.622713, label: "横浜駅周辺" },
      "大宮": { lat: 35.906295, lng: 139.623999, label: "大宮駅周辺" },
      "船橋": { lat: 35.700346, lng: 139.985587, label: "船橋駅周辺" },
      "吉祥寺": { lat: 35.703117, lng: 139.579765, label: "吉祥寺駅周辺" },
      "武蔵小杉": { lat: 35.576208, lng: 139.659918, label: "武蔵小杉駅周辺" },
      "品川": { lat: 35.628471, lng: 139.738760, label: "品川駅周辺" },
      "川崎": { lat: 35.531311, lng: 139.696884, label: "川崎駅周辺" },
      "立川": { lat: 35.698083, lng: 139.413722, label: "立川駅周辺" }
    };"""

if old_area_coords in c:
    c = c.replace(old_area_coords, new_area_coords)

# AREA_EXPANSIONS in dynamic suggestions
old_area_expansions = """    const AREA_EXPANSIONS = {
      "志津": ["志津駅", "勝田台駅", "ユーカリが丘", "八千代市", "佐倉市"],
      "勝田台": ["勝田台駅", "志津駅", "村上駅", "八千代市"],
      "八千代": ["八千代市", "八千代緑が丘", "八千代中央", "村上駅"],
      "佐倉": ["佐倉市", "京成佐倉", "JR佐倉", "志津駅", "臼井駅"],
      "船橋": ["船橋駅", "西船橋", "津田沼駅", "東船橋", "南船橋"],
      "津田沼": ["津田沼駅", "新津田沼", "船橋駅", "幕張本郷"],
      "新宿": ["新宿駅", "西新宿", "新宿三丁目", "東新宿", "高田馬場"],
      "渋谷": ["渋谷駅", "原宿", "恵比寿", "表参道", "代官山"],
      "池袋": ["池袋駅", "東池袋", "目白", "大塚", "要町"],
      "東京": ["東京駅", "有楽町", "大手町", "日本橋", "八重洲"],
      "品川": ["品川駅", "大崎", "五反田", "大井町"],
      "武蔵小杉": ["武蔵小杉駅", "新丸子", "元住吉", "武蔵中原"],
      "横浜": ["横浜駅", "みなとみらい", "桜木町", "関内"],
      "川崎": ["川崎駅", "京急川崎", "尻手", "鹿島田"],
      "柏": ["柏駅", "南柏", "柏の葉キャンパス", "松戸駅"],
      "松戸": ["松戸駅", "新松戸", "北松戸", "柏駅"],
      "大宮": ["大宮駅", "さいたま新都心", "北大宮", "浦和駅"],
      "浦和": ["浦和駅", "北浦和", "南浦和", "武蔵浦和"]
    };"""

new_area_expansions = """    const AREA_EXPANSIONS = {
      "新宿": ["新宿駅", "西新宿", "新宿三丁目", "東新宿", "高田馬場"],
      "渋谷": ["渋谷駅", "原宿", "恵比寿", "表参道", "代官山"],
      "東京": ["東京駅", "有楽町", "大手町", "日本橋", "八重洲", "銀座"],
      "池袋": ["池袋駅", "東池袋", "目白", "大塚", "要町"],
      "横浜": ["横浜駅", "みなとみらい", "桜木町", "関内", "元町・中華街"],
      "品川": ["品川駅", "大崎", "五反田", "大井町"],
      "吉祥寺": ["吉祥寺駅", "三鷹", "荻窪", "西荻窪"],
      "大宮": ["大宮駅", "さいたま新都心", "浦和駅"],
      "船橋": ["船橋駅", "西船橋", "津田沼駅", "南船橋"],
      "川崎": ["川崎駅", "武蔵小杉", "元住吉", "溝の口"],
      "秋葉原": ["秋葉原駅", "御茶ノ水", "神田", "上野"],
      "立川": ["立川駅", "八王子", "国分寺"],
      "中野": ["中野駅", "高円寺", "阿佐ヶ谷"],
      "柏": ["柏駅", "南柏", "松戸駅"],
      "浦和": ["浦和駅", "北浦和", "南浦和", "大宮駅"]
    };"""

if old_area_expansions in c:
    c = c.replace(old_area_expansions, new_area_expansions)

# Default fallback coordinate when GPS is not available
c = c.replace('return { lat: 35.717455, lng: 140.144992, label: "志津駅周辺（GPS未取得）" };',
              'return { lat: 35.681236, lng: 139.767125, label: "東京駅周辺（GPS未取得）" };')

c = c.replace('const fallbackArea = AREA_COORDS[currentArea] || AREA_COORDS["志津駅"];',
              'const fallbackArea = AREA_COORDS[currentArea] || AREA_COORDS["東京駅"];')

c = c.replace('{ lat: fallbackArea.lat, lng: fallbackArea.lng, label: "志津駅周辺（現在地を取得中...）" }',
              '{ lat: fallbackArea.lat, lng: fallbackArea.lng, label: "東京駅周辺（現在地を取得中...）" }')

# --------------------------------------------------------------------------
# 2. Flat icon & emoji replacements
# --------------------------------------------------------------------------
# Radar panel header title & rescan button
c = c.replace('<span class="radar-title-text">📡 周辺の対象店舗マップ</span>',
              '<span class="radar-title-text">周辺の対象店舗マップ</span>')

c = c.replace('<button type="button" class="btn-sm primary" id="rescan-top-btn">🔄 再検索</button>',
              '<button type="button" class="btn-sm primary" id="rescan-top-btn"><svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="icon-svg"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg><span>再検索</span></button>')

c = c.replace('<button type="button" class="btn-sm" id="rescan-radar-btn">🔄 再スキャン</button>',
              '<button type="button" class="btn-sm" id="rescan-radar-btn"><svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="icon-svg"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg><span>再スキャン</span></button>')

# Preset buttons: remove <span>🗺️</span>
c = c.replace('<span>🗺️</span> マップで探す', 'マップで探す')

# JR station preset icon: remove 🚉
c = c.replace('<span class="preset-icon">🚉</span> JR駅ビル・エキナカ',
              '<div class="preset-icon-badge" style="background:#e0f2fe;color:#0369a1;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="16" rx="2"/><path d="M4 11h16"/><path d="M12 3v8"/><circle cx="8" cy="15" r="1"/><circle cx="16" cy="15" r="1"/><path d="m6 19-2 2"/><path d="m18 19 2 2"/></svg></div> JR駅ビル・エキナカ')

# Search bar icon: flat magnifying glass SVG
c = c.replace('<span class="search-icon">🔍</span>',
              '<span class="search-icon"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>')

# Clear search button: flat cross icon
c = c.replace('<button class="clear-search-btn" id="clear-search-btn">✕</button>',
              '<button class="clear-search-btn" id="clear-search-btn" aria-label="クリア"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>')

# Modal close button: flat cross icon
c = c.replace('<button class="modal-close-btn" id="close-modal-btn">✕</button>',
              '<button class="modal-close-btn" id="close-modal-btn" aria-label="閉じる"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>')

# Checker tab headers & guide headers
c = c.replace('🔍 店名を入力して即時判定', '店名を入力して即時判定')
c = c.replace('<span>📲 iPhoneでホーム画面に追加する方法</span>', '<span>iPhoneでホーム画面に追加する方法</span>')
c = c.replace('<span>💡 teppay決済の基本知識</span>', '<span>teppay決済の基本知識</span>')

# Area suggestion chip: remove 🎯
c = c.replace('proposals.push({ label: "🎯 現在地に戻る", area: "", isGps: true });',
              'proposals.push({ label: "現在地に戻る", area: "", isGps: true });')

# Radar status text: remove ⏳, ⚠️, ⚡
c = c.replace('"⏳ 首都圏外のためライブ検索中（時間がかかる場合があります）..."',
              '"首都圏外のためライブ検索中（時間がかかる場合があります）..."')
c = c.replace('"⚠️ ライブスキャンが混雑しています。下のGoogleマップ一括検索をご利用ください。"',
              '"ライブスキャンが混雑しています。しばらく経ってからお試しください。"')

c = c.replace('`⚡ 表示中の地図内に ${totalCount}件 のteppay対応店舗（地図を動かすと即座に更新）`',
              '`表示中の地図内に ${totalCount}件 のteppay対応店舗（地図を動かすと即座に更新）`')
c = c.replace('`⚡ 半径${radarRadius / 1000}km圏内に ${totalCount}件 のteppay対応店舗が見つかりました`',
              '`半径${radarRadius / 1000}km圏内に ${totalCount}件 のteppay対応店舗が見つかりました`')

# Map popup center pin: remove 📍
c = c.replace('.bindPopup(`<strong>📍 検索中心: ${lastCenterCoords.label}</strong>`)',
              '.bindPopup(`<strong>検索中心: ${lastCenterCoords.label}</strong>`)')

# Distance in store item list: remove 📏
c = c.replace('<span>📏 現在地から約${distText}</span>',
              '<span>現在地から約${distText}</span>')

# Popup & list "Googleマップで開く": replace 📍 with flat arrow
c = c.replace('📍 Googleマップで開く', 'Googleマップで開く →')
c = c.replace('<span>📍</span> Googleマップ', '<span>Googleマップ</span>')

# Empty search results icon in list: flat SVG instead of 🔍
c = c.replace('<div style="font-size: 24px; margin-bottom: 8px;">🔍</div>',
              '<div style="margin-bottom: 8px;"><svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>')

# Chain list action buttons: remove 📍, 📋
c = c.replace('<span>📍</span> マップ', 'マップ')
c = c.replace('<span>📋</span>', 'コピー')

# Checker result card icons: flat checkmark, alert, question SVGs
c = c.replace('resultHeader.innerHTML = `<span>✅</span> 【${chainMatch.name}】はteppay対応です！`;',
              'resultHeader.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#16a34a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="icon-svg" style="margin-right:6px;"><polyline points="20 6 9 17 4 12"/></svg>【${chainMatch.name}】はteppay対応です！`;')

c = c.replace('<span>📍</span> 現在のエリアで「${chainMatch.name}」をマップ検索',
              '現在のエリアで「${chainMatch.name}」をマップ検索')

c = c.replace('resultHeader.innerHTML = `<span>⚠️</span> 【${altMatch.key}】はteppay対象外です`;',
              'resultHeader.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="icon-svg" style="margin-right:6px;"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>【${altMatch.key}】はteppay対象外です`;')

c = c.replace('<span>🗺️</span> 周辺の対応店舗マップを見る', '周辺の対応店舗マップを見る')

c = c.replace('resultHeader.innerHTML = `<span>❓</span> 【${q}】は公式対象シートに未掲載です`;',
              'resultHeader.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#64748b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="icon-svg" style="margin-right:6px;"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>【${q}】は公式対象シートに未掲載です`;')

c = c.replace('<span>🔍</span> 全330チェーン一覧で探す', '全330チェーン一覧で探す')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated index.html: removed emojis & updated personal stations successfully!")
