import re

with open("index.html", "r", encoding="utf-8") as f:
    c = f.read()

# --------------------------------------------------------------------------
# 1. Unify Teppay -> teppay and teppayナビ in head / metadata
# --------------------------------------------------------------------------
c = c.replace('<meta name="apple-mobile-web-app-title" content="Teppayナビ">',
              '<meta name="apple-mobile-web-app-title" content="teppayナビ">\n  <link rel="manifest" href="manifest.json">')
c = c.replace('<title>Teppayナビ - Teppay対応店舗 & Googleマップ検索</title>',
              '<title>teppayナビ - teppay対応店舗 & Googleマップ検索</title>')

# Update favicon and apple-touch-icon with flat stadium railway emblem
old_fav = """  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2228%22 fill=%22%2300beb7%22/><text x=%2250%22 y=%2266%22 font-size=%2254%22 text-anchor=%22middle%22 fill=%22white%22 font-weight=%22900%22 font-family=%22sans-serif%22>t</text></svg>">
  <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2228%22 fill=%22%2300beb7%22/><text x=%2250%22 y=%2266%22 font-size=%2254%22 text-anchor=%22middle%22 fill=%22white%22 font-weight=%22900%22 font-family=%22sans-serif%22>t</text></svg>">"""

new_fav = """  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2228%22 fill=%22%2300beb7%22/><rect x=%2212%22 y=%2226%22 width=%2276%22 height=%2248%22 rx=%2224%22 fill=%22%23ffffff%22/><rect x=%2216%22 y=%2230%22 width=%2268%22 height=%2240%22 rx=%2220%22 fill=%22none%22 stroke=%22%23283548%22 stroke-width=%223%22 stroke-dasharray=%224,5%22/><text x=%2250%22 y=%2256%22 font-family=%22sans-serif%22 font-size=%2220%22 font-weight=%22900%22 fill=%22%23283548%22 text-anchor=%22middle%22>teppay</text></svg>">
  <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2228%22 fill=%22%2300beb7%22/><rect x=%2212%22 y=%2226%22 width=%2276%22 height=%2248%22 rx=%2224%22 fill=%22%23ffffff%22/><rect x=%2216%22 y=%2230%22 width=%2268%22 height=%2240%22 rx=%2220%22 fill=%22none%22 stroke=%22%23283548%22 stroke-width=%223%22 stroke-dasharray=%224,5%22/><text x=%2250%22 y=%2256%22 font-family=%22sans-serif%22 font-size=%2220%22 font-weight=%22900%22 fill=%22%23283548%22 text-anchor=%22middle%22>teppay</text></svg>">"""

if old_fav in c:
    c = c.replace(old_fav, new_fav)

# --------------------------------------------------------------------------
# 2. Add flat icon styling in CSS
# --------------------------------------------------------------------------
extra_css = """    /* Flat SVG Icons */
    .icon-svg {
      display: inline-block;
      vertical-align: middle;
      flex-shrink: 0;
    }
    .nav-icon-svg {
      width: 22px;
      height: 22px;
      stroke: currentColor;
      fill: none;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
      transition: all 0.2s;
    }
    .nav-item.active .nav-icon-svg {
      stroke: var(--primary-dark);
      transform: translateY(-1px);
    }
    .preset-icon-badge {
      width: 32px;
      height: 32px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .preset-icon-badge svg {
      width: 18px;
      height: 18px;
    }
    .chips-label-note {
      font-size: 10px;
      color: var(--text-muted);
      margin-left: 4px;
      font-weight: 500;
    }
"""

c = c.replace("    .toast {", extra_css + "    .toast {")

# --------------------------------------------------------------------------
# 3. Header button: "ホーム追加" -> "ホーム画面に追加" with flat SVG icon
# --------------------------------------------------------------------------
old_header_btn = """      <button class="header-btn" id="open-install-guide-btn">
        <span>📲</span> ホーム追加
      </button>"""

