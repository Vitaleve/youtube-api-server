from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return {"error": "URL fehlt"}, 400

    output_path = f"/tmp/{uuid.uuid4()}.mp4"
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run()
