from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_diagnosis_action_text_update_auto_backup.html")
backup.write_text(s)

old = """      if (readinessEl) readinessEl.textContent = readiness + '%';
      if (riskCountEl) riskCountEl.textContent = priorityContracts.length + '件';

      if (listEl) {
        listEl.innerHTML = '';

        const makeCard = (contract, levelText) => {
          const reasons = [];

          if (contract.status === '未確認') reasons.push('家族が未確認');
          if (contract.autoRenew === 'あり') reasons.push('自動更新あり');
          if (contract.cancelMethod === '不明') reasons.push('解約方法不明');
          if (!contract.paymentNote || contract.paymentNote === '未入力') reasons.push('支払元が未入力');

          const div = document.createElement('div');
          div.className = 'diagnosis-item';
          div.innerHTML = `
            <h4>${contract.name}</h4>
            <p><strong>区分：</strong>${levelText}</p>
            <p><strong>カテゴリ：</strong>${contract.category}</p>
            <p><strong>次回支払日：</strong>${contract.nextPayment}</p>
            <p><strong>確認理由：</strong></p>
            <div>${reasons.map(reason => `<span class="diagnosis-badge">${reason}</span>`).join('')}</div>
            <p><strong>次の行動：</strong>問い合わせ先・解約方法・家族共有の有無を確認してください。</p>
          `;
          return div;
        };"""

new = """      if (readinessEl) readinessEl.textContent = readiness + '%';
      if (riskCountEl) riskCountEl.textContent = priorityContracts.length + '件';

      const readinessComment = document.getElementById('diagnosis-readiness-comment');
      if (readinessComment) {
        readinessComment.textContent =
          `家族が把握していない契約が${unaware}件あります。まずは自動更新がある契約から確認しましょう。`;
      }

      if (listEl) {
        listEl.innerHTML = '';

        const getNextAction = (contract) => {
          const name = contract.name;
          const category = contract.category;

          if (name.includes('サプリ') || category.includes('健康')) {
            return '解約方法と問い合わせ先を確認し、家族に共有する対象にしましょう。';
          }

          if (name.includes('ウォーター') || category.includes('生活')) {
            return '自動更新日、休止・解約条件、契約書の保管場所をメモしましょう。';
          }

          if (name.includes('動画') || category.includes('エンタメ')) {
            return '家族共有は急がなくてもよいですが、自動更新日と解約ページを確認しましょう。';
          }

          if (name.includes('クラウド') || category.includes('データ')) {
            return '写真やデータが残るため、家族に共有するか、解約せず残すかを確認しましょう。';
          }

          if (name.includes('電気') || name.includes('ガス') || category.includes('住宅')) {
            return '生活インフラなので、契約名義・問い合わせ先・停止手続きの流れを確認しましょう。';
          }

          if (category.includes('通信')) {
            return '契約名義、支払日、解約方法、店舗または問い合わせ先を確認しましょう。';
          }

          return '問い合わせ先・解約方法・家族共有の有無を確認しましょう。';
        };

        const makeCard = (contract, levelText) => {
          const reasons = [];

          if (contract.status === '未確認') reasons.push('家族が未確認');
          if (contract.autoRenew === 'あり') reasons.push('自動更新あり');
          if (contract.cancelMethod === '不明') reasons.push('解約方法不明');
          if (!contract.paymentNote || contract.paymentNote === '未入力') reasons.push('支払元が未入力');

          const div = document.createElement('div');
          div.className = 'diagnosis-item';
          div.innerHTML = `
            <h4>${contract.name}</h4>
            <p><strong>区分：</strong>${levelText}</p>
            <p><strong>カテゴリ：</strong>${contract.category}</p>
            <p><strong>次回支払日：</strong>${contract.nextPayment}</p>
            <p><strong>確認理由：</strong></p>
            <div>${reasons.map(reason => `<span class="diagnosis-badge">${reason}</span>`).join('')}</div>
            <p><strong>次の行動：</strong>${getNextAction(contract)}</p>
          `;
          return div;
        };"""

if old not in s:
    raise SystemExit("診断カード生成部分の差し替え位置が見つかりません")

s = s.replace(old, new)

s = s.replace(
    '<p>家族が契約を把握できる状態にどれだけ近いかを表示します。</p>',
    '<p>家族が契約を把握できる状態にどれだけ近いかを表示します。</p>\n          <p id="diagnosis-readiness-comment" class="diagnosis-comment"></p>'
)

css = """
/* diagnosis action text update */
.diagnosis-comment {
  font-weight: 700;
  color: #333;
  margin-top: 12px;
}
"""

if "diagnosis action text update" not in s:
    s = s.replace("</style>", css + "\n</style>")

p.write_text(s)

print("診断カードの次の行動をカテゴリ別に変更しました")
print("引継ぎ準備度の下にコメントを追加しました")
print("バックアップ:", backup)