new_header_btn = """      <button class="header-btn" id="open-install-guide-btn">
        <svg class="icon-svg" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="3"/><path d="M12 18h.01"/><path d="M12 7v6M9.5 10.5 12 13l2.5-2.5"/></svg>
        <span>ホーム画面に追加</span>
      </button>"""

if old_header_btn in c:
    c = c.replace(old_header_btn, new_header_btn)

# --------------------------------------------------------------------------
# 4. Hero Banner Catchphrase replacement
# --------------------------------------------------------------------------
old_hero_banner = """  <!-- Hero Brand Banner matching image.png -->
  <div class="hero-brand-banner">
    <div class="hero-brand-inner">
      <div class="hero-brand-top">
        <span class="hero-yellow-badge">全330チェーン対応！</span>
        <span class="hero-pink-badge">Googleマップ即時連携</span>
      </div>
      <h2 class="hero-brand-title">じゃ、こっちの<span>pay</span>で<br>よくない？</h2>
      <p class="hero-brand-desc">今いる場所からTeppay対応店舗を瞬時にスキャン &amp; ワンタップでルート案内</p>
    </div>
  </div>"""

new_hero_banner = """  <!-- Hero Brand Banner -->
  <div class="hero-brand-banner">
    <div class="hero-brand-inner">
      <div class="hero-brand-top">
        <span class="hero-yellow-badge">全330チェーン対応</span>
        <span class="hero-pink-badge">Googleマップ連携</span>
      </div>
      <h2 class="hero-brand-title">今いる場所から<span>teppay</span>対応店舗を<br>瞬時にチェック</h2>
    </div>
  </div>"""

if old_hero_banner in c:
    c = c.replace(old_hero_banner, new_hero_banner)

# --------------------------------------------------------------------------
# 5. Area Bar buttons (flat icons) & Area candidate chips (hidden by default)
# --------------------------------------------------------------------------
old_area_bar = """  <!-- Global Area Context Bar -->
  <div class="area-bar">
    <div class="area-status-row">
      <div class="area-label">
        <span>📍 検索エリア:</span>
        <span class="current-area-badge" id="current-area-display">現在地付近</span>
      </div>
      <div class="area-actions">
        <button class="btn-sm primary" id="gps-btn">
          <span>🎯</span> 現在地
        </button>
        <button class="btn-sm" id="toggle-area-input-btn">
          <span>✏️</span> 変更
        </button>
      </div>
    </div>
    <div class="area-input-panel" id="area-input-panel">
      <div class="area-input-group">
        <input type="text" id="custom-area-input" placeholder="駅名・地名（例: 志津駅, 武蔵小杉, 勝田台）">
        <button class="btn-sm primary" id="apply-area-btn">適用</button>
      </div>
    </div>
    <div class="chips-scroll">
      <button class="chip active" data-area="">現在地</button>
      <button class="chip" data-area="志津駅">志津・勝田台</button>
      <button class="chip" data-area="八千代市">八千代・村上</button>
      <button class="chip" data-area="武蔵小杉">武蔵小杉</button>
      <button class="chip" data-area="佐倉市">佐倉市</button>
      <button class="chip" data-area="津田沼駅">津田沼・船橋</button>
    </div>
  </div>"""

new_area_bar = """  <!-- Global Area Context Bar -->
  <div class="area-bar">
    <div class="area-status-row">
      <div class="area-label">
        <svg class="icon-svg" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#00beb7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="10" r="3"/><path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"/></svg>
        <span>検索エリア:</span>
        <span class="current-area-badge" id="current-area-display">現在地付近</span>
      </div>
      <div class="area-actions">
        <button class="btn-sm primary" id="gps-btn">
          <svg class="icon-svg" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/><line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg>
          <span>現在地</span>
        </button>
        <button class="btn-sm" id="toggle-area-input-btn">
          <svg class="icon-svg" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
          <span>変更</span>
        </button>
      </div>
    </div>
    <div class="area-input-panel" id="area-input-panel">
      <div class="area-input-group">
        <input type="text" id="custom-area-input" placeholder="駅名・地名（例: 新宿, 志津駅, 横浜, 船橋）">
        <button class="btn-sm primary" id="apply-area-btn">適用</button>
      </div>
    </div>
    <!-- Area suggestions: hidden by default, shown based on searched content -->
    <div class="chips-scroll" id="chips-scroll" style="display: none;"></div>
  </div>"""

