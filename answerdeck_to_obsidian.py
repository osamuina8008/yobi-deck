#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
答案デッキ → Obsidian 連携スクリプト
====================================
答案デッキ（自作版）の ⇅ バックアップで書き出した JSON を読み込み、
演習メモのある問題を Obsidian Vault に 1問=1ファイルの Markdown で展開します。

使い方:
    1) 答案デッキの ⇅ ボタン →「ファイル保存」で JSON を保存
       （例: ~/Downloads/answer-deck_2026-08-25.json）
    2) このスクリプトに JSON を渡して実行:
         python3 answerdeck_to_obsidian.py ~/Downloads/answer-deck_2026-08-25.json
       出力先を変えたいときは第2引数でフォルダ指定:
         python3 answerdeck_to_obsidian.py export.json "/path/to/出力フォルダ"

- 既定の出力先は下の OUTPUT_DIR。無ければ自動作成します。
- 演習メモが空の問題（公式問題そのまま）は書き出しません（--all で全問出力）。
- 既存ファイルは上書きします（手編集を残したい場合は出力先を分けてください）。
"""
import json, sys, os, re, datetime

# ▼ 出力先（必要なら書き換えてください）。CLAUDE.md の正式 Vault ルート配下。
OUTPUT_DIR = ("/Users/osamuinagaki/Documents/ObsidianVault/"
              "Time based-司法試験予備試験/TimeBase/20_Study/答案デッキ")

def slug(s):
    return re.sub(r'[\\/:*?"<>|\s]+', '_', str(s)).strip('_')

def md_for(p, work):
    w = work.get(p["id"], {})
    yl = p.get("yearLabel") or p.get("year") or "自作"
    tags = p.get("tags") or []
    L = []
    # frontmatter
    L.append("---")
    L.append(f'title: "{yl} 予備 {p["subject"]}"')
    L.append(f'年度: "{yl}"')
    L.append(f'科目: "{p["subject"]}"')
    if tags:
        L.append("論点: [" + ", ".join(f'"{t}"' for t in tags) + "]")
    if p.get("source"):
        L.append(f'出典: "{p["source"]}"')
    L.append(f'更新: {datetime.date.today().isoformat()}')
    L.append("tags: [答案デッキ, 予備試験, " + slug(p["subject"]) + "]")
    L.append("---")
    L.append("")
    L.append(f"# {yl} 予備 {p['subject']}")
    if p.get("title"):
        L.append(f"**{p['title']}**")
    if p.get("hook"):
        L.append(f"> 🔴 社会的フック：{p['hook']}")
    L.append("")
    L.append("## 問題文")
    L.append(p.get("statement") or "（未入力）")
    L.append("")

    def sec(title, val):
        if val and str(val).strip():
            L.append(f"## {title}")
            L.append(str(val).strip())
            L.append("")

    sec("一行問題・論点想起", w.get("think"))
    sec("知識チェック（思い出せた／曖昧な点）", w.get("check"))
    srcs = w.get("sources") or []
    if srcs:
        L.append("## 資料（法文・判例・PDF・動画）")
        for s in srcs:
            line = f"- [{s.get('kind','')}] {s.get('label','')}"
            if s.get("url"):
                line += f" {s['url']}"
            if s.get("note"):
                line += f" — {s['note']}"
            L.append(line)
        L.append("")
    sec("事例の整理（事実 → 法的意味）", w.get("seireki"))
    sec("答案構成", w.get("kousei"))
    sec("起案", w.get("kian"))
    sec("復習：思い出せなかった点", w.get("review"))
    steps = w.get("steps") or []
    done = sum(1 for x in steps if x)
    L.append(f"---\n進捗：{done}/6 ステップ完了")
    if w.get("last"):
        ts = datetime.datetime.fromtimestamp(w["last"] / 1000).strftime("%Y-%m-%d %H:%M")
        L.append(f"最終更新：{ts}")
    return "\n".join(L) + "\n"

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    src = os.path.expanduser(sys.argv[1])
    out = os.path.expanduser(sys.argv[2]) if len(sys.argv) > 2 else OUTPUT_DIR
    want_all = "--all" in sys.argv

    with open(src, encoding="utf-8") as f:
        db = json.load(f)
    problems = db.get("problems", [])
    work = db.get("work", {})
    os.makedirs(out, exist_ok=True)

    def has_work(pid):
        w = work.get(pid)
        if not w:
            return False
        return bool(w.get("think") or w.get("check") or w.get("seireki")
                    or w.get("kousei") or w.get("kian") or w.get("review")
                    or (w.get("sources")) or any(w.get("steps") or []))

    written = 0
    index = ["# 答案デッキ インデックス", f"_更新: {datetime.date.today().isoformat()}_", ""]
    for p in problems:
        if not want_all and not has_work(p["id"]):
            continue
        yl = p.get("yearLabel") or p.get("year") or "自作"
        fname = f"{slug(yl)}_{slug(p['subject'])}.md"
        with open(os.path.join(out, fname), "w", encoding="utf-8") as f:
            f.write(md_for(p, work))
        done = sum(1 for x in (work.get(p["id"], {}).get("steps") or []) if x)
        index.append(f"- [[{fname[:-3]}]] — {yl} {p['subject']}（{done}/6）")
        written += 1

    with open(os.path.join(out, "_index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index) + "\n")

    print(f"✅ 出力完了: {written} 件")
    print(f"   出力先: {out}")
    if written == 0:
        print("   （演習メモのある問題がありません。全問出したい場合は末尾に --all を付けてください）")

if __name__ == "__main__":
    main()
