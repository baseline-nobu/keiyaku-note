from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_diagnosis_text_update_auto_backup.html")
backup.write_text(s)

s = s.replace(
    "<h3>確認が必要な契約</h3>\n          <div class=\"diagnosis-score\" id=\"diagnosis-risk-count\">3件</div>\n          <p>未確認・自動更新あり・解約方法不明の契約を優先して確認します。</p>",
    "<h3>優先確認が必要な契約</h3>\n          <div class=\"diagnosis-score\" id=\"diagnosis-risk-count\">3件</div>\n          <p>家族が未確認で、自動更新がある契約を優先して確認します。</p>"
)

s = s.replace(
    "\n      <h3>確認が必要な契約</h3>\n      <div id=\"diagnosis-list\" class=\"diagnosis-list\"></div>",
    "\n      <div id=\"diagnosis-list\" class=\"diagnosis-list\"></div>"
)

p.write_text(s)

print("診断画面の文言を調整しました")
print("バックアップ:", backup)