if old_area_bar in c:
    c = c.replace(old_area_bar, new_area_bar)

# --------------------------------------------------------------------------
# 6. Remove "Googleマップアプリで主要チェーンを一括検索" section
# --------------------------------------------------------------------------
old_gmap_section = """        <div style="border-top: 1px dashed var(--border); padding-top: 10px; margin-top: 6px;">
          <button type="button" class="action-btn map" style="width: 100%; justify-content: center; padding: 11px 16px; font-size: 13px; font-weight: 800; background: linear-gradient(135deg, #00beb7 0%, #009e97 100%); color: #ffffff; border: none; box-shadow: 0 4px 12px rgba(0, 190, 183, 0.35);" id="open-gmaps-all-major-btn">
            <span>🚀</span> Googleマップアプリで主要チェーンを一括検索
          </button>
          <div style="font-size: 10px; color: var(--text-muted); margin-top: 5px; line-height: 1.4;">
            ※Googleマップの検索窓は文字数・単語数上限（約32語）があるため330チェーンすべてのOR検索はできません。上のアプリ内マップで全330チェーンを一括ピン表示し、Googleマップ側には主要16チェーンを一括送信します。
          </div>
        </div>"""

if old_gmap_section in c:
    c = c.replace(old_gmap_section, "")

# Remove JS listener for open-gmaps-all-major-btn
c = re.sub(r'document\.getElementById\("open-gmaps-all-major-btn"\)\.addEventListener\("click",\s*\(\)\s*=>\s*\{.*?\}\);\n*', '', c, flags=re.DOTALL)

# --------------------------------------------------------------------------
# 7. Presets flat icons
# --------------------------------------------------------------------------
preset_icons = {
    '🔨': '<div class="preset-icon-badge" style="background:#fef3c7;color:#d97706;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></div>',
    '🏪': '<div class="preset-icon-badge" style="background:#e0f2fe;color:#0284c7;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></div>',
    '💊': '<div class="preset-icon-badge" style="background:#fce7f3;color:#db2777;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg></div>',
    '🛒': '<div class="preset-icon-badge" style="background:#e6faf7;color:#00968f;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg></div>',
    '🍽️': '<div class="preset-icon-badge" style="background:#ffedd5;color:#ea580c;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2v6a3 3 0 0 1-3 3 3 3 0 0 1-3-3V2"/><path d="M15 11v11"/><path d="M6 2v20"/><path d="M6 7h4a2 2 0 0 0 2-2V2"/></svg></div>',
    '☕': '<div class="preset-icon-badge" style="background:#fef3c7;color:#b45309;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg></div>',
    '⚡': '<div class="preset-icon-badge" style="background:#fef9c3;color:#ca8a04;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>',
    '🚆': '<div class="preset-icon-badge" style="background:#e0f2fe;color:#0369a1;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="16" rx="2"/><path d="M4 11h16"/><path d="M12 3v8"/><circle cx="8" cy="15" r="1"/><circle cx="16" cy="15" r="1"/><path d="m6 19-2 2"/><path d="m18 19 2 2"/></svg></div>',
    '🎤': '<div class="preset-icon-badge" style="background:#ede9fe;color:#7c3aed;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="22"/></svg></div>'
}

for emoji, svg_badge in preset_icons.items():
    old_tag = f'<span class="preset-icon">{emoji}</span>'
    c = c.replace(old_tag, svg_badge)

