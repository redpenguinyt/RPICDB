# Setting up the bot to run on your own
This will run best on [repl.it](replit.com) as it uses replit.db so create a new repository there by importing it from github
## Setting up the .env
### Go to the secrets section (or create a .env file) and add the following
1. Got to [The discord dev page](https://discord.com/developers/applications/) and create a new application and create a new bot, add the bot token to your secrets with name "token" and the value as the bot token
2. Go to [reddit dev page](https://www.reddit.com/prefs/apps) and create a new app. Save the app id and app secret. In the secrets section, add:
	1. "reddit_id"= the app id
	2. "reddit_secret"= the app secret
	3. "reddit_user_agent"= type in something like "Redditapp by u/arealuser" but type in your app's name and your reddit username
3. set up mongodb
4. set up youtube

THIS IS WORK IN PROGRESS the tutorial isn't finished so don't try to set it up yet