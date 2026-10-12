# Sphere–cylinder contact packing: numerical supplement

同一の球3〜12個を、直径3.71 cmの円柱に接触させる配置の数値補足資料です。球直径は15.3 cm。床あり、側面・上面・上端の縁への接触を認め、球同士の重なりを禁止して円柱高さを探索しました。

公開対象は数値結果・中心座標・画像・3D表示と計算条件です。研究上の考察は別資料で扱います。全ケースは共通の数値収束基準v1を満たしますが、大域的最適性は未証明です。探索コード・全試行ログはこの補足資料には含みません。

## フォルダー

```text
docs/                 GitHub Pagesの公開ルート
  index.html          数値一覧・画像・3D表示への入口
  protocol.html       共通の数値収束基準
  assets/             図と各球数の画像
  data/               CSV、JSON、計算条件、全球中心座標
  viewers/            履歴を埋め込んだ各球数の3Dビューアー
  manifest.json       配布ファイルのSHA-256
tools/                Python標準ライブラリだけで動く検証
PUBLISHING_ja.md       公開の具体的手順
```

## 閲覧・検証

`docs/index.html`をブラウザーで開けば一覧を閲覧できます。3D表示にはWebGLとインターネット接続が必要です。Three.js r128とOrbitControlsをjsDelivrから読み込みます。静的画像と数値表はオフラインでも表示できます。

公開後のURLは `https://<GitHubユーザー名>.github.io/<リポジトリ名>/` です。公開手順は [PUBLISHING_ja.md](PUBLISHING_ja.md) を参照してください。

パッケージのルートから以下を実行します（Python 3.9以降、追加パッケージ不要）。

```bash
python tools/check_publication.py
python tools/verify_packing.py docs/data/best_10.json --tolerance-cm 0.000000765
```

配置JSONの座標・高さの単位はcm。`optimality_proven: false`は大域最適性が未証明であることを明示します。動画再生は選択した局所探索の履歴であり、6,000試行全体を再生するものではありません。ファイルハッシュは同梱物の整合性確認用で、署名や出所の証明ではありません。

## 参考と利用条件

- 探索・可視化の着想：[Yohei Nakajima — Soft-to-Rigid Packing](https://github.com/yoheinakajima/soft-to-rigid-packing)。本問題への適用結果は独立した数値実験です。
- [Three.js](https://github.com/mrdoob/three.js) とOrbitControls：MITライセンス。ライブラリーは配信元から読み込みます。

本パッケージ自身のコード・データ・図の再利用ライセンスは未指定です。公開前に権利者が方針を決めてください。閲覧公開と、改変・再配布等へのライセンス付与は別の判断です。
