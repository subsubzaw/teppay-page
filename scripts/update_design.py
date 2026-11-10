import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update <head> icons and font
old_head_icons = """  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🟢</text></svg>">
  <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2220%22 fill=%22%2300873c%22/><text x=%2250%22 y=%2265%22 font-size=%2250%22 text-anchor=%22middle%22 fill=%22white%22 font-weight=%22bold%22 font-family=%22sans-serif%22>T</text></svg>">"""

new_head_icons = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@500;700;900&display=swap" rel="stylesheet">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2228%22 fill=%22%2300beb7%22/><text x=%2250%22 y=%2266%22 font-size=%2254%22 text-anchor=%22middle%22 fill=%22white%22 font-weight=%22900%22 font-family=%22sans-serif%22>t</text></svg>">
  <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2228%22 fill=%22%2300beb7%22/><text x=%2250%22 y=%2266%22 font-size=%2254%22 text-anchor=%22middle%22 fill=%22white%22 font-weight=%22900%22 font-family=%22sans-serif%22>t</text></svg>">"""

assert old_head_icons in content, "old_head_icons not found"
content = content.replace(old_head_icons, new_head_icons)

# 2. Extract and replace entire <style> block
new_css = """  <style>
    :root {
      --primary: #00beb7;
      --primary-dark: #00968f;
      --primary-mint: #64d9c8;
      --primary-light: #e6faf7;
      --primary-ultra-light: #f2fcfb;
      --accent-yellow: #fcee21;
      --accent-pink: #ff4081;
      --slate-footer: #5c6d82;
      --slate-dark: #283548;
      --accent: #0284c7;
      --bg: #f4fbfb;
      --card-bg: #ffffff;
      --text: #283548;
      --text-muted: #627284;
      --border: #d5f4ee;
      --border-dark: #b2ebe1;
      --shadow: 0 4px 16px rgba(0, 190, 183, 0.08);
      --radius: 20px;
      --radius-sm: 12px;
      --radius-pill: 9999px;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }
    body {
      font-family: 'Zen Kaku Gothic New', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", "Hiragino Kaku Gothic ProN", Meiryo, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding-bottom: 90px;
      -webkit-font-smoothing: antialiased;
    }

    /* Top White Navbar */
    header {
      background: #ffffff;
      color: var(--text);
      padding: 10px 16px;
      position: sticky;
      top: 0;
      z-index: 50;
      border-bottom: 1.5px solid var(--border);
      box-shadow: 0 2px 8px rgba(0, 190, 183, 0.06);
    }
    .header-inner {
      max-width: 680px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .logo-area {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .teppay-logo-svg {
      height: 32px;
      width: auto;
      display: block;
    }
    .nav-title-badge {
      background: var(--primary);
      color: white;
      font-weight: 900;
      font-size: 11px;
      padding: 3px 9px;
      border-radius: var(--radius-pill);
      letter-spacing: 0.5px;
    }
    .header-btn {
      background: #ffffff;
      border: 1.5px solid var(--primary);
      color: var(--primary-dark);
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }
    .header-btn:hover, .header-btn:active {
      background: var(--primary-light);
    }

    /* Hero Brand Banner matching image.png */
    .hero-brand-banner {
      background: linear-gradient(135deg, #00beb7 0%, #03bfb7 50%, #2dd4bf 100%);
      color: white;
      padding: 18px 16px 20px;
      position: relative;
      overflow: hidden;
    }
    .hero-brand-banner::before {
      content: "";
      position: absolute;
      top: -25px;
      right: -25px;
      width: 150px;
      height: 150px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.12);
      pointer-events: none;
    }
    .hero-brand-banner::after {
      content: "";
      position: absolute;
      bottom: -35px;
      left: -35px;
      width: 120px;
      height: 120px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      pointer-events: none;
    }
    .hero-brand-inner {
      max-width: 680px;
      margin: 0 auto;
      position: relative;
      z-index: 2;
    }
    .hero-brand-top {
      display: flex;
      gap: 6px;
      align-items: center;
      margin-bottom: 8px;
      flex-wrap: wrap;
    }
    .hero-yellow-badge {
      background: var(--accent-yellow);
      color: var(--slate-dark);
      font-weight: 900;
      font-size: 11px;
      padding: 3px 10px;
      border-radius: var(--radius-pill);
      display: inline-block;
      box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }
    .hero-pink-badge {
      background: var(--accent-pink);
      color: white;
      font-weight: 700;
      font-size: 10px;
      padding: 3px 8px;
      border-radius: var(--radius-pill);
    }
    .hero-brand-title {
      font-size: 23px;
      font-weight: 900;
      line-height: 1.25;
      letter-spacing: -0.5px;
      margin-bottom: 5px;
      text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .hero-brand-title span {
      color: var(--accent-yellow);
    }
    .hero-brand-desc {
      font-size: 12px;
      opacity: 0.95;
      font-weight: 500;
    }

    /* Global Area Bar */
    .area-bar {
      background: #ffffff;
      border-bottom: 1.5px solid var(--border);
      padding: 10px 16px;
      position: sticky;
      top: 53px;
      z-index: 40;
      box-shadow: 0 2px 6px rgba(0, 190, 183, 0.05);
    }
    .area-status-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 8px;
    }
    .area-label {
      font-size: 12px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
    }
    .current-area-badge {
      font-weight: 800;
      color: var(--primary-dark);
      background: var(--primary-light);
      border: 1.5px solid var(--border-dark);
      padding: 4px 12px;
      border-radius: var(--radius-pill);
      font-size: 13px;
      max-width: 180px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .area-actions {
      display: flex;
      gap: 6px;
    }
    .btn-sm {
      padding: 5px 12px;
      font-size: 11px;
      border-radius: var(--radius-pill);
      border: 1.5px solid var(--border-dark);
      background: #ffffff;
      color: var(--text);
      cursor: pointer;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s;
    }
    .btn-sm:hover {
      background: var(--primary-light);
    }
    .btn-sm.primary {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
      box-shadow: 0 2px 6px rgba(0, 190, 183, 0.3);
    }
    .btn-sm.primary:hover {
      background: var(--primary-dark);
    }
    .chips-scroll {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 2px;
      scrollbar-width: none;
    }
    .chips-scroll::-webkit-scrollbar {
      display: none;
    }
    .chip {
      padding: 5px 12px;
      border-radius: var(--radius-pill);
      font-size: 11px;
      white-space: nowrap;
      background: #ffffff;
      border: 1.5px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s;
      font-weight: 600;
    }
    .chip:hover {
      border-color: var(--primary-mint);
      color: var(--primary-dark);
    }
    .chip.active {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
      font-weight: 800;
      box-shadow: 0 2px 6px rgba(0, 190, 183, 0.25);
    }

    /* Area Input Panel */
    .area-input-panel {
      display: none;
      margin-top: 8px;
      padding-top: 8px;
      border-top: 1px dashed var(--border-dark);
    }
    .area-input-group {
      display: flex;
      gap: 6px;
    }
    .area-input-group input {
      flex: 1;
      padding: 8px 14px;
      border: 1.5px solid var(--border-dark);
      border-radius: var(--radius-pill);
      font-size: 13px;
      outline: none;
      font-family: inherit;
    }
    .area-input-group input:focus {
      border-color: var(--primary);
    }

    /* Container */
    .container {
      max-width: 680px;
      margin: 0 auto;
      padding: 16px;
    }

    /* Radar Map Panel (All-genre map) */
    .radar-panel {
      display: none;
      background: #ffffff;
      border: 2px solid var(--primary-mint);
      border-radius: 22px;
      padding: 16px;
      margin-bottom: 18px;
      box-shadow: 0 6px 20px rgba(0, 190, 183, 0.1);
    }
    .radar-panel.open {
      display: block;
    }
    .radar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      gap: 8px;
    }
    .radar-controls {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 12px;
      align-items: center;
      justify-content: space-between;
    }
    .radius-group {
      display: flex;
      gap: 5px;
    }
    .radius-btn {
      padding: 5px 12px;
      font-size: 11px;
      border-radius: var(--radius-pill);
      border: 1.5px solid var(--border-dark);
      background: #ffffff;
      color: var(--text-muted);
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s;
    }
    .radius-btn:hover {
      border-color: var(--primary);
      color: var(--primary-dark);
    }
    .radius-btn.active {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
      box-shadow: 0 2px 6px rgba(0, 190, 183, 0.25);
    }
    .exclude-cvs-toggle {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      color: var(--text);
      cursor: pointer;
      background: var(--primary-ultra-light);
      padding: 5px 12px;
      border-radius: var(--radius-pill);
      border: 1.5px solid var(--border);
    }
    .store-pin {
      position: absolute;
      transform: translate(-50%, -50%);
      display: inline-flex; align-items: center; gap: 4px;
      max-width: 120px; box-sizing: border-box;
      color: #fff; border: 2px solid #fff; border-radius: var(--radius-pill);
      padding: 2px 7px 2px 3px; font-size: 11px; font-weight: 800; line-height: 16px;
      box-shadow: 0 3px 8px rgba(0,0,0,0.3);
      cursor: pointer;
      user-select: none;
    }
    .store-pin.has-logo { padding-left: 2px; }
    .store-pin .pin-logo {
      width: 18px; height: 18px; border-radius: 50%;
      background: #fff; object-fit: contain; flex: none;
      box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    .store-pin span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0; }
    .radar-store-logo {
      width: 32px; height: 32px; border-radius: 8px;
      background: #fff; object-fit: contain; flex: none;
      border: 1px solid var(--border); padding: 2px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    #radar-map-box {
      width: 100%;
      height: 360px;
      border-radius: 16px;
      border: 1.5px solid var(--border);
      margin-bottom: 12px;
      z-index: 10;
      overflow: hidden;
    }
    .radar-status {
      font-size: 12px;
      font-weight: 700;
      color: var(--primary-dark);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      flex-wrap: wrap;
    }
    .radar-results-list {
      max-height: 270px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 12px;
      padding-right: 2px;
    }
    .radar-store-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 9px 12px;
      border: 1.5px solid var(--border);
      border-radius: 14px;
      background: var(--primary-ultra-light);
      gap: 10px;
      transition: all 0.15s;
    }
    .radar-store-item:hover {
      border-color: var(--primary-mint);
      background: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 190, 183, 0.08);
    }
    .radar-store-info {
      min-width: 0;
      flex: 1;
    }
    .radar-store-name {
      font-size: 13px;
      font-weight: 800;
      color: var(--text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 2px;
    }
    .radar-store-sub {
      font-size: 11px;
      color: var(--text-muted);
      display: flex;
      gap: 6px;
      align-items: center;
      font-weight: 500;
    }
    .radar-store-sub span:first-child {
      color: var(--primary-dark);
      font-weight: 700;
    }

    /* Bottom Navigation Tabs */
    .nav-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-top: 1.5px solid var(--border);
      display: flex;
      justify-content: space-around;
      padding: 6px 4px 10px;
      z-index: 60;
      box-shadow: 0 -2px 12px rgba(0, 190, 183, 0.08);
    }
    .nav-item {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 10px;
      font-weight: 700;
      cursor: pointer;
      padding: 4px 0;
      transition: color 0.15s;
    }
    .nav-item.active {
      color: var(--primary-dark);
    }
    .nav-icon {
      font-size: 19px;
      line-height: 1;
    }

    /* Tab Panes */
    .tab-pane {
      display: none;
    }
    .tab-pane.active {
      display: block;
    }

    /* Cards */
    .card {
      background: var(--card-bg);
      border-radius: var(--radius);
      border: 1.5px solid var(--border);
      box-shadow: var(--shadow);
      padding: 18px;
      margin-bottom: 16px;
    }
    .card-title {
      font-size: 15px;
      font-weight: 800;
      color: var(--text);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Preset Grid */
    .preset-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      margin-bottom: 16px;
    }
    @media (min-width: 500px) {
      .preset-grid {
        grid-template-columns: repeat(3, 1fr);
      }
    }
    .preset-card {
      background: white;
      border: 1.5px solid var(--border);
      border-radius: 18px;
      padding: 14px 12px;
      cursor: pointer;
      transition: all 0.15s ease-in-out;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0, 190, 183, 0.04);
    }
    .preset-card:hover, .preset-card:active {
      border-color: var(--primary);
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 190, 183, 0.15);
    }
    .preset-header {
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 800;
      font-size: 13px;
      color: var(--text);
      margin-bottom: 4px;
    }
    .preset-icon {
      font-size: 18px;
    }
    .preset-desc {
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.35;
      margin-bottom: 10px;
    }
    .preset-btn {
      width: 100%;
      background: var(--primary-light);
      color: var(--primary-dark);
      border: 1.5px solid var(--border-dark);
      font-weight: 800;
      font-size: 11px;
      padding: 6px 10px;
      border-radius: var(--radius-pill);
      cursor: pointer;
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.15s;
    }
    .preset-btn:hover {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }

    /* Search Bar */
    .search-bar-wrap {
      margin-bottom: 12px;
      position: relative;
    }
    .search-input {
      width: 100%;
      padding: 11px 16px 11px 38px;
      border: 2px solid var(--border-dark);
      border-radius: var(--radius-pill);
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
      background: white;
      font-family: inherit;
    }
    .search-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(0, 190, 183, 0.15);
    }
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--primary);
      font-size: 14px;
    }
    .clear-search-btn {
      position: absolute;
      right: 14px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 14px;
      display: none;
    }

    /* Category Pill Filter */
    .cat-filter-wrap {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 12px;
      scrollbar-width: none;
    }
    .cat-filter-wrap::-webkit-scrollbar {
      display: none;
    }
    .cat-pill {
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-size: 12px;
      background: white;
      border: 1.5px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
      font-weight: 700;
      transition: all 0.15s;
    }
    .cat-pill:hover {
      border-color: var(--primary-mint);
      color: var(--primary-dark);
    }
    .cat-pill.active {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
      font-weight: 800;
      box-shadow: 0 2px 8px rgba(0, 190, 183, 0.3);
    }

    /* Chain List Cards */
    .chain-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .chain-item {
      background: white;
      border: 1.5px solid var(--border);
      border-radius: 16px;
      padding: 12px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      transition: all 0.15s;
    }
    .chain-item:hover {
      border-color: var(--primary-mint);
      box-shadow: 0 4px 12px rgba(0, 190, 183, 0.08);
    }
    .chain-info {
      flex: 1;
      min-width: 0;
    }
    .chain-name {
      font-weight: 800;
      font-size: 14px;
      color: var(--text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 2px;
    }
    .chain-meta {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }
    .badge {
      font-size: 10px;
      padding: 2px 8px;
      border-radius: var(--radius-pill);
      font-weight: 700;
    }
    .badge-cat {
      background: var(--primary-ultra-light);
      color: var(--primary-dark);
      border: 1px solid var(--border);
    }
    .badge-tag {
      background: #fef3c7;
      color: #92400e;
      border: 1px solid #fde68a;
    }
    .chain-actions {
      display: flex;
      gap: 6px;
      flex-shrink: 0;
    }
    .action-btn {
      padding: 6px 12px;
      border-radius: var(--radius-pill);
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      border: 1.5px solid var(--border);
      background: #ffffff;
      color: var(--text);
      display: inline-flex;
      align-items: center;
      gap: 4px;
      text-decoration: none;
      transition: all 0.15s;
    }
    .action-btn.map {
      background: var(--primary-light);
      border-color: var(--primary);
      color: var(--primary-dark);
    }
    .action-btn.map:hover {
      background: var(--primary);
      color: white;
    }
    .action-btn.copy:hover {
      background: var(--primary-ultra-light);
      border-color: var(--border-dark);
    }

    /* Checker Tab */
    .checker-box {
      background: white;
      border: 2px solid var(--primary-mint);
      border-radius: 22px;
      padding: 20px;
      margin-bottom: 16px;
      box-shadow: 0 6px 20px rgba(0, 190, 183, 0.08);
    }
    .checker-input-wrap {
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
    }
    .checker-input {
      flex: 1;
      padding: 11px 16px;
      border: 2px solid var(--border-dark);
      border-radius: var(--radius-pill);
      font-size: 14px;
      outline: none;
      font-family: inherit;
    }
    .checker-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(0, 190, 183, 0.15);
    }
    .checker-btn {
      background: var(--primary);
      color: white;
      border: none;
      padding: 11px 22px;
      border-radius: var(--radius-pill);
      font-weight: 800;
      font-size: 13px;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(0, 190, 183, 0.3);
      transition: all 0.15s;
    }
    .checker-btn:hover {
      background: var(--primary-dark);
    }
    .checker-samples {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 16px;
    }
    .sample-pill {
      padding: 5px 12px;
      background: var(--primary-ultra-light);
      border-radius: var(--radius-pill);
      font-size: 11px;
      color: var(--primary-dark);
      cursor: pointer;
      border: 1px solid var(--border);
      font-weight: 700;
      transition: all 0.15s;
    }
    .sample-pill:hover {
      background: var(--primary-light);
      border-color: var(--primary);
    }
    .result-card {
      border-radius: 16px;
      padding: 16px;
      margin-top: 12px;
      display: none;
    }
    .result-card.ok {
      display: block;
      background: #f0fdf4;
      border: 2px solid #86efac;
      color: #14532d;
    }
    .result-card.ng {
      display: block;
      background: #fffbeb;
      border: 2px solid #fde68a;
      color: #78350f;
    }
    .result-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 800;
      font-size: 15px;
      margin-bottom: 6px;
    }
    .result-body {
      font-size: 13px;
      line-height: 1.5;
    }

    /* Modal / Help */
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(40, 53, 72, 0.6);
      backdrop-filter: blur(4px);
      z-index: 100;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }
    .modal-content {
      background: white;
      border-radius: 22px;
      max-width: 500px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 22px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
      border: 2px solid var(--primary-mint);
    }
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 10px;
    }
    .modal-close-btn {
      background: var(--primary-ultra-light);
      border: 1px solid var(--border);
      width: 30px;
      height: 30px;
      border-radius: 50%;
      cursor: pointer;
      font-weight: bold;
      color: var(--text);
    }

    /* Toast */
    .toast {
      position: fixed;
      bottom: 75px;
      left: 50%;
      transform: translateX(-50%) translateY(50px);
      background: var(--slate-dark);
      color: white;
      padding: 9px 20px;
      border-radius: var(--radius-pill);
      font-size: 12px;
      font-weight: 700;
      box-shadow: 0 4px 14px rgba(0,0,0,0.2);
      z-index: 99;
      opacity: 0;
      transition: all 0.25s ease-out;
      pointer-events: none;
    }
    .toast.show {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }

    /* Guide steps */
    .step-item {
      display: flex;
      gap: 12px;
      margin-bottom: 14px;
      align-items: flex-start;
      background: var(--primary-ultra-light);
      border: 1.5px solid var(--border);
      border-radius: 16px;
      padding: 14px;
    }
    .step-num {
      background: var(--primary);
      color: white;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 900;
      flex-shrink: 0;
      box-shadow: 0 2px 6px rgba(0, 190, 183, 0.3);
    }
    .step-text {
      font-size: 13px;
    }
    .step-text strong {
      color: var(--text);
    }

    /* Footer styled after official Teppay page */
    .teppay-footer {
      background: var(--slate-footer);
      color: #e2e8f0;
      font-size: 11px;
      line-height: 1.7;
      margin-top: 30px;
      position: relative;
    }
    .footer-track-ribbon {
      height: 8px;
      width: 100%;
      background: repeating-linear-gradient(90deg, #00beb7 0px, #00beb7 12px, #283548 12px, #283548 24px);
    }
    .footer-content {
      max-width: 680px;
      margin: 0 auto;
      padding: 24px 16px 40px;
    }
    .footer-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
    }
    .footer-desc {
      color: #cbd5e1;
      margin-bottom: 14px;
      font-size: 11px;
    }
    .footer-copy {
      color: #94a3b8;
      font-size: 10px;
    }
  </style>"""

