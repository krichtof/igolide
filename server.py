from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Notif Light anime votre salon lorsqu'un événement survient"

@app.route('/events', methods=['POST'])
def handle_event():
    print("coucou")
    return "Ok guy"
