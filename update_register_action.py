from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_register_action_auto_backup.html")
backup.write_text(s)

# register section を差し替え
start_id = s.find('id="register"')
if start_id == -1:
    raise SystemExit('id="register" が見つかりません')

start = s.rfind("<section", 0, start_id)
diagnosis_id = s.find('id="diagnosis"', start_id)
end = s.rfind("<section", 0, diagnosis_id)

if start == -1 or end == -1 or end <= start:
    raise SystemExit("register section の範囲が見つかりません")

new_register = '''<section class="tab-pane" id="register">
      <h2>契約登録</h2>
      <p>パスワード、口座番号、カード番号、暗証番号は入力・保存しないでください。</p>

      <div class="form-note">
        <h3>家族があとで困らないために残す情報</h3>
        <p>金額や支払日だけでなく、解約方法・問い合わせ先・家族に共有するかを記録します。</p>
      </div>

      <label>契約名</label>
      <input id="contract-name" type="text" placeholder="例：サプリメント定期便">

      <label>カテゴリ</label>
      <select id="contract-category">
        <option>健康・サプリ</option>
        <option>動画・音楽配信</option>
        <option>通信・スマートフォン</option>
        <option>電気・ガス・水道</option>
        <option>クラウド・データ保存</option>
        <option>通販・定期購入</option>
        <option>保険・住宅</option>
        <option>その他</option>
      </select>

      <label>次回支払日</label>
      <input id="contract-next-payment" type="date">

      <label>支払金額の目安</label>
      <input id="contract-amount" type="text" placeholder="例：3,000円 / 月">

      <label>自動更新</label>
      <select id="contract-auto-renew">
        <option>あり</option>
        <option>なし</option>
        <option>不明</option>
      </select>

      <label>支払元の目印</label>
      <input id="contract-payment-note" type="text" placeholder="例：Amazon、KDDI、東京電力">
      <p class="input-warning">口座番号・カード番号・暗証番号は入力しないでください。</p>

      <label>問い合わせ先</label>
      <input id="contract-contact" type="text" placeholder="例：会社名、電話番号、問い合わせページ名">

      <label>解約方法</label>
      <select id="contract-cancel-method">
        <option>アプリ・Webで解約</option>
        <option>電話で解約</option>
        <option>店舗・窓口で解約</option>
        <option>契約書を確認する必要あり</option>
        <option>不明</option>
      </select>

      <label>家族に共有するか</label>
      <select id="contract-share">
        <option>共有する</option>
        <option>まだ共有しない</option>
        <option>確認してから決める</option>
      </select>

      <label>メモ</label>
      <textarea id="contract-memo" placeholder="例：契約書はリビングのファイルに保管。解約は電話のみ。"></textarea>

      <button class="button" id="register-button" type="button">登録</button>

      <p id="register-message" class="register-message"></p>
    </section>

    '''

s = s[:start] + new_register + s[end:]

# script 全体を差し替え
script_start = s.find("<script>")
script_end = s.rfind("</script>")

if script_start == -1 or script_end == -1:
    raise SystemExit("script タグが見つかりません")

script_end += len("</script>")

