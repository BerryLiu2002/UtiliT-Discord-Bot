import os
import discord
from dotenv import load_dotenv
import time
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# GUILD_ID = 830500455019970620

client = discord.Client()
client.intents.members=True # must enable intents to check if member is in guild. See https://discordpy.readthedocs.io/en/latest/intents.html

@client.event
async def on_ready():
  for guild in client.guilds:
    if guild.id == int(GUILD):
      break
  print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
  )

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content == "~pomodoro":
    pom_message = await message.channel.send("React 🍅 here to be included in the pomodoro session!\nReact 🏁 to start the session!")
    await pom_message.add_reaction("🍅")
    await pom_message.add_reaction("🏁")
    def check(reaction, user):
      return user == message.author and str(reaction.emoji) == "🏁"
    try: 
      await client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
      await pom_message.edit(content="You didn't react in time! The pomodoro session has been cancelled.")
      await pom_message.clear_reactions()
    else:
      await pom_message.edit(content="The pomodoro session has started!")
      cache_msg = discord.utils.get(client.cached_messages, id=pom_message.id) # retrieve the updated message from cache
      for reaction in cache_msg.reactions:
        if reaction.emoji == "🍅":
          participants = await reaction.users().flatten()
          print(participants)
          for guild in client.guilds:
            if guild.name == GUILD:
              break
          member_participants = []
          for user in participants:
            if user != client.user:
              member = guild.get_member(user.id)
              if not member:
                print(f"{user} is not a member of the server.")
              else:
                print(f"{user} is a member of the server.")
                member_participants.append(member)
          for member in member_participants:
            await member.edit(mute = True)

  # if message.content == "~pomodoro":
  #   channel = message.author.voice.channel
  #   if channel:
  #     print(channel)


client.run(TOKEN)