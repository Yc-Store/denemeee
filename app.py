from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_audio', methods=['POST'])
def get_audio():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL girilmedi'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'skip_download': True,  # Sadece info alıyoruz
        'noplaylist': True,     # Playlist yerine tek video
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Eğer video oturum veya captcha istiyorsa hata verir
            if 'url' not in info:
                return jsonify({'error': 'Bu video çerez veya giriş gerektiriyor.'}), 403
            audio_url = info['url']
            title = info.get('title', 'Unknown')
        return jsonify({'audio_url': audio_url, 'title': title})
    except Exception as e:
        return jsonify({'error': 'Link alınamadı: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
