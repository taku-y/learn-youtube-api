import os
import urllib.request
import urllib.parse
import json
import pandas as pd
import isodate

#-------↓パラメータ入力↓-------

APIKEY = os.environ.get("APIKEY")
channel_id = "UCOjD18EJYcsBog4IozkF_7w" #  PyDataチャンネルのID

#-------↑パラメータ入力↑-------

df = pd.read_csv("video_ids.csv")
video_ids = list(df["ID"])
size = 50
chunk = [video_ids[pos:pos + size] for pos in range(0, len(video_ids), size)]
outputs = []

for video_ids in chunk:
    #videoメソッドで動画情報取得
    param = {
        'part':'id,snippet,contentDetails,liveStreamingDetails,player,recordingDetails,statistics,status,topicDetails',
        'id':",".join(video_ids),
        'key':APIKEY
    }
    target_url = 'https://www.googleapis.com/youtube/v3/videos?'+(urllib.parse.urlencode(param))
    req = urllib.request.Request(target_url)

    try:
        with urllib.request.urlopen(req) as res:
            body = json.load(res)
            for item in body['items']:
                #値が存在しない場合ブランク
                publishedAt = item['snippet']['publishedAt'] if 'publishedAt' in item['snippet'] else ''
                title = item['snippet']['title'] if 'title' in item['snippet'] else ''
                description = item['snippet']['description'] if 'description' in item['snippet'] else ''
                url = 'https://www.youtube.com/watch?v=' + item['id'] if 'id' in item else ''
                thumbnail_url = item['snippet']['thumbnails']['high']['url'] if 'thumbnails' in item['snippet'] else ''
                categoryId = item['snippet']['categoryId'] if 'categoryId' in item['snippet'] else ''
                # liveBroadcastContent = item['snippet']['liveBroadcastContent'] if 'liveBroadcastContent' in item['snippet'] else ''
                if 'duration' in item['contentDetails']:
                    #durationを時分秒へ変換
                    duration = isodate.parse_duration(item['contentDetails']['duration'])
                else:
                    duration = ''
                viewCount = item['statistics']['viewCount'] if 'viewCount' in item['statistics'] else 0
                likeCount = item['statistics']['likeCount'] if 'likeCount' in item['statistics'] else 0
                favoriteCount = item['statistics']['favoriteCount'] if 'favoriteCount' in item['statistics'] else 0
                commentCount = item['statistics']['commentCount'] if 'commentCount' in item['statistics'] else 0
                # embedHtml = item['player']['embedHtml'] if 'embedHtml' in item['player'] else ''
                outputs.append([
                    publishedAt, title, description, url, thumbnail_url,
                    categoryId, duration, viewCount, likeCount, favoriteCount,
                    commentCount
                ])
            
    except urllib.error.URLError as err:
        print(err)

df = pd.DataFrame({
    "PublishedAt": [e[0] for e in outputs],
    "Title": [e[1] for e in outputs],
    "Description": [e[2] for e in outputs],
    "Url": [e[3] for e in outputs],
    "ThumbnailId": [e[4] for e in outputs],
    "CategoryId": [e[5] for e in outputs],
    "Duration": [e[6] for e in outputs],
    "ViewCount": [e[7] for e in outputs],
    "LikeCount": [e[8] for e in outputs],
    "FavCount": [e[9] for e in outputs],
    "CommentCount": [e[10] for e in outputs],
})
df.to_csv("video_infos.csv")
