from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/')
def home():
    return 'API работает. Отправь POST на /download с JSON.'

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'Не передан параметр "url"'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'noplaylist': True,
        'skip_download': True,
        'forcejson': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                'title': info.get('title'),
                'url': info.get('url'),
                'ext': info.get('ext'),
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
