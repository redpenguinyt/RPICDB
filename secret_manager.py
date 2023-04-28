from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')
REDDIT_ID = os.getenv('REDDIT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
YT_API_KEY = os.getenv('YT_API_KEY')