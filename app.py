from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_path = download_youtube_video(url)
    response = send_file(download_path, as_attachment=True)
    @response.call_on_close
    def cleanup():
        try:
            os.remove(download_path)
        except Exception:
            pass
    return response

def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

if __name__ == '__main__':
    # Only run in debug mode when running directly
    app.run(debug=True, host='127.0.0.1', port=5000)

#https://www.youtube.com/watch?v=wL8DVHuWI7Y