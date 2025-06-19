from flask import Flask, request, jsonify
import os
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Сервер работает. Отправляй POST на /download с JSON {'url':'https://youtube.com/...'}"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL не указан"}), 400

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            direct_url = info.get("url")
            return jsonify({"direct_url": direct_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
