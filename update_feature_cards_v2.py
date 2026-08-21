from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_feature_cards_update_v2_auto_backup.html")
backup.write_text(s)

feature_cards = '''
    <div class="feature-cards">
      <div class="feature-card">
        <h3>契約を見える化</h3>
        <p>サブスク、定期購入、通信、生活インフラなど、本人しか把握していない契約を一覧化します。</p>
      </div>

      <div class="feature-card">
        <h3>家族への引継ぎ診断</h3>
        <p>家族が未確認の契約や自動更新の契約を見つけ、優先して確認する契約を表示します。</p>
      </div>

      <div class="feature-card">
        <h3>困った時の相談ナビ</h3>
        <p>解約できない、請求が続く、契約が分からない時に、公的相談先へつなげます。</p>
      </div>
    </div>
'''

if "feature-cards" not in s:
    target = '<section class="tab-pane active" id="dashboard">'
    if target not in s:
        raise SystemExit("dashboard section の開始位置が見つかりません")
    s = s.replace(target, feature_cards + "\n" + target, 1)

css = '''
/* feature cards update */
.feature-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin: 28px 0 36px;
}

.feature-card {
  background: #f7f7f7;
  border-radius: 16px;
  padding: 24px;
}

.feature-card h3 {
  margin-top: 0;
  font-size: 22px;
}

.feature-card p {
  line-height: 1.7;
  margin-bottom: 0;
}

@media (max-width: 900px) {
  .feature-cards {
    grid-template-columns: 1fr;
  }
}
'''

if "feature cards update" not in s:
    s = s.replace("</style>", css + "\n</style>")

p.write_text(s)

print("トップに特徴カードを追加しました")
print("バックアップ:", backup)
