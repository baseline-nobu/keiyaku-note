import fileinput

with fileinput.FileInput('public/index.html', inplace=True) as f:
    for line in f:
        if 'dashboard-area' in line:
            print('\n    <div class=\"dashboard-cards\">\n      <div id=\"total-contracts\">\n        <h3>総契約数</h3>\n        <p>123契約</p>\n      </div>\n      <div id=\"readiness-score\">\n        <h3>引継ぎ準備度</h3>\n        <p>85%</p>\n      </div>\n      <div id=\"unaware-contracts\">\n        <h3>家族が把握していない契約</h3>\n        <p>15契約</p>\n      </div>\n      <div id=\"auto-renewals\">\n        <h3>自動更新あり</h3>\n        <p>28契約</p>\n      </div>\n      <div id=\"monthly-payments\">\n        <h3>今月支払い予定</h3>\n        <p>¥150,000</p>\n      </div>\n    </div>')
        else:
            print(line, end='')

with fileinput.FileInput('public/style.css', inplace=True) as f:
    for line in f:
        if '.dashboard-cards' in line:
            print('.dashboard-cards { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; }')
        else:
            print(line, end='')

print('Dashboard修正: ダッシュボードHTMLを静的コンテンツに置換し、CSSをグリッドレイアウトに変更しました。')