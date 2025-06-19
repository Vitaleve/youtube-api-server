from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return 'API läuft!'

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'Keine URL angegeben'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return jsonify({
                'title': info.get('title'),
                'filename': info.get('title') + '.' + info.get('ext'),
                'status': 'done'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
