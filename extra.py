import random, json, requests

def mentionusr(inputid):
    return "<@" + str(inputid) + ">"

sad_words = [  # List of sad words
    "sad", "depress", "unhappy", "angry", "miserable", "unpog"
]
starter_encouragements = [  # List of encouragements
    "Cheer up %s !", "Hang in there, %s", "You are a great person / bot, %s",
    "%s's mum gae",
    "%s, I just wanna say things will be ok, i cant say they will get better, but I know you can find something to keep you going",
    "your hair is nice %s"
]

def get_quote():  # get a random quote
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

if any(word in message.content for word in sad_words):
	await message.channel.send(random.choice(starter_encouragements) % mentionusr(message.author.id))