from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def data():
    data_received = request.json
    print(data_received)
    return {"message": "Data received!"}

if __name__ == "__main__":
    app.run(debug=True)
