from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_register_form_update_auto_backup.html")
backup.write_text(s)

start_id = s.find('id="register"')
if start_id == -1:
    raise SystemExit('id="register" が見つかりません')

start = s.rfind("<section", 0, start_id)
if start == -1:
    raise SystemExit("register section の開始が見つかりません")

diagnosis_id = s.find('id="diagnosis"', start_id)
if diagnosis_id == -1:
    raise SystemExit('id="diagnosis" が見つかりません')

end = s.rfind("<section", 0, diagnosis_id)
if end == -1 or end <= start:
    raise SystemExit("diagnosis section の開始が見つかりません")

new_register = '''<section class="tab-pane" id="register">
      <h2>契約登録</h2>
      <p>パスワード、口座番号、カード番号、暗証番号は入力・保存しないでください。</p>

      <div class="form-note">
        <h3>家族があとで困らないために残す情報</h3>
        <p>金額や支払日だけでなく、解約方法・問い合わせ先・家族に共有するかを記録します。</p>
      </div>

      <label>契約名</label>
      <input type="text" placeholder="例：サプリメント定期便">

      <label>カテゴリ</label>
      <select>
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
      <input type="date">

      <label>支払金額の目安</label>
      <input type="text" placeholder="例：3,000円 / 月">

      <label>自動更新</label>
      <select>
        <option>あり</option>
        <option>なし</option>
        <option>不明</option>
      </select>

      <label>支払元の目印</label>
      <input type="text" placeholder="例：Amazon、KDDI、東京電力">
      <p class="input-warning">口座番号・カード番号・暗証番号は入力しないでください。</p>

      <label>問い合わせ先</label>
      <input type="text" placeholder="例：会社名、電話番号、問い合わせページ名">

      <label>解約方法</label>
      <select>
        <option>アプリ・Webで解約</option>
        <option>電話で解約</option>
        <option>店舗・窓口で解約</option>
        <option>契約書を確認する必要あり</option>
        <option>不明</option>
      </select>

      <label>家族に共有するか</label>
      <select>
        <option>共有する</option>
        <option>まだ共有しない</option>
        <option>確認してから決める</option>
      </select>

      <label>メモ</label>
      <textarea placeholder="例：契約書はリビングのファイルに保管。解約は電話のみ。"></textarea>

      <button class="button">登録</button>
    </section>

    '''

s = s[:start] + new_register + s[end:]

css = '''
/* register form update */
.form-note {
  background: #f7f7f7;
  border-radius: 14px;
  padding: 20px 24px;
  margin: 20px 0 28px;
}

select,
textarea {
  width: 100%;
  max-width: 520px;
  padding: 14px;
  font-size: 18px;
  border: 1px solid #ccc;
  border-radius: 8px;
  display: block;
  margin: 8px 0 18px;
  box-sizing: border-box;
  font-family: inherit;
}

textarea {
  min-height: 110px;
}

.input-warning {
  color: #666;
  font-size: 14px;
  margin-top: -10px;
  margin-bottom: 18px;
}
'''

if "register form update" not in s:
    s = s.replace("</style>", css + "\n</style>")

p.write_text(s)

print("契約登録フォームを更新しました")
print("バックアップ:", backup)
