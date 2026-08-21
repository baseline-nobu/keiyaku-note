(function () {
  function renderDashboard() {
    const dashboard = document.getElementById('dashboard');
    if (!dashboard) return;

    dashboard.innerHTML = `
      <h2>ダッシュボード</h2>

      <section class="dashboard-next">
        <h3>次に確認すること</h3>
        <ul>
          <li>契約書の整理</li>
          <li>連絡先の確認</li>
          <li>自動更新設定の見直し</li>
        </ul>
      </section>

      <section class="dashboard-cards">
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
      </section>
    `;
  }

  document.addEventListener('DOMContentLoaded', renderDashboard);
  window.addEventListener('load', renderDashboard);
})();
