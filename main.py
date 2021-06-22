import discord, os, requests, json, random

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = [
	"Cheer up! ",
	"Hang in there. ",
	"You are a great person / bot! "
]

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return(quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! I am RedPenguin Bot!')

    if message.content.startswith('$inspire'):
    	quote = get_quote()
    	await message.channel.send(quote)
    
    msg = message.content

    if any(word in msg for word in sad_words):
    	rngmsg = random.choice(starter_encouragements) + message.author
		await message.channel.send(rngmsg)


client.run(os.getenv('TOKEN'))
