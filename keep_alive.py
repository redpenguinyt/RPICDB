from flask import Flask, redirect
from threading import Thread
import logging

app = Flask('RPICDB')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
	return redirect("https://rpicdb-website.redpenguin.repl.co/")

def run():
  app.run(
		host='0.0.0.0',
		port=8080
	)

def keep_alive():
	t = Thread(target=run)
	t.start()