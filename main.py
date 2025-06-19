from flask import Flask, request, jsonify, send_file
import os
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API работает. Отправляй POST на /download с JSON 
{'url':'https://youtu.be/...'}"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL не указан"}), 400

    output = "/tmp/video.mp4"
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output,
        "merge_output_format": "mp4",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(output, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
