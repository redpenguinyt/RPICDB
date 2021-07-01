from flask import Flask, send_from_directory, render_template
from threading import Thread
import os

app = Flask('Red Penguin Discord bot')

@app.route('/favicon.ico')
def favicon(): # Favicon config
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
	return render_template('home.html')

def run():
  app.run(host='0.0.0.0',port=8080)

def start():
    t = Thread(target=run)
    t.start()