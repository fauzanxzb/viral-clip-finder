from datetime import datetime, timezone
import math
import re

def _hours_since(iso_date):
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        return max((datetime.now(timezone.utc) - dt).total_seconds() / 3600, 0.25)
    except Exception:
        return 168.0

def _norm(value, low, high):
    if value <= low:
        return 0.0
    if value >= high:
        return 1.0
    return (value - low) / (high - low)

def score_videos(videos, query=""):
    q_words = {w.lower() for w in re.findall(r"\w+", query) if len(w) > 2}

    for video in videos:
        hours = _hours_since(video["published_at"])
        views = video["views"]
        likes = video["likes"]
        comments = video["comments"]

        engagement = ((likes + comments) / views * 100) if views else 0
        views_per_hour = views / hours

        title_words = {w.lower() for w in re.findall(r"\w+", video["title"]) if len(w) > 2}
        relevance = len(q_words & title_words) / max(len(q_words), 1)

        velocity_score = _norm(math.log10(max(views_per_hour, 1)), 1.5, 5.0)
        engagement_score = _norm(engagement, 0.5, 12.0)
        freshness_score = math.exp(-hours / 168)
        relevance_score = min(relevance * 1.5, 1.0)
        volume_score = _norm(math.log10(max(views, 1)), 3.0, 7.0)

        score = (
            0.35 * velocity_score +
            0.25 * engagement_score +
            0.15 * freshness_score +
            0.15 * relevance_score +
            0.10 * volume_score
        ) * 100

        video["engagement"] = round(engagement, 2)
        video["views_per_hour"] = round(views_per_hour, 1)
        video["viral_score"] = round(min(score, 100), 1)
        video["age_hours"] = round(hours, 1)

    return sorted(videos, key=lambda x: x["viral_score"], reverse=True)
