from pathlib import Path

p = Path("public/index.html")
s = p.read_text()

backup = Path("public/index_before_intro_update_auto_backup.html")
backup.write_text(s)

target = '<p>日常は契約備忘録、将来は家族への引継ぎ</p>'

replacement = '''<p>日常は契約備忘録、将来は家族への引継ぎ</p>

    <div class="intro-card">
      <h2>本人しか知らない契約を、家族が困る前に見える化</h2>
      <p>
        サブスク、定期購入、通信、電気・ガス、クラウドサービスなどを整理し、
        家族への共有、引継ぎ診断、公的相談先への案内までつなげます。
      </p>
      <p>
        パスワード、口座番号、カード番号、暗証番号は保存せず、
        家族が手続きに必要な「契約の存在」「支払元の目印」「問い合わせ先」「解約方法」を残します。
      </p>
    </div>'''

if target not in s:
    raise SystemExit("トップ説明文の差し替え位置が見つかりません")

s = s.replace(target, replacement, 1)

css = '''
/* intro update */
.intro-card {
  background: #f7f7f7;
  border-radius: 16px;
  padding: 28px;
  margin: 28px 0 36px;
}

.intro-card h2 {
  margin-top: 0;
  font-size: 28px;
}

.intro-card p {
  line-height: 1.8;
  margin: 12px 0 0;
}
'''

if "intro update" not in s:
    s = s.replace("</style>", css + "\n</style>")

p.write_text(s)

print("トップ説明カードを追加しました")
print("バックアップ:", backup)
