from flask import Flask
app = Flask(__name__)

@app.route("/upload", methods = ['GET'])
def hello():
    return "Hello World!"
