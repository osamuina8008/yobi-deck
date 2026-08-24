# 予備デッキ（答案デッキ・短答デッキ）

司法試験予備試験の過去問を、隙間時間に学習するための自作ツールです。
外部サーバー・APIを使わない **単一HTML** で、演習データは各自のブラウザ内（localStorage）にのみ保存されます。

## 収録

| ツール | 内容 |
|--------|------|
| **答案デッキ**（`ronbun.html`） | 令和元年〜令和7年 論文式 全63問（憲法/行政法/民法/商法/民訴/刑法/刑訴/実務基礎）。問題文を見ながら6ステップで構成→起案→復習。科目・年度・キーワード検索、出題傾向の社会的フック分析つき。 |
| **短答デッキ**（`tanto.html`） | 令和7年 短答式 95問（法律7科目）。左に問題・右に解答解説。正解の自動採点と「できた/曖昧/できない」で弱点を回す。 |

問題文・正解・配点は **法務省の公表資料** に基づきます（各問に出典PDFへのリンクあり）。

## 使い方

- `index.html` をブラウザで開くと、2つのツールへのランディングが出ます。
- そのままローカルで開いてもOK（`ronbun.html` / `tanto.html` を直接ダブルクリック）。
- データは端末ごとのブラウザに保存されます。端末移行・バックアップは各ツールの **⇅** ボタンからJSONで。

## GitHub Pages で公開する

```bash
gh repo create yobi-deck --public --source=. --push
gh api repos/:owner/yobi-deck/pages -f "source[branch]=main" -f "source[path]=/"
```

→ `https://<ユーザー名>.github.io/yobi-deck/` で開けます。

## Obsidian 連携

`answerdeck_to_obsidian.py` … 答案デッキの ⇅ で書き出したJSONを渡すと、演習メモを Obsidian Vault に 1問=1.md で展開します。

```bash
python3 answerdeck_to_obsidian.py ~/Downloads/answer-deck_YYYY-MM-DD.json
```

出力先はスクリプト冒頭の `OUTPUT_DIR` で変更できます。

## ライセンス / 注意

- 問題文等は法務省公表の試験問題（公的資料）に基づく学習用の再構成です。図・別紙を含む問題は図をテキスト化できないため、公式PDFリンクを併記しています。
- 個人学習用。演習データの送信・収集は行いません。
