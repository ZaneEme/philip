import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '!')
reverseWords = False

@client.event
async def on_ready():
    print("The bot is ready")
    print(client.user)

@client.event
async def on_message(message):
    global reverseWords
    channel = message.channel

    if message.author == client.user:
      return

    if message.content == "Philicia" or message.content == "philicia":
      await channel.send('I love you <3')

    elif reverseWords == True:
      await channel.send(message.content[::-1])

    await client.process_commands(message) #end the onMessage loop

@client.command()
async def quitBot(ctx): #quit the bot
    valid_users = ['Zane#9722']
    await ctx.send("quitting the bot")
    
    if str(ctx.author) in valid_users:
        quit()


@client.command() #toggle the reversal of words
async def toggleReverseWords(ctx):
    global reverseWords
    reverseWords = not reverseWords
    await ctx.send('reversal of words now set to ' + str(reverseWords))

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")



client.run('NTc4MzY4NTI3NzY2MTI2NjEz.XN15Vw.TbHe8gQ2jGVkxbyqXTC2kiUxiS4')
