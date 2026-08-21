from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_fix_dashboard_backup.html")
backup.write_text(s)

start_id = s.find('id="dashboard"')
if start_id == -1:
    raise SystemExit("id=\"dashboard\" が見つかりません")

start = s.rfind("<section", 0, start_id)
if start == -1:
    raise SystemExit("dashboard の開始 section が見つかりません")

contracts_id = s.find('id="contracts"', start_id)
if contracts_id == -1:
    raise SystemExit("id=\"contracts\" が見つかりません")

end = s.rfind("<section", 0, contracts_id)
if end == -1 or end <= start:
    raise SystemExit("contracts の開始 section が見つかりません")

new_dashboard = '''<section class="tab-pane active" id="dashboard">
      <h2>ダッシュボード</h2>

      <div class="dashboard-next">
        <h3>次に確認すること</h3>
        <ul>
          <li>契約書の整理</li>
          <li>連絡先の確認</li>
          <li>自動更新設定の見直し</li>
        </ul>
      </div>

      <div class="dashboard-cards">
        <div class="dashboard-card">
          <h3>総契約数</h3>
          <div class="dashboard-value" id="total-contracts">6</div>
          <p class="dashboard-caption">すべての契約</p>
        </div>

        <div class="dashboard-card">
          <h3>引継ぎ準備度</h3>
          <div class="dashboard-value" id="readiness-score">65%</div>
          <p class="dashboard-caption">家族への引継ぎ準備</p>
        </div>

        <div class="dashboard-card">
          <h3>家族が把握していない契約</h3>
          <div class="dashboard-value" id="unaware-contracts">3件</div>
          <p class="dashboard-caption">引継ぎが必要な契約</p>
        </div>

        <div class="dashboard-card">
          <h3>自動更新あり</h3>
          <div class="dashboard-value" id="auto-renewals">5件</div>
          <p class="dashboard-caption">自動更新設定の確認</p>
        </div>

        <div class="dashboard-card">
          <h3>今月支払い予定</h3>
          <div class="dashboard-value" id="monthly-payments">15,000円</div>
          <p class="dashboard-caption">今月の支払い合計</p>
        </div>
      </div>
    </section>

    '''

s = s[:start] + new_dashboard + s[end:]

css = '''
/* dashboard repair */
.dashboard-next {
  background: #f7f7f7;
  border-radius: 14px;
  padding: 24px 28px;
  margin: 24px 0 32px;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 18px;
  margin-top: 24px;
}

.dashboard-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 14px;
  padding: 22px 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  min-height: 150px;
}

.dashboard-card h3 {
  font-size: 18px;
  line-height: 1.4;
  margin: 0 0 14px;
}

.dashboard-value {
  font-size: 34px;
  font-weight: 800;
  margin: 12px 0;
}

.dashboard-caption {
  color: #666;
  font-size: 14px;
  margin: 0;
}

@media (max-width: 1000px) {
  .dashboard-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .dashboard-cards {
    grid-template-columns: 1fr;
  }
}
'''

if "dashboard repair" not in s:
    s = s.replace("</style>", css + "\n</style>")

p.write_text(s)

print("ダッシュボードを修復しました")
print("バックアップ:", backup)
