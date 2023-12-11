from flask import Flask, request, render_template
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def data():
    data_received = request.json
    print(data_received)
    return {"message": "Data received!"}

@app.route('/video', methods=['POST'])
def video():
    video_file = request.files['video']
    temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    video_file.save(temp_video.name)

    # OpenCv stuff here with the video
    # temp video should be the output video with acompanying text or just pose info.

    print("Sending Video...")
    return send_file(temp_output_video.name, as_attachment=True, attachment_filename='processed_video.mp4')


if __name__ == "__main__":
    app.run(debug=True)
