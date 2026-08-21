document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab-btn');
  const panes = document.querySelectorAll('.tab-pane');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      panes.forEach(p => p.classList.remove('active'));
      
      tab.classList.add('active');
      document.getElementById(tab.dataset.tab).classList.add('active');
  // ダッシュボードデータの初期化
  const totalContracts = dummyContracts.length;
  const unawareContracts = dummyContracts.filter(c => c.status === '未確認').length;
  const autoRenewals = dummyContracts.filter(c => c.autoRenew === 'あり').length;
  
  document.getElementById('total-contracts').textContent = totalContracts;
  document.getElementById('readiness-score').textContent = '65%';
  document.getElementById('unaware-contracts').textContent = unawareContracts;
  document.getElementById('auto-renewals').textContent = autoRenewals;
  document.getElementById('monthly-payments').textContent = '15,000円';
});
  });

  // ダミーデータの初期化
  const dummyContracts = [
  { name: 'サプリメント定期便', category: '健康', nextPayment: '2023/09/15', autoRenew: 'あり', paymentNote: 'Amazon', status: '未確認' },
  { name: '動画配信サービス', category: 'エンタメ', nextPayment: '2023/09/20', autoRenew: 'あり', paymentNote: 'Netflix', status: '確認済み' },
  { name: 'スマートフォン契約', category: '通信', nextPayment: '2023/09/25', autoRenew: 'なし', paymentNote: 'KDDI', status: '未確認' },
  { name: 'クラウド写真保存', category: 'データ', nextPayment: '2023/09/10', autoRenew: 'あり', paymentNote: 'Google Drive', status: '確認済み' },
  { name: 'ウォーターサーバー', category: '生活', nextPayment: '2023/09/18', autoRenew: 'あり', paymentNote: 'ウォーターサーバー', status: '未確認' },
  { name: '電気・ガス契約', category: '住宅', nextPayment: '2023/09/30', autoRenew: 'あり', paymentNote: '東京電力', status: '確認済み' },

]

  // 契約一覧の表示
  const tableBody = document.querySelector('#contracts-table tbody');
  dummyContracts.forEach(contract => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${contract.name}</td>
      <td>${contract.category}</td>
      <td>${contract.nextPayment}</td>
      <td>${contract.autoRenew}</td>
      <td>${contract.paymentNote}</td>
      <td>${contract.status}</td>
    `;
    tableBody.appendChild(row);
  });

  // ダッシュボードデータの初期化
  // Create dashboard cards\nconst cardContainer = document.getElementById('dashboard-card');\ncardContainer.className = 'card-container';\n\ndummyContracts.forEach(contract => {\n  const card = document.getElementById('dashboard-card');\n  card.className = 'card';\n  card.innerHTML = `\n    <h3>${contract.name}</h3>\n    <p>カテゴリ: ${contract.category}</p>\n    <p>次回支払い: ${contract.nextPayment}</p>\n    <p>自動更新: ${contract.autoRenew}</p>\n    <p>支払い先: ${contract.paymentNote}</p>\n    <p>状態: ${contract.status}</p>\n  `;\n  cardContainer.appendChild(card);\n});\n\ndocument.querySelector('.container').appendChild(cardContainer);



  

});