# --------------------------------------------------------------------------
# 8. Bottom Navigation Flat SVG Icons
# --------------------------------------------------------------------------
old_bottom_nav = """  <!-- Bottom Navigation -->
  <nav class="nav-bar">
    <button class="nav-item active" data-tab="tab-quick">
      <span class="nav-icon">📍</span>
      <span>周辺マップ</span>
    </button>
    <button class="nav-item" data-tab="tab-list">
      <span class="nav-icon">🔍</span>
      <span>チェーン一覧</span>
    </button>
    <button class="nav-item" data-tab="tab-checker">
      <span class="nav-icon">❓</span>
      <span>使える？判定</span>
    </button>
    <button class="nav-item" data-tab="tab-guide">
      <span class="nav-icon">📖</span>
      <span>ガイド</span>
    </button>
  </nav>"""

new_bottom_nav = """  <!-- Bottom Navigation with Flat SVG Icons -->
  <nav class="nav-bar">
    <button class="nav-item active" data-tab="tab-quick">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><circle cx="12" cy="10" r="3"/><path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"/></svg>
      <span>周辺マップ</span>
    </button>
    <button class="nav-item" data-tab="tab-list">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h7"/><circle cx="17" cy="17" r="3"/><path d="m21 21-1.5-1.5"/></svg>
      <span>チェーン一覧</span>
    </button>
    <button class="nav-item" data-tab="tab-checker">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
      <span>使える？判定</span>
    </button>
    <button class="nav-item" data-tab="tab-guide">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
      <span>ガイド</span>
    </button>
  </nav>"""

if old_bottom_nav in c:
    c = c.replace(old_bottom_nav, new_bottom_nav)

# --------------------------------------------------------------------------
# 9. Install Modal: Android PWA + iOS Support
# --------------------------------------------------------------------------
old_modal = """  <!-- Install Modal -->
  <div class="modal-overlay" id="install-modal">
    <div class="modal-content">
      <div class="modal-header">
        <h3 style="font-size: 16px;">📲 ホーム画面への追加手順</h3>
        <button class="modal-close-btn" id="close-modal-btn">✕</button>
      </div>
      <div style="font-size: 13px; line-height: 1.6; color: #334155;">
        <p style="margin-bottom: 12px;">
          このHTMLファイルをホーム画面に追加すると、アドレスバーのないフルスクリーンアプリとして快適にご利用いただけます。
        </p>
        <div style="background: #f8fafc; border-radius: 8px; padding: 12px; margin-bottom: 12px; border: 1px solid #e2e8f0;">
          <strong>【iPhone Safariの場合】</strong>
          <ol style="margin-left: 20px; margin-top: 6px;">
            <li>画面下中央の共有ボタン（四角から上向き矢印）をタップ</li>
            <li>メニューをスクロールして「ホーム画面に追加」をタップ</li>
            <li>右上の「追加」をタップ</li>
          </ol>
        </div>
        <div style="background: #f8fafc; border-radius: 8px; padding: 12px; border: 1px solid #e2e8f0;">
          <strong>【iPhone Chromeの場合】</strong>
          <ol style="margin-left: 20px; margin-top: 6px;">
            <li>アドレスバー右側の共有アイコンまたは右下のメニュー（…）をタップ</li>
            <li>「ホーム画面に追加」または「共有...」→「ホーム画面に追加」を選択</li>
            <li>「追加」をタップ</li>
          </ol>
        </div>
      </div>
    </div>
  </div>"""

