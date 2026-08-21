from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_diagnosis_update_auto_backup.html")
backup.write_text(s)

start_id = s.find('id="diagnosis"')
if start_id == -1:
    raise SystemExit('id="diagnosis" が見つかりません')

start = s.rfind("<section", 0, start_id)
opendata_id = s.find('id="opendata"', start_id)
end = s.rfind("<section", 0, opendata_id)

if start == -1 or end == -1 or end <= start:
    raise SystemExit("diagnosis section の範囲が見つかりません")

new_diagnosis = '''<section class="tab-pane" id="diagnosis">
      <h2>引継ぎ診断</h2>

      <div class="diagnosis-summary">
        <div>
          <h3>引継ぎ準備度</h3>
          <div class="diagnosis-score" id="diagnosis-readiness">50%</div>
          <p>家族が契約を把握できる状態にどれだけ近いかを表示します。</p>
        </div>

        <div>
          <h3>確認が必要な契約</h3>
          <div class="diagnosis-score" id="diagnosis-risk-count">3件</div>
          <p>未確認・自動更新あり・解約方法不明の契約を優先して確認します。</p>
        </div>
      </div>

      <h3>確認が必要な契約</h3>
      <div id="diagnosis-list" class="diagnosis-list"></div>

      <div class="diagnosis-next-action">
        <h3>次にやること</h3>
        <ol>
          <li>自動更新の契約を確認する</li>
          <li>問い合わせ先・解約方法を記録する</li>
          <li>家族に共有する契約を選ぶ</li>
          <li>困った場合はオープンデータの相談ナビを確認する</li>
        </ol>
        <button class="button" data-tab-jump="opendata" type="button">相談ナビを見る</button>
      </div>
    </section>

    '''

s = s[:start] + new_diagnosis + s[end:]

css = '''
/* diagnosis update */
.diagnosis-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin: 24px 0 32px;
}

.diagnosis-summary > div,
.diagnosis-item,
.diagnosis-next-action {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.diagnosis-score {
  font-size: 40px;
  font-weight: 900;
  margin: 8px 0;
}

.diagnosis-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
  margin: 18px 0 32px;
}

.diagnosis-item h4 {
  font-size: 22px;
  margin: 0 0 8px;
}

.diagnosis-badge {
  display: inline-block;
  background: #fff3cd;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 14px;
  font-weight: 700;
  margin: 4px 6px 8px 0;
}

.diagnosis-item p {
  margin: 8px 0;
}

.diagnosis-next-action {
  background: #f7f7f7;
}

@media (max-width: 900px) {
  .diagnosis-summary,
  .diagnosis-list {
    grid-template-columns: 1fr;
  }
}
'''

if "diagnosis update" not in s:
    s = s.replace("</style>", css + "\n</style>")

old = "    renderTables();\n    updateDashboard();\n  </script>"
new = """    function updateDiagnosis() {
      const riskContracts = contracts.filter(contract => {
        return contract.status === '未確認' || contract.autoRenew === 'あり' || contract.cancelMethod === '不明';
      });

      const total = contracts.length;
      const unaware = contracts.filter(c => c.status === '未確認').length;
      const readiness = total === 0 ? 0 : Math.round(((total - unaware) / total) * 100);

      const readinessEl = document.getElementById('diagnosis-readiness');
      const riskCountEl = document.getElementById('diagnosis-risk-count');
      const listEl = document.getElementById('diagnosis-list');

      if (readinessEl) readinessEl.textContent = readiness + '%';
      if (riskCountEl) riskCountEl.textContent = riskContracts.length + '件';

      if (listEl) {
        listEl.innerHTML = '';

        riskContracts.forEach(contract => {
          const reasons = [];

          if (contract.status === '未確認') reasons.push('家族が未確認');
          if (contract.autoRenew === 'あり') reasons.push('自動更新あり');
          if (contract.cancelMethod === '不明') reasons.push('解約方法不明');
          if (!contract.paymentNote || contract.paymentNote === '未入力') reasons.push('支払元が未入力');

          const div = document.createElement('div');
          div.className = 'diagnosis-item';
          div.innerHTML = `
            <h4>${contract.name}</h4>
            <p><strong>カテゴリ：</strong>${contract.category}</p>
            <p><strong>次回支払日：</strong>${contract.nextPayment}</p>
            <p><strong>確認理由：</strong></p>
            <div>${reasons.map(reason => `<span class="diagnosis-badge">${reason}</span>`).join('')}</div>
            <p><strong>次の行動：</strong>問い合わせ先・解約方法・家族共有の有無を確認してください。</p>
          `;
          listEl.appendChild(div);
        });

        if (riskContracts.length === 0) {
          listEl.innerHTML = '<p>確認が必要な契約はありません。</p>';
        }
      }
    }

    renderTables();
    updateDashboard();
    updateDiagnosis();
  </script>"""

if old not in s:
    raise SystemExit("script末尾の差し替え位置が見つかりません")

s = s.replace(old, new)

# registerContract 内で診断も更新
s = s.replace(
    "      renderTables();\n      updateDashboard();\n      clearRegisterForm();",
    "      renderTables();\n      updateDashboard();\n      updateDiagnosis();\n      clearRegisterForm();"
)

p.write_text(s)

print("引継ぎ診断画面を更新しました")
print("バックアップ:", backup)
