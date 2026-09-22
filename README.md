# 回路のきほん — CIRCUIT NOTES

電子回路・電子部品・電子計測を日本語で学ぶ、静的な入門教材サイトです。「部品の名前を知る」から、回路図を読み、安全に測り、故障を切り分け、仕様から簡単な回路を設計するところまでを扱います。

直感的な説明 → 技術的な説明 → 数値例 → 実測／故障という順で構成。設計演習は要求仕様を先に提示し、設計例を折りたたんでいます。全53教材に答え・解説付きの理解度チェックがあります。

## 技術構成

- Astro 7 / TypeScript strict、全ページ静的生成。
- Astro Content Collections（glob loader + `astro/zod`）でMarkdownのメタデータを検証。
- Vanilla CSSと小さなブラウザー用TypeScript。React等のUIフレームワークなし。
- 検索はビルド時生成のJSONを検索ページでのみ取得。日本語の部分一致、NFKC正規化、空白区切りAND検索、章の絞り込み、検索URLをサポート。
- テーマ設定のみlocalStorageへ保存。アカウント、外部API、アクセス解析、外部フォントなし。
- 自作SVG 22点とトップのRC図。画像生成モデルや外部画像は使用していません。
- 開発用依存：`@astrojs/check`、`typescript`。リンク・内容検証にはPython 3の標準ライブラリを使用。

## 開発環境

Node.js 22.19以上を推奨します。既存のAstro依存 `unifont → undici@8` が22.19以上を指定しています。今回の環境Node 22.16ではインストール時にengine警告が出ましたが、型検証・静的ビルドは成功しています。

```sh
npm install
npm run dev -- --background
```

開発サーバーはAGENTS.mdに従いバックグラウンドで起動します。URLは起動時出力を確認（通常 `http://localhost:4321`）。

```sh
npm run astro -- dev status
npm run astro -- dev logs
npm run astro -- dev stop
```

## ビルド・検証

```sh
npm run check
npm run build
npm run verify
```

`dist/` が配布可能な静的ファイル一式です。静的ホスティングではこのディレクトリを公開し、404には `dist/404.html` を指定します。ルートパスでの配置を前提としています。サブディレクトリ配信ではリンクをbase対応に変更してください。

`verify` はビルド済みHTMLの内部リンク・アンカー・アセット、ページ言語・見出し・画像代替文、全教材の順序・関連記事・演習構造・検索収録、主要な数値計算を確認します。外部リンクの継続可用性、ブラウザーでの操作、実回路の安全適合性を保証する検証ではありません。

## サイト構造

| URL | 内容 |
| --- | --- |
| `/` | 目的別の入口、学習章、おすすめ教材 |
| `/roadmap/` | 前提知識と到達目標を持つ学習順序 |
| `/category/[category]/` | 7章の教材一覧 |
| `/learn/[id]/` | 本文、目次、図、問題、前後・関連記事 |
| `/search/` | 全文検索とカテゴリ絞り込み |
| `/about/` | 教材の使い方とレビュー方針 |

| 章ID | 教材数 | 内容 |
| --- | ---: | --- |
| basics | 8 | 安全、V/I/R、電力、KCL/KVL、分圧、AC、インピーダンス、GND・回路図 |
| components | 12 | 抵抗からロジックICまで。関連部品を比較しながら収録 |
| circuits | 11 | LED、RC、スイッチ、増幅、整流、PWM、電源配置、BJTバイアス |
| measurement | 4 | DMM、オシロ、FG、誤差と記録 |
| experiments | 8 | 無通電の抵抗測定からRCの周波数応答まで |
| troubleshooting | 1 | 電源・帰路・DC電圧・信号・波形の順に切り分け |
| design | 9 | 設計プロセスと8つの設計演習 |

```text
src/
  content.config.ts       # 教材スキーマ
  content/lessons/*.md     # 本文・メタデータ（ファイル名がID）
  data/categories.ts      # 章名・順序・到達目標
  components/             # 図、警告、式、問題など
  layouts/Layout.astro    # 共通ヘッダー、ナビ、テーマ、フッター
  pages/                  # 静的ルートと検索インデックス
  styles/global.css       # テーマ・レイアウト・レスポンシブ
public/diagrams/           # 自作SVG原本
scripts/verify-site.py     # リンク・教材・計算検証
scripts/generate-diagrams.py # SVGの再生成用ソース
 docs/IMPLEMENTATION.md    # 調査と当初の情報設計
 docs/TECHNICAL_REVIEW.md  # レビュー範囲・根拠・検証結果
TODO.md                   # 完了済みと未検証・今後の拡張
```

