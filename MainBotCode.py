import discord
from discord.ext import commands
import random

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
    if str(ctx.author) in valid_users:
        await ctx.send("quitting the bot")
        await client.change_presence(status = discord.Status.offline)
        quit()
    else:
        await ctx.send("You do not have permission to enter this command")


@client.command() #toggle the reversal of words
async def toggleReverseWords(ctx):
    global reverseWords
    reverseWords = not reverseWords
    await ctx.send('reversal of words now set to ' + str(reverseWords))

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
async def helpMe(ctx):
    embed = discord.Embed(title = "chatBot help", description = "Some useful commands")
    embed.add_field(name = "!toggleReverseWords", value = "Toggles whether all words will be reversed or not")
    embed.add_field(name = "!ping", value = "Returns the bot's ping to the server")
    embed.add_field(name = "joke", value = "tells a joke")
    await ctx.send(embed = embed)

@client.command(aliases = ["joke", "telljoke"])
async def tellJoke(ctx):
    jokeQuestion = [
    "What do you call bears without ears?",
    "Why don't blind people skydive?",
    "As a scarecrow people say I'm outstanding at my job",
    "What do cannonballs do when they're in love?"
    "How long is a chinese man's name"]

    jokeAnswer = [
    "B",
    "It scares the hell out of their dogs",
    "but hay, its in my jeans",
    "make bb's"
    "no, really, it is."]

    jokeNumber = random.randint(0, len(jokeQuestion) - 1)
    await ctx.send(jokeQuestion[jokeNumber])
    await ctx.send(jokeAnswer[jokeNumber])

client.run('NTc4MzY4NTI3NzY2MTI2NjEz.XN15Vw.TbHe8gQ2jGVkxbyqXTC2kiUxiS4')
