def generate_content(title, video_id):
    clean = title.strip() or "Video ini"
    return {
        "hook": f"TERNYATA {clean.upper()} 😱",
        "caption": f"Kalau kamu lihat sampai akhir, bagian ini yang paling menarik. {clean}",
        "hashtags": "#viral #fyp #fbpro #reels #shortvideo",
        "note": "Gunakan hanya materi yang kamu punya hak/izin untuk dipakai ulang."
    }
