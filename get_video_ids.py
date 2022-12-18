# PyDataチャンネルのVideoIDのリストをCSVファイルに出力します
import os
import urllib.request
import urllib.parse
import json
import datetime
import pandas as pd

#-------↓パラメータ入力↓-------

APIKEY = os.environ.get("APIKEY")
channel_id = "UCOjD18EJYcsBog4IozkF_7w" #  PyDataチャンネルのID

#-------↑パラメータ入力↑-------

dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
nextPageToken = ''
item_count = 0
outputs = []
outputs.append(['publishedAt', 'title', 'description', 'url', 'thumbnail_url', 'categoryId', 'liveBroadcastContent', 'duration', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount', 'embedHtml'])
n = 0
video_ids = []

while True:
    #searchメソッドでvideoid一覧取得
    param = {
        'part':'snippet',
        'channelId':channel_id,
        'maxResults':50,
        'order':'date',
        'type':'video',
        'pageToken':nextPageToken,
        'key':APIKEY
    }
    target_url = 'https://www.googleapis.com/youtube/v3/search?'+urllib.parse.urlencode(param)

    req = urllib.request.Request(target_url)
    try:
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
            for item in body["items"]:
                video_ids.append(item["id"]["videoId"])
    except urllib.error.HTTPError as err:
        print(err)
        break

    #nextPageTokenが表示されなくなったらストップ
    if 'nextPageToken' in body:
        nextPageToken = body['nextPageToken']
    else:
        break

df = pd.DataFrame({"ID": video_ids})
df.to_csv("video_ids.csv")
