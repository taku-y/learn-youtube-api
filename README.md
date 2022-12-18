# learn-youtube-api
YouTube APIの学習用リポジトリ。[こちらの記事](https://diy-programming.site/youtube/channel-video-info-get/)のコードを引用しています。

## PyDataチャンネルのビデオの統計情報

使い方は以下の通りです。

1. Google Cloud Platformの自身のアカウントでプロジェクトを作成し、YouTube Data API v3を有効にします。
2. APIキーを取得し、環境変数APIKEYにセットします。
3. 以下のコマンドを実行します。`video_ids.csv`が生成されます。このファイルにはチャンネルに登録されている動画のIDの一覧が含まれます。

  ```bash
  python get_video_ids.py
  ```

4. 以下のコマンドを実行します。`video_infos.csv`が生成されます。このファイルには各動画の情報が含まれます。

  ```bash
  python get_video_infos.py
  ```
