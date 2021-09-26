from flask import Flask, redirect
from threading import Thread
import logging

app = Flask('RPICDB')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
	return redirect("https://rpicdb-website.redpenguin.repl.co/")

@app.route("/<url>")
def url(url):
	return redirect(
		f"https://rpicdb-website.redpenguin.repl.co/{url}"
	)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
	Thread(target=run).start()