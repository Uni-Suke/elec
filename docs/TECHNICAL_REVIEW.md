# 技術レビューと検証記録

確認日：2026-09-19。教材の机上レビューであり、実機試験・認証・独立した第三者による承認ではない。

## 教材の確認

| 対象 | 確認と修正 |
| --- | --- |
| 基礎 | 電圧は2点の差、電流は保存、電力と電力量を区別。KCL/KVLの入門集中定数モデルという適用範囲を明記 |
| 分圧 | 無負荷の式の前提を明記。10 kΩ負荷追加で2.5→1.67 Vになることを再計算 |
| RC | τ、fc、−3 dBが振幅0.707倍であること、位相−45°、100 kΩ/100 µFの10秒を確認 |
| LED | 公称と電源・Vf・抵抗許容差の最悪値を再計算。最大5.62 mA、抵抗最大19.4 mW |
| BJT | 典型hFEで飽和を保証しない。VCE(sat)のIC/IB条件とGPIOのVOHを使用。増幅用バイアスの別教材を追加 |
| MOSFET | VGS(th)と十分なONを区別。2.5 V時のRDS(on)、温度、Qgと駆動電流、SOAを確認 |
| リレー | フライバックのKは電源＋、Aは低側。OFF時の循環と復帰遅れを明記 |
| 増幅・ADC | 3.3 V単電源でゲイン3を選び、入力同相・出力範囲・負荷・端点の誤差を記載。ADCの理想LSBと実精度を区別 |
| 電源 | 13.2→3.3 V / 300 mAのLDO損失2.97 W。効率85%は製品保証でなく仮定と明記 |
| PWM | 平均電圧の2乗から抵抗電力を出さない。5 V/100 Ω/50%は平均125 mW |
| DMM | 赤端子とモードを両方確認。電圧並列、電流直列、電流測定後のV/Ω復帰、無通電で抵抗測定 |
| オシロ | 全CHのGNDと保護接地の共通性、AC couplingは絶縁ではないこと、プローブ負荷とエイリアシング |
| FG | Hi-Zは出力抵抗0 Ωの意味ではない。実振幅を先に測り、RC手前のVinで正規化 |
| 安全 | 低電圧でも短絡・発熱に注意。商用AC等は実習対象外。通電中の配線変更と保護を外す比較実験を禁止 |
| 図 | 自作SVGの接続、ダイオードK/A、BJTのE矢印を確認。代表6図をPNG化して目視確認。PWM設計の負荷を専用図で100 Ωに一致 |

## 参考にした一次資料

- [Tektronix — オシロの準備・接地・プローブ](https://www.tek.com/en/documents/primer/setting-and-using-oscilloscope)
- [Tektronix — ABCs of Probes](https://www.tek.com/en/documents/whitepaper/abcs-probes-primer)
- [Fluke — 287/289取扱説明書](https://assets.fluke.com/manuals/287_289_umeng0000.pdf)
- [Keysight — Output Load Termination](https://helpfiles.keysight.com/Standalone_BenchVueSoftware_PW_HelpFiles/PWFGApp/Content/Configure%20Waveforms/Waveform%20Configuration/Output%20Load%20Termination.htm)
- [Keysight — 設定振幅と実測値の違い](https://docs.keysight.com/kkbopen/why-can-a-function-generators-output-signal-amplitude-be-different-from-what-is-selected-577941706.html)
- [AOS — AO3400A](https://www.aosmd.com/products/mosfets/low-voltage-mosfets-12v-30v/ao3400a)
- [onsemi — 2N3903 / 2N3904データシート](https://www.onsemi.com/download/data-sheet/pdf/2n3903-d.pdf)
- [TI — TLV9002](https://www.ti.com/product/TLV9002)
- [TI — MOSFET Selection Guide](https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/sluaax9.pdf)
- [TI — デカップリングの配置](https://e2e.ti.com/blogs_/archives/b/precisionhub/posts/the-decoupling-capacitor-is-it-really-necessary)

メーカー資料は該当部分の確認に用いた。全教材の実機動作を各メーカーが保証しているわけではない。詳細値は採用型番の最新版と試験条件を優先する。

## ソフトウェア検証

- `npm run check`：0 errors / 0 warnings / 0 hints。Astro 7に合わせてzのimportを`astro/zod`へ更新。
- `npm run build`：静的65 HTMLページと検索JSONを生成。全Content Collectionsスキーマ適合。
- `npm run verify`：2,263件の内部リンク・アンカー・画像参照、53教材の順序と関連記事、8実験と8設計演習の構造、検索収録を確認。
- 12件の数値例をPythonで独立に再計算し、許容誤差内を確認。
- 開発サーバーを`astro dev --background`で起動。教材追加前のプレビューには動的記事が反映されなかったため、完成後に再起動し、`http://localhost:4322`のホーム・ロードマップ・オシロ教材・設計8・検索・検索JSONの6 URLでHTTP 200を確認。
- CSSは620/760/900/980/1200px付近の構成を確認し、狭い中間幅でのヒーロー見出しのはみ出しを抑制。図はスクロール・原寸リンクを追加。
- 検索表示は`textContent`で組み立て、検索語をHTMLとして挿入しない。テーマ保存が使えない場合も操作継続する。
- 閉じた設計解答内への目次リンクは、先にdetailsを開くようにした。小画面で閉じたサイドバーはvisibilityでフォーカス対象から除外。

## 未検証・限界

- ブラウザー連携がなく、ネイティブブラウザー操作も端末権限により拒否された。実ブラウザーの表示、検索・テーマ・メニューのE2E、200%拡大、スクリーンリーダー操作は未検証。
- 全回路の部品調達・ブレッドボード実装・オシロ波形記録は未実施。
- 汎用部品の仕様は種類の選定指針であり、全品番の保証ではない。BOMは仕様例で、量産・発注用の完全型番は未確定。
- 商用電源、高電圧、絶縁規格、EMC適合、機能安全は実装教材の対象外。
- ローカル全文検索は全件JSON方式。数千教材規模では分割や専用検索インデックスを検討する。