## 新しい記事を追加する

`src/content/lessons/` へ `.md` を追加します。ファイル名は小文字英数字とハイフンで一意にし、`order` は同じ章内で重複させません。

```yaml
---
title: "新しい回路の読み方"
description: "どのような仕組みを学び、何をできるようになるかを説明します。"
category: "circuits"
order: 12
minutes: 10
level: "基礎"
tags: ["回路", "測定"]
objectives: ["電流の帰路を説明できる"]
related: ["reading-schematics", "multimeter"]
reviewed: "2026-09-19"
quiz:
  question: "部品が断線したらどの測定点が変わりますか？"
  answer: "予想と、その根拠となる電流経路を説明します。"
---

## まず直感で
身近な見方で説明します。

## 正確な説明
式の適用条件、単位、値、測定点を明記します。
```

`reviewed` は実際に内容を確認した日を文字列で指定します。`level` は「入門」「基礎」「実践」。`category` は上表のID。

任意項目：

```yaml
warning: "作業前に電源を切り、残留電圧を確認します。"
diagram: "led"
diagramCaption: "電源から抵抗とLEDを通ってGNDへ戻る経路。"
formula:
  expression: "V = IR"
  example: "1 kΩ × 5 mA = 5 V"
```

記事追加後は一覧、順序、前後リンク、検索、目次が自動更新されます。`related` は記事IDを指定。本文リンクは `/learn/id/`、図は `/diagrams/name.svg`。本文のSVGには原寸リンクも添えてください。

設計演習は `要求仕様` → `まず自分で考える` の後に `<details><summary>設計例を開く</summary>` を置き、空行を挟んでMarkdownを書きます。目次やハッシュリンクから折りたたみ内を選ぶと、自動で開きます。

## 教材コンポーネント

Markdownは本文に集中し、frontmatterから記事テンプレートが共通コンポーネントを表示します。MDXは導入していないため、`.md` にAstroコンポーネントを直接importする方式ではありません。独自の`.astro`ページから使う場合：

```astro
---
import Callout from '../components/Callout.astro';
import Formula from '../components/Formula.astro';
import Quiz from '../components/Quiz.astro';
import CircuitDiagram from '../components/CircuitDiagram.astro';
import ComponentSpec from '../components/ComponentSpec.astro';
import Experiment from '../components/Experiment.astro';
---
<Callout kind="warning" title="接続前に確認"><p>電源をOFFにします。</p></Callout>
<Formula expression="τ = RC" example="1 kΩ × 100 nF = 100 µs" />
<Quiz question="Rを2倍にすると？" answer="理想的な時定数は2倍です。" />
<CircuitDiagram name="rc" caption="出力を取り出す場所を比較する。" />
<ComponentSpec rows={[{name:'抵抗', value:'1 kΩ ±1%', reason:'時定数を決める'}]} />
<Experiment level={1} title="抵抗を測る"><p>目的と手順をここに書きます。</p></Experiment>
```

`Callout` のkindは `warning / important / tip / mistake / measurement`。別々のWarning/Tip等を増やす代わりに、見た目と意味をここで統一しています。

## 図の編集

SVGは外部ライブラリなしの自作です。再生成する場合は `python3 scripts/generate-diagrams.py`。原本を直接編集した場合は、再生成時に失わないようスクリプトにも反映してください。回路図は部品の物理的端子配列を示しません。機能ブロック図は本文でその旨を明記しています。

## 安全と確認範囲

実験は原則DC 3〜5 V、小電流。12 V設計は絶縁済み直流電源の二次側のみ。商用AC、高電圧、大容量蓄電部は実習対象外です。BOMは選定条件を示す教材用で、全品の発注型番が確定した量産設計ではありません。

数式、主要計算、極性、測定器のGND、部品選定条件を机上レビューしました。実回路の実測検証や第三者レビューは未実施。端末のブラウザー操作権限がないため、デスクトップ／スマートフォンの実ブラウザーによる最終表示・操作テストも未実施です。CSSは幅別の設計と静的確認を行っています。

詳細は [技術レビュー記録](docs/TECHNICAL_REVIEW.md) と [TODO](TODO.md) を参照してください。
