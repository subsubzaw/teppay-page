import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Bottom Navigation (remove tab-checker)
old_nav = """  <!-- Bottom Navigation with Flat SVG Icons -->
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

new_nav = """  <!-- Bottom Navigation with Flat SVG Icons -->
  <nav class="nav-bar">
    <button class="nav-item active" data-tab="tab-quick">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><circle cx="12" cy="10" r="3"/><path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"/></svg>
      <span>周辺マップ</span>
    </button>
    <button class="nav-item" data-tab="tab-list">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h7"/><circle cx="17" cy="17" r="3"/><path d="m21 21-1.5-1.5"/></svg>
      <span>チェーン一覧</span>
    </button>
    <button class="nav-item" data-tab="tab-guide">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
      <span>ガイド</span>
    </button>
  </nav>"""

assert old_nav in content, "old_nav not found"
content = content.replace(old_nav, new_nav)

# 2. Remove chips-scroll below area search bar
old_chips_div = """    <!-- Area suggestions: hidden by default, shown based on searched content -->
    <div class="chips-scroll" id="chips-scroll" style="display: none;"></div>"""
assert old_chips_div in content, "old_chips_div not found"
content = content.replace(old_chips_div, "")

# 3. Remove TAB 3 (checker) and update TAB 4 (guide) to both iOS & Android
old_checker_and_guide = """    <!-- TAB 3: 「これ使える？」teppayチェッカー -->
    <div class="tab-pane" id="tab-checker">
      <div class="checker-box">
        <div style="font-size: 15px; font-weight: 700; margin-bottom: 6px;">
          店名を入力して即時判定
        </div>
        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">
          「このお店でteppay使える？」を公式シート準拠で判定します。非対応の場合は代替チェーンをご案内します。
        </div>

        <div class="checker-input-wrap">
          <input type="text" class="checker-input" id="checker-input" placeholder="店舗名（例: カインズ, マクドナルド, コーナン）">
          <button class="checker-btn" id="run-check-btn">判定</button>
        </div>

        <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px;">よく試される店舗例:</div>
        <div class="checker-samples">
          <button class="sample-pill" data-val="カインズ">カインズ</button>
          <button class="sample-pill" data-val="ケーヨーデイツー">ケーヨーデイツー</button>
          <button class="sample-pill" data-val="コーナン">コーナン</button>
          <button class="sample-pill" data-val="ビバホーム">ビバホーム</button>
          <button class="sample-pill" data-val="マクドナルド">マクドナルド</button>
          <button class="sample-pill" data-val="スターバックス">スターバックス</button>
          <button class="sample-pill" data-val="コメダ珈琲店">コメダ珈琲店</button>
          <button class="sample-pill" data-val="セリア">セリア</button>
          <button class="sample-pill" data-val="ダイソー">ダイソー</button>
          <button class="sample-pill" data-val="ニトリ">ニトリ</button>
          <button class="sample-pill" data-val="ユニクロ">ユニクロ</button>
          <button class="sample-pill" data-val="オーケー">オーケー</button>
        </div>

        <div class="result-card" id="check-result-card">
          <div class="result-header" id="result-header"></div>
          <div class="result-body" id="result-body"></div>
          <div style="margin-top: 10px;" id="result-action-area"></div>
        </div>
      </div>
    </div>

    <!-- TAB 4: 使い方 & ガイド -->
    <div class="tab-pane" id="tab-guide">
      <div class="card">
        <div class="card-title">
          <span>iPhoneでホーム画面に追加する方法</span>
        </div>
        <div class="step-item">
          <div class="step-num">1</div>
          <div class="step-text">
            <strong>SafariまたはChromeで開く</strong><br>
            このHTMLファイルをiPhoneのブラウザで開きます。
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">2</div>
          <div class="step-text">
            <strong>共有メニューをタップ</strong><br>
            Safariの場合は画面下の <strong>「共有アイコン（四角から矢印上）」</strong>、Chromeの場合は右上のメニューをタップ。
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">3</div>
          <div class="step-text">
            <strong>「ホーム画面に追加」を選択</strong><br>
            メニュー一覧から「ホーム画面に追加」をタップします。
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">4</div>
          <div class="step-text">
            <strong>ネイティブアプリのように起動！</strong><br>
            ホーム画面にアイコンが追加され、いつでもワンタップで近くのteppay対応店を探せます。
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">
          <span>teppay決済の基本知識</span>
        </div>
        <div style="font-size: 13px; line-height: 1.6; color: #334155;">
          <p style="margin-bottom: 8px;">
            <strong>Q. Suicaタッチ払いと何が違う？</strong><br>
            Suicaは「交通系ICカードのタッチ決済」ですが、teppayは「モバイルSuicaアプリ内のバーコード/QRコード決済」です。それぞれ使えるお店が異なります。
          </p>
          <p style="margin-bottom: 8px;">
            <strong>Q. どのお店で使える？</strong><br>
            レジに <strong>「teppay」</strong> または <strong>「Smart Code（スマートコード）」</strong> のマークがある加盟店（全国170万カ所以上）で利用できます。
          </p>
          <p style="margin-bottom: 8px;">
            <strong>Q. レジでの伝え方は？</strong><br>
            「スマートコードで」または「teppayで」「コード決済で」と伝えて画面のコードを提示（または店舗のQRコードをスキャン）します。
          </p>
          <p>
            <strong>Q. データの収録元は？</strong><br>
            ユーザー様管理のGoogleスプレッドシート（teppay対象チェーン店：全330チェーン）に基づき構成されています。
          </p>
        </div>
      </div>
    </div>"""

new_guide = """    <!-- TAB 3: 使い方 & ガイド (iPhone / Android 両対応) -->
    <div class="tab-pane" id="tab-guide">
      <div class="card">
        <div class="card-title">
          <span>ホーム画面に追加する方法（PWA）</span>
        </div>
        <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 14px; line-height: 1.6;">
          スマホのホーム画面に追加すると、アドレスバーのない全画面（アプリモード）で瞬時に起動でき、現在地周辺のteppay対応店をすぐに見つけられます。
        </p>

        <!-- iPhone Instructions -->
        <div style="background: var(--primary-ultra-light); border-radius: 16px; padding: 14px; margin-bottom: 14px; border: 1.5px solid var(--border);">
          <div style="font-weight: 800; color: var(--primary-dark); font-size: 14px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="3"/><path d="M12 18h.01"/></svg>
            <span>iPhone (Safari) の場合</span>
          </div>
          <div class="step-item">
            <div class="step-num">1</div>
            <div class="step-text">
              <strong>Safariで本ページを開く</strong><br>
              iPhoneの標準ブラウザ「Safari」でアクセスします。
            </div>
          </div>
          <div class="step-item">
            <div class="step-num">2</div>
            <div class="step-text">
              <strong>画面下部の「共有ボタン」をタップ</strong><br>
              画面下部中央の <strong>四角から上向き矢印</strong> アイコンをタップします。
            </div>
          </div>
          <div class="step-item">
            <div class="step-num">3</div>
            <div class="step-text">
              <strong>「ホーム画面に追加」を選択</strong><br>
              共有メニュー内をスクロールし、「ホーム画面に追加」をタップします。
            </div>
          </div>
          <div class="step-item">
            <div class="step-num">4</div>
            <div class="step-text">
              <strong>右上の「追加」をタップ</strong><br>
              ホーム画面にアプリアイコンが追加され、次回からワンタップで起動できます。
            </div>
          </div>
        </div>

        <!-- Android Instructions -->
        <div style="background: var(--primary-ultra-light); border-radius: 16px; padding: 14px; border: 1.5px solid var(--border);">
          <div style="font-weight: 800; color: var(--primary-dark); font-size: 14px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="3"/><path d="M12 18h.01"/></svg>
            <span>Android (Chrome) の場合</span>
          </div>
          <div class="step-item">
            <div class="step-num">1</div>
            <div class="step-text">
              <strong>Chromeで本ページを開く</strong><br>
              Androidの標準ブラウザ「Chrome」でアクセスします。
            </div>
          </div>
          <div class="step-item">
            <div class="step-num">2</div>
            <div class="step-text">
              <strong>右上のメニュー（︙）をタップ</strong><br>
              画面右上にある <strong>縦の3点リーダー（︙）</strong> をタップします。
            </div>
          </div>
          <div class="step-item">
            <div class="step-num">3</div>
            <div class="step-text">
              <strong>「アプリをインストール」または「ホーム画面に追加」</strong><br>
              メニュー内から追加項目をタップします。
            </div>
          </div>
          <div class="step-item">
            <div class="step-num">4</div>
            <div class="step-text">
              <strong>「インストール」をタップ</strong><br>
              ホーム画面やアプリ一覧に追加され、ネイティブアプリ同様に利用できます。
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">
          <span>teppay決済の基本知識 & よくある質問</span>
        </div>
        <div style="font-size: 13px; line-height: 1.6; color: #334155;">
          <p style="margin-bottom: 10px;">
            <strong>Q. Suicaタッチ払いと何が違う？</strong><br>
            Suicaは交通系ICカードのタッチ決済ですが、teppayは「モバイルSuicaアプリ等のバーコード/QRコード決済」です。対応している加盟店が異なります。
          </p>
          <p style="margin-bottom: 10px;">
            <strong>Q. どのお店で使える？</strong><br>
            レジや店頭に <strong>「teppay」</strong> または <strong>「Smart Code（スマートコード）」</strong> のマークがある全国170万カ所以上の店舗・チェーンで利用できます。
          </p>
          <p style="margin-bottom: 10px;">
            <strong>Q. レジでの伝え方は？</strong><br>
            「スマートコードで」または「teppayで」「コード決済で」と店員に伝え、スマホ画面のバーコードを提示（または店舗QRを読み取り）します。
          </p>
          <p>
            <strong>Q. データの収録元は？</strong><br>
            全330チェーンの公式対象店舗リストに基づき構成されています。
          </p>
        </div>
      </div>
    </div>"""

assert old_checker_and_guide in content, "old_checker_and_guide not found"
content = content.replace(old_checker_and_guide, new_guide)

# 4. Add CSS for chain-item logos and remove chips CSS
css_old = """    .chain-name {
      font-weight: 800;
      font-size: 14px;
      color: var(--text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 2px;
    }"""

css_new = """    .chain-item-logo {
      width: 38px;
      height: 38px;
      border-radius: 9px;
      background: #ffffff;
      object-fit: contain;
      flex: none;
      border: 1px solid var(--border);
      padding: 2px;
      box-shadow: 0 1px 3px rgba(0, 190, 183, 0.06);
    }
    .chain-item-logo-fallback {
      width: 38px;
      height: 38px;
      border-radius: 9px;
      background: var(--primary-ultra-light);
      border: 1px solid var(--border);
      color: var(--primary-dark);
      display: flex;
      align-items: center;
      justify-content: center;
      flex: none;
    }
    .chain-name {
      font-weight: 800;
      font-size: 14px;
      color: var(--text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 2px;
    }"""

assert css_old in content, "css_old not found"
content = content.replace(css_old, css_new)

# 5. Remove unused suggestion JS logic and add getChainFallbackIcon
js_suggestions_old = """    // Smart Area Suggestion & Search History Logic
    // Candidate expansions for searched areas
    const AREA_EXPANSIONS = {
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
        proposals.push({ label: "現在地に戻る", area: "", isGps: true });
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

    // Update Area UI
    function updateAreaDisplay() {
      if (currentArea) {
        areaDisplay.textContent = currentArea;
        radarAreaTitle.textContent = currentArea;
      } else {
        areaDisplay.textContent = "現在地付近";
        radarAreaTitle.textContent = "現在地付近";
      }
      // Update chips
      document.querySelectorAll(".chips-scroll .chip").forEach(chip => {
        const a = chip.getAttribute("data-area");
        if (a === currentArea) {
          chip.classList.add("active");
        } else {
          chip.classList.remove("active");
        }
      });
    }

    function setArea(newArea) {
      currentArea = (newArea || "").trim();
      try {
        localStorage.setItem("teppay_area", currentArea);
      } catch (e) {}
      if (currentArea) {
        addRecentArea(currentArea);
      }
      updateAreaDisplay();
    renderAreaSuggestions();
      renderAreaSuggestions();
      showToast(currentArea ? `検索エリアを「${currentArea}」に設定しました` : "現在地付近に設定しました");
      if (radarPanel.classList.contains("open")) {
        runAllGenreRadarScan();
      }
    }"""

js_suggestions_new = """    // Update Area UI
    function updateAreaDisplay() {
      if (currentArea) {
        areaDisplay.textContent = currentArea;
        radarAreaTitle.textContent = currentArea;
      } else {
        areaDisplay.textContent = "現在地付近";
        radarAreaTitle.textContent = "現在地付近";
      }
    }

    function setArea(newArea) {
      currentArea = (newArea || "").trim();
      try {
        localStorage.setItem("teppay_area", currentArea);
      } catch (e) {}
      updateAreaDisplay();
      showToast(currentArea ? `検索エリアを「${currentArea}」に設定しました` : "現在地付近に設定しました");
      if (radarPanel.classList.contains("open")) {
        runAllGenreRadarScan();
      }
    }"""

assert js_suggestions_old in content, "js_suggestions_old not found"
content = content.replace(js_suggestions_old, js_suggestions_new)

# 6. Update renderChainList to include store icon
old_chain_item = """      // Build HTML
      let html = "";
      filtered.forEach(item => {
        const tagsHtml = item.tags.map(t => `<span class="badge badge-tag">${t}</span>`).join("");
        html += `
          <div class="chain-item">
            <div class="chain-info">
              <div class="chain-name">${item.name}</div>
              <div class="chain-meta">
                <span class="badge badge-cat">${item.category}</span>
                ${tagsHtml}
              </div>
            </div>
            <div class="chain-actions">
              <button class="action-btn map" data-action="map-chain" data-name="${item.name}">
                マップ
              </button>
              <button class="action-btn copy" data-action="copy-chain" data-name="${item.name}">
                コピー
              </button>
            </div>
          </div>
        `;
      });"""

new_chain_item = """      // Category fallback flat SVG icon helper
      function getChainFallbackIcon(item) {
        const cat = item.category || "";
        const tags = (item.tags || []).join(" ");
        if (cat.includes("コンビニ")) {
          return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`;
        } else if (cat.includes("ドラッグ") || tags.includes("ドラッグ")) {
          return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg>`;
        } else if (tags.includes("ホームセンター")) {
          return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>`;
        } else if (cat.includes("スーパー") || tags.includes("スーパー")) {
          return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>`;
        } else if (tags.includes("カフェ") || cat.includes("カフェ")) {
          return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><line x1="6" y1="2" x2="6" y2="4"/><line x1="10" y1="2" x2="10" y2="4"/><line x1="14" y1="2" x2="14" y2="4"/></svg>`;
        } else if (cat.includes("グルメ") || cat.includes("飲食")) {
          return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2v20M18 8a3 3 0 0 0 0-6v6ZM6 2v7a3 3 0 0 0 6 0V2M9 12v10"/></svg>`;
        } else if (cat.includes("家電")) {
          return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`;
        } else if (cat.includes("JR") || tags.includes("エキナカ")) {
          return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="16" rx="2"/><path d="M4 11h16"/><path d="M12 3v8"/><circle cx="8" cy="15" r="1"/><circle cx="16" cy="15" r="1"/><path d="m6 19-2 2"/><path d="m18 19 2 2"/></svg>`;
        } else if (cat.includes("カラオケ")) {
          return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 8-9.04 9.06a2.82 2.82 0 1 0 3.98 3.98L16 12"/><circle cx="17" cy="7" r="5"/></svg>`;
        }
        return `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`;
      }

      // Build HTML
      let html = "";
      filtered.forEach(item => {
        const tagsHtml = item.tags.map(t => `<span class="badge badge-tag">${t}</span>`).join("");
        const logoUrl = LOGO_MAP[item.name];
        const logoHtml = logoUrl
          ? `<img src="${logoUrl}" class="chain-item-logo" alt="${item.name}" loading="lazy">`
          : `<div class="chain-item-logo-fallback">${getChainFallbackIcon(item)}</div>`;

        html += `
          <div class="chain-item">
            ${logoHtml}
            <div class="chain-info">
              <div class="chain-name">${item.name}</div>
              <div class="chain-meta">
                <span class="badge badge-cat">${item.category}</span>
                ${tagsHtml}
              </div>
            </div>
            <div class="chain-actions">
              <button class="action-btn map" data-action="map-chain" data-name="${item.name}">
                マップ
              </button>
              <button class="action-btn copy" data-action="copy-chain" data-name="${item.name}">
                コピー
              </button>
            </div>
          </div>
        `;
      });"""

assert old_chain_item in content, "old_chain_item not found"
content = content.replace(old_chain_item, new_chain_item)

# 7. Update empty search message in chain-list
old_empty = """<div style="font-size: 12px;">店名「${q}」はteppay非対応の可能性があります。「使える？判定」タブでご確認ください。</div>"""
new_empty = """<div style="font-size: 12px;">店名「${q}」はteppay非対応の可能性があります。別の名称やキーワードでお試しください。</div>"""
assert old_empty in content, "old_empty not found"
content = content.replace(old_empty, new_empty)

# 8. Remove Checker JS listeners at bottom
old_checker_js = """    // Checker Logic
    const checkerInput = document.getElementById("checker-input");
    const runCheckBtn = document.getElementById("run-check-btn");
    const checkResultCard = document.getElementById("check-result-card");
    const resultHeader = document.getElementById("result-header");
    const resultBody = document.getElementById("result-body");
    const resultActionArea = document.getElementById("result-action-area");

    function executeCheck(query) {
      const q = query.trim();
      if (!q) return;

      // Check in ALTS_DATA exact or partial
      let altMatch = null;
      for (const [k, v] of Object.entries(ALTS_DATA)) {
        if (q.includes(k) || k.includes(q)) {
          altMatch = { key: k, data: v };
          break;
        }
      }

      // Check in CHAINS_DATA using false-positive-safe matcher first, or exact/substring if not excluded
      const chainMatch = (altMatch && altMatch.data.status === "ng")
        ? null
        : (matchPoiToteppayChain(q, "") || CHAINS_DATA.find(c => {
            const excludes = CHAIN_FP_EXCLUDES[c.name];
            if (excludes && excludes.some(ex => q.toLowerCase().includes(ex.toLowerCase()))) return false;
            return c.name.toLowerCase().includes(q.toLowerCase()) || q.toLowerCase().includes(c.name.toLowerCase());
          }));

      checkResultCard.className = "result-card";
      resultActionArea.innerHTML = "";

      if (chainMatch) {
        // Supported!
        checkResultCard.classList.add("ok");
        resultHeader.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#16a34a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="icon-svg" style="margin-right:6px;"><polyline points="20 6 9 17 4 12"/></svg>【${chainMatch.name}】はteppay対応です！`;
        resultBody.innerHTML = `
          <div><strong>業種:</strong> ${chainMatch.category}</div>
          <div style="margin-top: 4px; font-size: 12px; color: #166534;">
            ※Smart Codeまたはteppayマークのある店舗でコード決済が可能です。
          </div>
        `;
        resultActionArea.innerHTML = `
          <button class="action-btn map" style="width: 100%; justify-content: center; padding: 8px;" onclick="openGoogleMaps('${chainMatch.name}')">
            現在のエリアで「${chainMatch.name}」をマップ検索
          </button>
        `;
      } else if (altMatch && altMatch.data.status === "ng") {
        // Known Not Supported!
        checkResultCard.classList.add("ng");
        resultHeader.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#d97706" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="icon-svg" style="margin-right:6px;"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>【${altMatch.key}】はteppay対象外です`;
        resultBody.innerHTML = `
          <div style="margin-bottom: 6px;">${altMatch.data.reason}</div>
          <div style="background: white; padding: 8px 10px; border-radius: 6px; border: 1px solid #fcd34d;">
            <strong>おすすめの代替対応店舗:</strong><br>
            ${altMatch.data.recommend}
          </div>
        `;
        resultActionArea.innerHTML = `
          <button class="action-btn map" style="width: 100%; justify-content: center; padding: 8px;" onclick="document.querySelector('[data-tab=\\'tab-quick\\']').click()">
            周辺の対応店舗マップを見る
          </button>
        `;
      } else {
        // General Unknown / Not in sheet
        checkResultCard.classList.add("ng");
        resultHeader.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#64748b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="icon-svg" style="margin-right:6px;"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>【${q}】は公式対象シートに未掲載です`;
        resultBody.innerHTML = `
          <div>公式掲載の330チェーンに該当がありませんでした（teppay / Smart Code非対応の可能性が高いです）。</div>
          <div style="margin-top: 6px; font-size: 12px;">
            ※個人の商店等で個別にSmart Codeを導入している場合を除き、基本的にチェーン店では利用できません。
          </div>
        `;
        resultActionArea.innerHTML = `
          <button class="action-btn" style="width: 100%; justify-content: center; padding: 8px;" onclick="document.querySelector('[data-tab=\\'tab-list\\']').click()">
            全330チェーン一覧で探す
          </button>
        `;
      }
    }

    runCheckBtn.addEventListener("click", () => {
      executeCheck(checkerInput.value);
    });

    checkerInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        executeCheck(checkerInput.value);
      }
    });

    document.querySelectorAll(".sample-pill").forEach(pill => {
      pill.addEventListener("click", () => {
        const val = pill.getAttribute("data-val");
        checkerInput.value = val;
        executeCheck(val);
      });
    });"""

assert old_checker_js in content, "old_checker_js not found"
content = content.replace(old_checker_js, "")

# 9. Clean up trailing renderAreaSuggestions() calls and unused listeners
content = content.replace("renderAreaSuggestions();", "")
content = re.sub(r'document\.querySelectorAll\("\.chips-scroll \.chip"\)\.forEach\(chip => \{[\s\S]*?\}\);', '', content)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully applied UI simplification script!")
