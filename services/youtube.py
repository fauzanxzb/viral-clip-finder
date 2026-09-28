from datetime import datetime, timedelta, timezone
import requests
from config import YOUTUBE_API_KEY

BASE_URL = "https://www.googleapis.com/youtube/v3"

class YouTubeAPIError(Exception):
    pass

class YouTubeService:
    def __init__(self):
        if not YOUTUBE_API_KEY:
            raise YouTubeAPIError(
                "YOUTUBE_API_KEY belum diisi. Buat file .env dari .env.example lalu masukkan API key."
            )
        self.key = YOUTUBE_API_KEY

    def _get(self, endpoint, params):
        params = dict(params)
        params["key"] = self.key
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=20)
        if not response.ok:
            try:
                detail = response.json().get("error", {}).get("message", response.text)
            except Exception:
                detail = response.text
            raise YouTubeAPIError(f"YouTube API error ({response.status_code}): {detail}")
        return response.json()

    def search_videos(self, query, region="ID", language="id", days=7,
                      order="date", max_results=25, creative_commons=False):
        published_after = (
            datetime.now(timezone.utc) - timedelta(days=days)
        ).isoformat().replace("+00:00", "Z")

        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "order": order if order in {"date", "viewCount", "rating", "relevance"} else "date",
            "maxResults": max_results,
            "regionCode": region,
            "relevanceLanguage": language,
            "publishedAfter": published_after,
            "safeSearch": "moderate",
        }
        if creative_commons:
            params["videoLicense"] = "creativeCommon"

        search_data = self._get("search", params)
        ids = [
            item.get("id", {}).get("videoId")
            for item in search_data.get("items", [])
            if item.get("id", {}).get("videoId")
        ]
        if not ids:
            return []

        details = self._get("videos", {
            "part": "snippet,statistics,contentDetails,status",
            "id": ",".join(ids),
        })

        by_id = {item["id"]: item for item in details.get("items", [])}
        videos = []

        for item in search_data.get("items", []):
            vid = item.get("id", {}).get("videoId")
            data = by_id.get(vid)
            if not data:
                continue

            snippet = data.get("snippet", {})
            stats = data.get("statistics", {})
            status = data.get("status", {})

            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))
            published = snippet.get("publishedAt", "")

            videos.append({
                "id": vid,
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "channel": snippet.get("channelTitle", ""),
                "published_at": published,
                "views": views,
                "likes": likes,
                "comments": comments,
                "license": status.get("license", "youtube"),
                "duration": data.get("contentDetails", {}).get("duration", ""),
                "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                "url": f"https://www.youtube.com/watch?v={vid}",
            })

        return videos
