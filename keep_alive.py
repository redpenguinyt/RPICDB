from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hey there! This is the page that keeps Red Penguin's Discord bot alive! use $help on his discord server for more info!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()