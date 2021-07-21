import discord
import os 
import requests
import json
from keep_alive import keep_alive
import random

client=discord.Client()

def get_apod():
  key='FMfWK8eHQ7zBWqhSrqQ27dmxHe45x642CqlhBboO'
  url=f'https://api.nasa.gov/planetary/apod?api_key={key}'
  response=requests.get(url)
  json_data=json.loads(response.text)
  pic=json_data['url']
  return pic

def get_photo():
  response= requests.get('https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/latest_photos?api_key=FMfWK8eHQ7zBWqhSrqQ27dmxHe45x642CqlhBboO')
  json_data=json.loads(response.text)
  pic=json_data['latest_photos']
  pics=[]
  for p in pic:
    pics.append(p['img_src'])
  random_pic=random.choice(pics)
  return random_pic

def elon():
  lines=open('extras/elon.txt').read().splitlines()
  my_lines=random.choice(lines)
  output=f'Elon Musk once said - {my_lines}'
  return output

def get_astronaut():
  response = requests.get("http://api.open-notify.org/astros.json")
  json_data = json.loads(response.text)
  people = json_data['people']
  ppl=[]
  for p in people:
    ppl.append(p['name'])
  x=(', '.join(ppl))
  output=f'The current people in space are {x}'
  return(output)

def get_ISS():
  response=requests.get('http://api.open-notify.org/iss-now.json')
  json_data=json.loads(response.text)
  location=json_data['iss_position']
  lat=location['latitude']
  long=location['longitude']
  output=f'The current longitude and latitude of the International Space Station (ISS) is {long} , {lat}'
  return (output)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return

  msg = message.content

  if msg.startswith('$apod'):
    apod=get_apod()
    await message.channel.send(apod)

  if msg.startswith('$pic'):
    p=get_photo()
    await message.channel.send(p)
  
  if msg.startswith('$elon') :
      e = elon()
      await message.channel.send(e)

  if msg.startswith('$ISS') or msg.startswith('$iss') :
      iss = get_ISS()
      await message.channel.send(iss)

  if msg.startswith('$People')or msg.startswith('$people'):
    people_in_space = get_astronaut()
    await message.channel.send(people_in_space)

  if msg.startswith('$help'):
    output='$People for current astronauts in space\n$ISS for current location of ISS\n$elon for a random quote from Elon Musk\n$pic for random picture from perseverance rover on mars\n$apod for NASA Astronomy Picture of the Day'
    await message.channel.send(output)

keep_alive()
client.run(os.environ['TOKEN'])