new_modal = """  <!-- Install Modal with Android & iOS Support -->
  <div class="modal-overlay" id="install-modal">
    <div class="modal-content">
      <div class="modal-header">
        <div style="font-size: 16px; font-weight: 800; color: var(--primary-dark); display: flex; align-items: center; gap: 8px;">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="3"/><path d="M12 18h.01"/><path d="M12 7v6M9.5 10.5 12 13l2.5-2.5"/></svg>
          <span>ホーム画面に追加</span>
        </div>
        <button class="modal-close-btn" id="close-modal-btn">✕</button>
      </div>
      <div style="font-size: 13px; line-height: 1.6; color: var(--text);">
        <p style="margin-bottom: 14px;">
          ホーム画面に追加すると、アドレスバーのないフルスクリーンアプリとして快適にワンタップ起動できます。
        </p>
        <div style="background: var(--primary-ultra-light); border-radius: 14px; padding: 14px; margin-bottom: 12px; border: 1.5px solid var(--border);">
          <strong style="color: var(--primary-dark);">【Android (Chrome等) の場合】</strong>
          <ol style="margin-left: 20px; margin-top: 6px;">
            <li>画面右上のメニュー（<strong>⋮</strong>）をタップ</li>
            <li><strong>「アプリをインストール」</strong>または<strong>「ホーム画面に追加」</strong>をタップ</li>
            <li>確認ダイアログで「インストール」を選択</li>
          </ol>
        </div>
        <div style="background: var(--primary-ultra-light); border-radius: 14px; padding: 14px; margin-bottom: 12px; border: 1.5px solid var(--border);">
          <strong style="color: var(--primary-dark);">【iPhone (Safari) の場合】</strong>
          <ol style="margin-left: 20px; margin-top: 6px;">
            <li>画面下中央の<strong>共有アイコン</strong>（四角から上向き矢印）をタップ</li>
            <li>メニューから<strong>「ホーム画面に追加」</strong>をタップ</li>
            <li>右上の「追加」をタップ</li>
          </ol>
        </div>
      </div>
    </div>
  </div>"""

if old_modal in c:
    c = c.replace(old_modal, new_modal)

# --------------------------------------------------------------------------
# 10. Unify all Teppay -> teppay and teppayナビ across text content
# --------------------------------------------------------------------------
# Title / badge text
c = c.replace('<span class="nav-title-badge">ナビ</span>', '<span class="nav-title-badge">teppayナビ</span>')
c = c.replace('Teppay ナビゲーション', 'teppayナビ')
c = c.replace('Teppay Navi', 'teppayナビ')
c = c.replace('Teppay対応店舗', 'teppay対応店舗')
c = c.replace('Teppay対象店舗', 'teppay対象店舗')
c = c.replace('Teppay対応チェーン', 'teppay対応チェーン')
c = c.replace('Teppayチェッカー', 'teppayチェッカー')
c = c.replace('Teppay使える？', 'teppay使える？')
c = c.replace('Teppay非対応', 'teppay非対応')
c = c.replace('Teppay対象外', 'teppay対象外')
c = c.replace('Teppay対応です', 'teppay対応です')
c = c.replace('Teppay決済', 'teppay決済')
c = c.replace('Teppayマーク', 'teppayマーク')
c = c.replace('Teppayで', 'teppayで')
c = c.replace('「Teppay」', '「teppay」')
c = c.replace('Teppay利用者', 'teppay利用者')
c = c.replace('Teppay / Smart Code', 'teppay / Smart Code')
c = c.replace('Teppayチェーン', 'teppayチェーン')
c = c.replace('Teppay', 'teppay')

