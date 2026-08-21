from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_diagnosis_priority_update_auto_backup.html")
backup.write_text(s)

old = """    function updateDiagnosis() {
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
    }"""

new = """    function updateDiagnosis() {
      const priorityContracts = contracts.filter(contract => {
        return contract.status === '未確認' && contract.autoRenew === 'あり';
      });

      const recommendedContracts = contracts.filter(contract => {
        return !(contract.status === '未確認' && contract.autoRenew === 'あり') &&
               (contract.autoRenew === 'あり' || contract.cancelMethod === '不明');
      });

      const total = contracts.length;
      const unaware = contracts.filter(c => c.status === '未確認').length;
      const readiness = total === 0 ? 0 : Math.round(((total - unaware) / total) * 100);

      const readinessEl = document.getElementById('diagnosis-readiness');
      const riskCountEl = document.getElementById('diagnosis-risk-count');
      const listEl = document.getElementById('diagnosis-list');

      if (readinessEl) readinessEl.textContent = readiness + '%';
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
        };

        const priorityTitle = document.createElement('h3');
        priorityTitle.textContent = '優先して確認する契約';
        priorityTitle.className = 'diagnosis-section-title';
        listEl.appendChild(priorityTitle);

        if (priorityContracts.length === 0) {
          const p = document.createElement('p');
          p.textContent = '優先して確認する契約はありません。';
          listEl.appendChild(p);
        } else {
          priorityContracts.forEach(contract => {
            listEl.appendChild(makeCard(contract, '優先確認'));
          });
        }

        const recommendedTitle = document.createElement('h3');
        recommendedTitle.textContent = '確認しておくと安心な契約';
        recommendedTitle.className = 'diagnosis-section-title';
        listEl.appendChild(recommendedTitle);

        if (recommendedContracts.length === 0) {
          const p = document.createElement('p');
          p.textContent = '確認推奨の契約はありません。';
          listEl.appendChild(p);
        } else {
          recommendedContracts.forEach(contract => {
            listEl.appendChild(makeCard(contract, '確認推奨'));
          });
        }
      }
    }"""

if old not in s:
    raise SystemExit("updateDiagnosis の差し替え位置が見つかりません")

s = s.replace(old, new)

css = """
/* diagnosis priority update */
.diagnosis-section-title {
  grid-column: 1 / -1;
  margin: 10px 0 0;
  font-size: 24px;
}
"""

if "diagnosis priority update" not in s:
    s = s.replace("</style>", css + "\n</style>")

p.write_text(s)

print("引継ぎ診断を優先確認と確認推奨の2段階表示に変更しました")
print("バックアップ:", backup)
