# 🔥 Viral Clip Finder

Dashboard Flask + YouTube Data API untuk mencari kandidat video yang sedang naik berdasarkan views, engagement, umur video, kecepatan views, dan relevansi keyword.

> **Catatan:** Viral Score adalah heuristik internal, bukan prediksi pasti bahwa sebuah video akan viral. Gunakan data sebagai alat riset.

## Fitur

- Search video YouTube berdasarkan keyword.
- Filter region dan bahasa.
- Filter umur video 1–30 hari.
- Urutkan berdasarkan terbaru, views, relevansi, atau rating.
- Opsional: hanya hasil Creative Commons.
- Mengambil statistik video.
- Menghitung:
  - Views per jam
  - Engagement rate
  - Freshness
  - Relevansi keyword
  - Volume views
  - Viral Score 0–100
- Generate hook/caption/hashtag sederhana.
- Export hasil ke CSV.
- Responsive dashboard.

## 1. Persiapan Google Cloud

1. Buka Google Cloud Console.
2. Buat project.
3. Aktifkan **YouTube Data API v3**.
4. Buat API key.
5. Batasi API key berdasarkan kebutuhan project/API.

Dokumentasi resmi:
https://developers.google.com/youtube/v3/getting-started

## 2. Instalasi

```bash
git clone https://github.com/USERNAME/viral-clip-finder.git
cd viral-clip-finder

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## 3. Konfigurasi

Salin:

```bash
copy .env.example .env
```

Kemudian isi:

```env
YOUTUBE_API_KEY=API_KEY_KAMU
FLASK_SECRET_KEY=secret-random-kamu
```

**Jangan commit `.env` ke GitHub.**

## 4. Jalankan

```bash
python app.py
```

Buka:

http://127.0.0.1:5000

## Cara kerja scoring

Skor bukan ukuran resmi YouTube. Aplikasi menggunakan heuristik:

- 35% kecepatan views
- 25% engagement
- 15% freshness
- 15% relevansi keyword
- 10% volume views

Karena API tidak menyediakan "viral score", skor ini hanya alat penyaringan kandidat.

## Lisensi dan penggunaan ulang

Menemukan video melalui API **tidak otomatis memberikan hak untuk mengunduh atau mengunggah ulang video tersebut**.

Jika ingin menggunakan materi orang lain, periksa lisensi, izin pemilik, dan aturan platform. Filter Creative Commons tersedia sebagai bantuan awal, tetapi tetap periksa syarat lisensi dan kecocokan penggunaan.

## Quota API

Aplikasi menggunakan `search.list` untuk pencarian dan `videos.list` untuk mengambil detail/statistik. Google mendokumentasikan bahwa `search.list` memiliki biaya quota tersendiri dan quota dapat berubah sesuai kebijakan/API project.

Hindari pencarian berulang yang tidak diperlukan.

## Struktur

```text
viral-clip-finder/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── services/
│   ├── __init__.py
│   ├── youtube.py
│   ├── scoring.py
│   └── captions.py
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Roadmap

- [ ] Penyimpanan database SQLite
- [ ] Riwayat pencarian
- [ ] Scheduler pencarian otomatis
- [ ] Multi-keyword scanning
- [ ] Telegram notification
- [ ] Email notification
- [ ] YouTube Shorts detection
- [ ] Analisis transcript
- [ ] Hook berdasarkan isi video
- [ ] Docker
- [ ] Deployment Render/Railway/VPS

## Disclaimer

Project ini dibuat untuk riset konten dan discovery. Jangan menggunakan bot untuk menghindari pembatasan platform, mengambil konten tanpa izin, atau melanggar hak cipta.
