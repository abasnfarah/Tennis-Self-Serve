from flask import Flask, request, render_template, send_file
import tempfile
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def data():
    data_received = request.json
    print(data_received)
    video_file = request.files['video']
    if video_file:
        input_path = data_received['uri']
        output_path = 'output_video.mp4'

        video_file.save(input_path)

        # convert mov to mp4
        subprocess.run(['ffmpeg', '-i', input_path, '-vcodec', 'copy', '-acodec', 'copy', output_path])

        #OpenCv stuff here with the video
        return send_file(output_path, as_attachment=True)

    return 'No video file provided', 400

if __name__ == "__main__":
    app.run(debug=True)
