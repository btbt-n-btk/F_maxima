# GitHub / GitHub Pagesへの公開手順

## 推奨する構成

新しい公開リポジトリ（例：`sphere-cylinder-packing`）を作り、このフォルダーの**中身**をルートに置きます。GitHub Pagesは`main`ブランチの`/docs`を公開元にします。HTML・PNG・JSONだけなので、npmやビルド、独自のGitHub Actions設定は不要です。

親の`touch`フォルダー全体をアップロードする必要はありません。考察レポート・依存ライブラリー・全探索ログはパッケージに含めていません。公開リポジトリでは`docs`以外のREADMEや検証スクリプトも誰でも閲覧できます。

## 1. 公開前の確認

1. `docs/index.html`から表・画像・全10ケースの3D表示を確認する。
2. このフォルダーのルートで`python tools/check_publication.py`を実行する。
3. 自分のコード・図・数値データの再利用条件を決める。MIT等を採用する場合は権利者・年を確認してLICENSEを追加し、READMEを更新する。ライセンスを指定しないまま閲覧公開することも可能ですが、再利用許諾は明確になりません。
4. README等を変更した場合は`python tools/check_publication.py --refresh-manifest`でハッシュを更新し、通常チェックを再実行する。

## 2A. GitHub画面からアップロードする場合

1. GitHubで新規リポジトリを作成する。名前は任意、GitHub FreeならPublicを選ぶ。
2. リポジトリの「Add file → Upload files」で、このパッケージ内の`docs`、`tools`、`README.md`、`PUBLISHING_ja.md`、`.gitignore`をアップロードしてコミットする。ZIPそのものをアップロードせず、展開した中身をアップロードする。
3. `docs/index.html`、空の`docs/.nojekyll`、ルートの`.gitignore`があることを確認する。ブラウザーアップロードで隠しファイルが入らなければGitの手順を利用するか、「Add file → Create new file」で追加する。改行を加えるなど内容が変わった場合は、クローンしたフォルダーでハッシュを更新する。
4. ルート直下に`docs`があり、`sphere-cylinder-packing/docs`のような余分な階層になっていないことを確認する。

## 2B. Gitを使う場合

GitHubでPublicの空リポジトリを作成します。README等の自動生成は選ばず、このパッケージのルートで以下を実行します。`YOUR_ACCOUNT`とリポジトリ名を自分のものに置き換えてください。

```bash
git init
git branch -M main
git add docs tools README.md PUBLISHING_ja.md .gitignore
git commit -m "Publish sphere-cylinder packing numerical supplement"
git remote add origin https://github.com/YOUR_ACCOUNT/sphere-cylinder-packing.git
git push -u origin main
```

既にリポジトリがある場合は新規初期化やremote追加をせず、既存のクローンへ中身をコピーしてコミットしてください。認証はGitHubの通常のログイン手順で行います。

## 3. Pagesを有効にする

1. リポジトリの「Settings → Pages」を開く。
2. 「Build and deployment → Source」で「Deploy from a branch」を選択する。
3. Branchを`main`、フォルダーを`/docs`にしてSaveする。
4. デプロイ完了後、Pages画面の「Visit site」を開く。

公開URL：`https://YOUR_ACCOUNT.github.io/sphere-cylinder-packing/`

公式手順：[公開元の設定](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)、[サイトの作成](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)。

## 4. 公開後の確認・更新

- 別の端末またはログアウトしたブラウザーから一覧・3D表示・CSV・座標JSONにアクセスする。
- 3D表示は球数を選び、回転と再生を確認する。回転しない場合はWebGLやjsDelivrへの接続を確認する。
- 全リンクを相対パスにしているため、プロジェクト名を変更してもサイト内のリンクは維持される。
- 新しいデータを追加するときは対応する画像・ビューアー・表を更新し、検証とハッシュ更新を行ってからコミット・pushする。

この手順書を作成した時点では、GitHubへのアップロードや公開設定は行っていません。