content = re.sub(r'  <style>.*?</style>', new_css, content, flags=re.DOTALL)

# 3. Update header HTML and add Hero Brand Banner
old_header = """  <!-- Top Header -->
  <header>
    <div class="header-top">
      <div class="logo-area">
        <span class="logo-badge">Teppay</span>
        <h1>Teppay ナビ</h1>
      </div>
      <button class="header-btn" id="open-install-guide-btn">
        <span>📲</span> ホーム画面追加
      </button>
    </div>
    <div class="sub-tag">全330チェーン対応店舗 &amp; Googleマップ即時連携ツール</div>
  </header>"""

new_header = """  <!-- Top Header with Official Railway Track Teppay Logo -->
  <header>
    <div class="header-inner">
      <div class="logo-area">
        <svg viewBox="0 0 110 34" class="teppay-logo-svg" aria-label="teppay">
          <rect x="2" y="2" width="106" height="30" rx="15" fill="#ffffff" stroke="#00beb7" stroke-width="2.5"/>
          <rect x="5.5" y="5.5" width="99" height="23" rx="11.5" fill="none" stroke="#283548" stroke-width="1.8" stroke-dasharray="3.5,4"/>
          <text x="55" y="22" font-family="'Zen Kaku Gothic New', sans-serif" font-size="16" font-weight="900" fill="#283548" text-anchor="middle" letter-spacing="-0.5px">teppay</text>
        </svg>
        <span class="nav-title-badge">ナビ</span>
      </div>
      <button class="header-btn" id="open-install-guide-btn">
        <span>📲</span> ホーム追加
      </button>
    </div>
  </header>

  <!-- Hero Brand Banner matching image.png -->
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

assert old_header in content, "old_header not found"
content = content.replace(old_header, new_header)

# 4. Add footer before nav-bar
footer_html = """  <!-- Official Teppay Style Footer -->
  <footer class="teppay-footer">
    <div class="footer-track-ribbon"></div>
    <div class="footer-content">
      <div class="footer-brand">
        <svg viewBox="0 0 110 34" class="teppay-logo-svg" style="height:28px;">
          <rect x="2" y="2" width="106" height="30" rx="15" fill="#ffffff" stroke="#00beb7" stroke-width="2.5"/>
          <rect x="5.5" y="5.5" width="99" height="23" rx="11.5" fill="none" stroke="#283548" stroke-width="1.8" stroke-dasharray="3.5,4"/>
          <text x="55" y="22" font-family="'Zen Kaku Gothic New', sans-serif" font-size="16" font-weight="900" fill="#283548" text-anchor="middle" letter-spacing="-0.5px">teppay</text>
        </svg>
        <span style="font-weight:800; font-size:12px; color:#ffffff;">Teppay ナビゲーション</span>
      </div>
      <div class="footer-desc">
        ※本サイトはTeppay利用者のための周辺店舗検索・ルート案内ツールです。加盟店データは全330チェーンの対象店舗リストに基づき構成されています。
      </div>
      <div class="footer-copy">
        &copy; 2026 Teppay Navi - 全330チェーン対象店舗マップ
      </div>
    </div>
  </footer>

  <!-- Bottom Navigation -->"""

assert "  <!-- Bottom Navigation -->" in content, "Bottom Navigation not found"
content = content.replace("  <!-- Bottom Navigation -->", footer_html)

# 5. Update map pin colors in JavaScript
# pinColor: #00873c -> #00beb7
content = content.replace('const pinColor = isHc ? "#d97706" : (isCvs ? "#0284c7" : "#00873c");',
                          'const pinColor = isHc ? "#f59e0b" : (isCvs ? "#0284c7" : "#00beb7");')

# radarCircle color: #00873c -> #00beb7, fillColor #34d399 -> #64d9c8
old_circle = """        radarCircle = L.circle([lastCenterCoords.lat, lastCenterCoords.lng], {
          radius: scanRadius,
          color: "#00873c",
          fillColor: "#34d399",
          fillOpacity: 0.08,
          weight: 1.5
        }).addTo(radarMap);"""

new_circle = """        radarCircle = L.circle([lastCenterCoords.lat, lastCenterCoords.lng], {
          radius: scanRadius,
          color: "#00beb7",
          fillColor: "#64d9c8",
          fillOpacity: 0.12,
          weight: 2
        }).addTo(radarMap);"""

if old_circle in content:
    content = content.replace(old_circle, new_circle)

# center pin: #dc2626 -> #ff4081
content = content.replace('style="background:#dc2626;color:white;border:2px solid white;border-radius:50%;width:16px;height:16px;box-shadow:0 2px 5px rgba(0,0,0,0.4);"',
                          'style="background:#ff4081;color:white;border:2.5px solid white;border-radius:50%;width:18px;height:18px;box-shadow:0 2px 6px rgba(0,0,0,0.35);"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Design update completed successfully!")
