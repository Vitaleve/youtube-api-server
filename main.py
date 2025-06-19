from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# 🟢 Главная страница для проверки
@app.route("/")
def home():
    return "✅ Сервер работает. Используй POST на /download с JSON: 
{\"url\": \"https://youtube.com/...\"}"

# 📥 Web API — принимает ссылку и отдаёт прямой файл
@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL не указан"}), 400

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'outtmpl': 'video.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            direct_url = info.get("url")
            return jsonify({"direct_url": direct_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
