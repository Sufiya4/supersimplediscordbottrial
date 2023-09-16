import discord
import os
import requests 
import json
import random 
from replit import db 
from keep_alive import keep_alive

db["encouragements"] = []

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry"]

starter_encouragements = ["dont worry", "tension nakko le", "it will be ok"]

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragemenets"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["enouragements"] = encouragements

def get_quote():
  resp = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(resp.text)
  quote = json_data[0]['q']
  return quote


@client.event
async def on_ready():
  print("we have logged in as {0.user}".format(client))

keys = db.keys()
@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  msg = message.content
  
  if msg.startswith('$hello'):
    await message.channel.send('Hello ji!')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in keys:
    options = options + list(db["encouragements"])

  if msg.startswith('$new'):
    encouraging_message = msg.split('$new ', 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send('new encouraging msg added')

  if msg.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = msg.split('$del ', 1)[1]
      index=int(index[0])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(list(encouragements))
    

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice((options)))

  if msg.startswith('$list'):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"]
    await message.channel.send(list(encouragements)) 

keep_alive()
client.run(os.getenv("TOKEN"))

print (keys)
