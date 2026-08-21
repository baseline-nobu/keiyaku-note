from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_share_preview_update_auto_backup.html")
backup.write_text(s)

start_id = s.find('id="preview"')
if start_id == -1:
    raise SystemExit('id="preview" が見つかりません')

start = s.rfind("<section", 0, start_id)
end = s.find("</section>", start)

if start == -1 or end == -1:
    raise SystemExit("preview section の範囲が見つかりません")

end += len("</section>")

new_preview = '''<section class="tab-pane" id="preview">
      <h2>共有プレビュー</h2>

      <div class="share-note">
        <h3>家族に渡すための確認用一覧</h3>
        <p>
          この画面では、本人が「共有する」と選んだ契約だけを表示します。
          パスワード、口座番号、カード番号、暗証番号は表示しません。
        </p>
      </div>

      <table>
        <thead>
          <tr>
            <th>契約名</th>
            <th>カテゴリ</th>
            <th>次回支払日</th>
            <th>自動更新</th>
            <th>支払元の目印</th>
            <th>家族が確認すること</th>
          </tr>
        </thead>
        <tbody id="preview-table-body"></tbody>
      </table>
    </section>'''

s = s[:start] + new_preview + s[end:]

old = """      const previewBody = document.querySelector('#preview tbody');
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
      }"""

new = """      const previewBody = document.getElementById('preview-table-body');
      if (previewBody) {
        previewBody.innerHTML = '';

        const getFamilyCheckPoint = (contract) => {
          const name = contract.name;
          const category = contract.category;

          if (name.includes('サプリ') || category.includes('健康')) {
            return '解約方法と問い合わせ先を確認';
          }

          if (name.includes('ウォーター') || category.includes('生活')) {
            return '休止・解約条件と契約書の保管場所を確認';
          }

          if (name.includes('電気') || name.includes('ガス') || category.includes('住宅')) {
            return '契約名義と問い合わせ先を確認';
          }

          if (name.includes('クラウド') || category.includes('データ')) {
            return '写真やデータを残すか確認';
          }

          if (name.includes('動画') || category.includes('エンタメ')) {
            return '自動更新日と解約ページを確認';
          }

          if (category.includes('通信')) {
            return '契約名義・支払日・解約方法を確認';
          }

          return '問い合わせ先と解約方法を確認';
        };

        const sharedContracts = contracts.filter(contract => contract.share === '共有する');

        sharedContracts.forEach(contract => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${contract.name}</td>
            <td>${contract.category}</td>
            <td>${contract.nextPayment}</td>
            <td>${contract.autoRenew}</td>
            <td>${contract.paymentNote || '未入力'}</td>
            <td>${getFamilyCheckPoint(contract)}</td>
          `;
          previewBody.appendChild(tr);
        });

        if (sharedContracts.length === 0) {
          const tr = document.createElement('tr');
          tr.innerHTML = '<td colspan="6">家族に共有する契約はまだ選ばれていません。</td>';
          previewBody.appendChild(tr);
        }
      }"""

if old not in s:
    raise SystemExit("共有プレビューの描画処理が見つかりません")

s = s.replace(old, new)

css = '''
/* share preview update */
.share-note {
  background: #f7f7f7;
  border-radius: 14px;
  padding: 24px;
  margin: 20px 0 28px;
}

.share-note h3 {
  margin-top: 0;
}

.share-note p {
  margin-bottom: 0;
  line-height: 1.8;
}
'''

if "share preview update" not in s:
    s = s.replace("</style>", css + "\n</style>")

p.write_text(s)

print("共有プレビューを家族向けの確認画面に変更しました")
print("バックアップ:", backup)
