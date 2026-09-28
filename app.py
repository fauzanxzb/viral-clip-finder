import csv
import io
from flask import Flask, render_template, request, Response, flash
from services.youtube import YouTubeService, YouTubeAPIError
from services.scoring import score_videos
from services.captions import generate_content

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", videos=[], query="", region="ID", days=7, order="date")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").strip()
    region = request.form.get("region", "ID").upper()
    language = request.form.get("language", "id")
    days = max(1, min(int(request.form.get("days", 7)), 30))
    order = request.form.get("order", "date")
    max_results = max(5, min(int(request.form.get("max_results", 25)), 50))
    creative_commons = request.form.get("creative_commons") == "on"

    if not query:
        flash("Masukkan keyword terlebih dahulu.", "error")
        return render_template("index.html", videos=[], query=query, region=region, days=days, order=order)

    try:
        service = YouTubeService()
        videos = service.search_videos(
            query=query,
            region=region,
            language=language,
            days=days,
            order=order,
            max_results=max_results,
            creative_commons=creative_commons,
        )
        videos = score_videos(videos, query)
        return render_template(
            "index.html",
            videos=videos,
            query=query,
            region=region,
            days=days,
            order=order,
            language=language,
            creative_commons=creative_commons,
        )
    except YouTubeAPIError as exc:
        flash(str(exc), "error")
    except Exception as exc:
        flash(f"Terjadi kesalahan: {exc}", "error")

    return render_template("index.html", videos=[], query=query, region=region, days=days, order=order)

@app.route("/content/<video_id>", methods=["GET"])
def content(video_id):
    title = request.args.get("title", "")
    return generate_content(title, video_id)

@app.route("/export", methods=["POST"])
def export():
    payload = request.form.get("rows", "")
    if not payload:
        flash("Tidak ada data untuk diekspor.", "error")
        return render_template("index.html", videos=[])

    # Rows are encoded as JSON by the frontend.
    import json
    rows = json.loads(payload)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "rank", "title", "channel", "published_at", "views",
        "likes", "comments", "engagement", "views_per_hour",
        "viral_score", "license", "url"
    ])
    writer.writeheader()
    writer.writerows(rows)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=viral_candidates.csv"}
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