# --------------------------------------------------------------------------
# 11. Add Android beforeinstallprompt logic & dynamic area candidate generator in JS
# --------------------------------------------------------------------------
js_additions = """
    // Android PWA Deferred Install Prompt Support
    let deferredInstallPrompt = null;
    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      deferredInstallPrompt = e;
    });

    // Smart Area Suggestion & Search History Logic
    // Candidate expansions for searched areas
    const AREA_EXPANSIONS = {
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
    };

    function getRecentAreas() {
      try {
        const raw = localStorage.getItem("teppay_recent_areas");
        return raw ? JSON.parse(raw) : [];
      } catch (e) {
        return [];
      }
    }

    function addRecentArea(areaName) {
      if (!areaName || !areaName.trim()) return;
      const clean = areaName.trim();
      let list = getRecentAreas().filter(a => a !== clean);
      list.unshift(clean);
      if (list.length > 8) list = list.slice(0, 8);
      try {
        localStorage.setItem("teppay_recent_areas", JSON.stringify(list));
      } catch (e) {}
      renderAreaSuggestions();
    }

    function renderAreaSuggestions() {
      const scrollEl = document.getElementById("chips-scroll");
      if (!scrollEl) return;

      const recent = getRecentAreas();
      let proposals = [];

      // If user currently has an area set, first add "現在地に戻る"
      if (currentArea) {
        proposals.push({ label: "🎯 現在地に戻る", area: "", isGps: true });
      }

      // Add expansions if currentArea matches any keyword
      if (currentArea) {
        for (const [key, expansions] of Object.entries(AREA_EXPANSIONS)) {
          if (currentArea.includes(key)) {
            expansions.forEach(exp => {
              if (exp !== currentArea && !proposals.some(p => p.area === exp)) {
                proposals.push({ label: exp, area: exp });
              }
            });
            break;
          }
        }
      }

      // Add recent search history
      recent.forEach(r => {
        if (!proposals.some(p => p.area === r)) {
          proposals.push({ label: r, area: r });
        }
      });

      // Default: if no searches yet, keep hidden
      if (proposals.length === 0) {
        scrollEl.style.display = "none";
        scrollEl.innerHTML = "";
        return;
      }

      scrollEl.style.display = "flex";
      scrollEl.innerHTML = proposals.map(p => {
        const isActive = p.area === currentArea && !p.isGps;
        const cls = isActive ? "chip active" : "chip";
        return `<button type="button" class="${cls}" data-area="${p.area}">${p.label}</button>`;
      }).join("");

      // Re-attach click events
      scrollEl.querySelectorAll(".chip").forEach(chip => {
        chip.addEventListener("click", () => {
          const a = chip.getAttribute("data-area");
          setArea(a);
        });
      });
    }
"""

# Insert js_additions right before updateAreaDisplay
c = c.replace("    // Update Area UI\n    function updateAreaDisplay() {",
              js_additions + "\n    // Update Area UI\n    function updateAreaDisplay() {")

# Update setArea to call addRecentArea and renderAreaSuggestions
old_set_area = """    function setArea(newArea) {
      currentArea = newArea.trim();
      try {
        localStorage.setItem("teppay_area", currentArea);
      } catch (e) {}
      updateAreaDisplay();
      showToast(currentArea ? `検索エリアを「${currentArea}」に設定しました` : "現在地付近に設定しました");
      if (radarPanel.classList.contains("open")) {
        runAllGenreRadarScan();
      }
    }"""

new_set_area = """    function setArea(newArea) {
      currentArea = (newArea || "").trim();
      try {
        localStorage.setItem("teppay_area", currentArea);
      } catch (e) {}
      if (currentArea) {
        addRecentArea(currentArea);
      }
      updateAreaDisplay();
      renderAreaSuggestions();
      showToast(currentArea ? `検索エリアを「${currentArea}」に設定しました` : "現在地付近に設定しました");
      if (radarPanel.classList.contains("open")) {
        runAllGenreRadarScan();
      }
    }"""

if old_set_area in c:
    c = c.replace(old_set_area, new_set_area)

# Update install button click listener to prompt native Android PWA install if available
old_install_click = """    openInstallGuideBtn.addEventListener("click", () => {
      installModal.style.display = "flex";
    });"""

new_install_click = """    openInstallGuideBtn.addEventListener("click", async () => {
      if (deferredInstallPrompt) {
        try {
          deferredInstallPrompt.prompt();
          const { outcome } = await deferredInstallPrompt.userChoice;
          if (outcome === "accepted") {
            showToast("ホーム画面に追加しました");
          }
          deferredInstallPrompt = null;
          return;
        } catch (e) {}
      }
      installModal.style.display = "flex";
    });"""

if old_install_click in c:
    c = c.replace(old_install_click, new_install_click)

# Initialize renderAreaSuggestions on page load
c = c.replace("    updateAreaDisplay();", "    updateAreaDisplay();\n    renderAreaSuggestions();")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(c)

print("Improvements applied successfully!")