new_script = '''<script>
    const contracts = [
      { name: 'サプリメント定期便', category: '健康', nextPayment: '2023/09/15', autoRenew: 'あり', paymentNote: 'Amazon', status: '未確認', share: '共有する', amount: '3,000円' },
      { name: '動画配信サービス', category: 'エンタメ', nextPayment: '2023/09/20', autoRenew: 'あり', paymentNote: 'Netflix', status: '確認済み', share: '共有する', amount: '1,500円' },
      { name: 'スマートフォン契約', category: '通信', nextPayment: '2023/09/25', autoRenew: 'なし', paymentNote: 'KDDI', status: '未確認', share: '確認してから決める', amount: '7,000円' },
      { name: 'クラウド写真保存', category: 'データ', nextPayment: '2023/09/10', autoRenew: 'あり', paymentNote: 'Google Drive', status: '確認済み', share: 'まだ共有しない', amount: '300円' },
      { name: 'ウォーターサーバー', category: '生活', nextPayment: '2023/09/18', autoRenew: 'あり', paymentNote: 'ウォーターサーバー', status: '未確認', share: '共有する', amount: '3,500円' },
      { name: '電気・ガス契約', category: '住宅', nextPayment: '2023/09/30', autoRenew: 'あり', paymentNote: '東京電力', status: '確認済み', share: '共有する', amount: '15,000円' }
    ];

    function showTab(tabName) {
      document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.toggle('active', button.dataset.tab === tabName);
      });

      document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.toggle('active', pane.id === tabName);
      });
    }

    function yenToNumber(text) {
      if (!text) return 0;
      const n = String(text).replace(/[円,\\s]/g, '').match(/\\d+/);
      return n ? Number(n[0]) : 0;
    }

    function formatYen(value) {
      return value.toLocaleString('ja-JP') + '円';
    }

    function formatDate(value) {
      if (!value) return '未入力';
      return value.replaceAll('-', '/');
    }

    function normalizeCategory(category) {
      if (category.includes('健康')) return '健康';
      if (category.includes('動画')) return 'エンタメ';
      if (category.includes('通信')) return '通信';
      if (category.includes('電気')) return '住宅';
      if (category.includes('クラウド')) return 'データ';
      if (category.includes('通販')) return '通販';
      if (category.includes('保険')) return '保険';
      return category;
    }

    function renderTables() {
      const contractBody = document.querySelector('#contracts tbody');
      if (contractBody) {
        contractBody.innerHTML = '';
        contracts.forEach(contract => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${contract.name}</td>
            <td>${contract.category}</td>
            <td>${contract.nextPayment}</td>
            <td>${contract.autoRenew}</td>
            <td>${contract.paymentNote || '未入力'}</td>
            <td>${contract.status}</td>
          `;
          contractBody.appendChild(tr);
        });
      }

      const previewBody = document.querySelector('#preview tbody');
      if (previewBody) {
        previewBody.innerHTML = '';
        contracts
          .filter(contract => contract.share === '共有する')
          .slice(0, 5)
          .forEach(contract => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>${contract.name}</td>
              <td>${contract.category}</td>
              <td>${contract.nextPayment}</td>
              <td>${contract.autoRenew}</td>
            `;
            previewBody.appendChild(tr);
          });
      }
    }

    function setDashboardValue(title, value) {
      const cards = document.querySelectorAll('.dashboard-card');
      cards.forEach(card => {
        const h3 = card.querySelector('h3');
        const valueEl = card.querySelector('.dashboard-value');
        if (h3 && valueEl && h3.textContent.trim() === title) {
          valueEl.textContent = value;
        }
      });
    }

    function updateDashboard() {
      const total = contracts.length;
      const autoRenewals = contracts.filter(c => c.autoRenew === 'あり').length;
      const unaware = contracts.filter(c => c.status === '未確認').length;
      const monthlyTotal = contracts.reduce((sum, c) => sum + yenToNumber(c.amount), 0);

      const readiness = total === 0 ? 0 : Math.round(((total - unaware) / total) * 100);

      setDashboardValue('総契約数', String(total));
      setDashboardValue('引継ぎ準備度', readiness + '%');
      setDashboardValue('家族が把握していない契約', unaware + '件');
      setDashboardValue('自動更新あり', autoRenewals + '件');
      setDashboardValue('今月支払い予定', formatYen(monthlyTotal));
    }

    function clearRegisterForm() {
      document.getElementById('contract-name').value = '';
      document.getElementById('contract-next-payment').value = '';
      document.getElementById('contract-amount').value = '';
      document.getElementById('contract-payment-note').value = '';
      document.getElementById('contract-contact').value = '';
      document.getElementById('contract-memo').value = '';
      document.getElementById('contract-category').selectedIndex = 0;
      document.getElementById('contract-auto-renew').selectedIndex = 0;
      document.getElementById('contract-cancel-method').selectedIndex = 0;
      document.getElementById('contract-share').selectedIndex = 0;
    }

    function registerContract() {
      const name = document.getElementById('contract-name').value.trim();
      const category = document.getElementById('contract-category').value;
      const nextPayment = document.getElementById('contract-next-payment').value;
      const amount = document.getElementById('contract-amount').value.trim();
      const autoRenew = document.getElementById('contract-auto-renew').value;
      const paymentNote = document.getElementById('contract-payment-note').value.trim();
      const contact = document.getElementById('contract-contact').value.trim();
      const cancelMethod = document.getElementById('contract-cancel-method').value;
      const share = document.getElementById('contract-share').value;
      const memo = document.getElementById('contract-memo').value.trim();
      const message = document.getElementById('register-message');

      if (!name) {
        message.textContent = '契約名を入力してください。';
        message.classList.add('error');
        return;
      }

      contracts.push({
        name,
        category: normalizeCategory(category),
        nextPayment: formatDate(nextPayment),
        autoRenew,
        paymentNote: paymentNote || '未入力',
        status: share === '共有する' ? '確認済み' : '未確認',
        share,
        amount,
        contact,
        cancelMethod,
        memo
      });

      renderTables();
      updateDashboard();
      clearRegisterForm();

      message.textContent = '契約を登録しました。契約一覧とダッシュボードに反映しました。';
      message.classList.remove('error');

      showTab('contracts');
    }

    document.querySelectorAll('.tab-button').forEach(button => {
      button.addEventListener('click', () => showTab(button.dataset.tab));
    });

    document.querySelectorAll('[data-tab-jump]').forEach(button => {
      button.addEventListener('click', () => showTab(button.dataset.tabJump));
    });

    const registerButton = document.getElementById('register-button');
    if (registerButton) {
      registerButton.addEventListener('click', registerContract);
    }

    renderTables();
    updateDashboard();
  </script>'''

s = s[:script_start] + new_script + s[script_end:]

css = '''
/* register action update */
.register-message {
  margin-top: 16px;
  font-weight: 700;
  color: #43ad4f;
}

.register-message.error {
  color: #c0392b;
}
'''

if "register action update" not in s:
    s = s.replace("</style>", css + "\n</style>")

p.write_text(s)

print("登録ボタンで契約一覧・共有プレビュー・ダッシュボードに反映する処理を追加しました")
print("バックアップ:", backup)
