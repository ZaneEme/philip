import discord
from discord.ext import commands
import random
import os

client = commands.Bot(command_prefix = '!', help_command = None)
reverseWords = False
valid_users = ['Zane#9722', 'Phililiser#9239'] #users with admin priveleges

@client.event
async def on_ready():
    print("The bot is ready")
    print(client.user)

@client.event
async def on_message(message): #when the bot starts
    global reverseWords
    channel = message.channel

    if message.author == client.user:  #if the bot sent the last message, do nothing
      return

    if message.content == "Philicia" or message.content == "philicia": #if the last message was philicia
        if reverseWords == True:
            await channel.send('ε> uoy evol I')
        else:
            await channel.send('I love you <3')

    elif reverseWords == True:
      await channel.send(message.content[::-1])

    await client.process_commands(message) #end the onMessage loop

@client.command(aliases = ["quit", "quitbot", "q"])
async def quitBot(ctx): #quit the bot
    global valid_users
    if str(ctx.author) in valid_users:
        await ctx.send("quitting the bot")
        await client.change_presence(status = discord.Status.offline)
        quit()
    else:
        await ctx.send("You do not have permission to enter this command")


@client.command(aliases = ["reverse", "reverseWords"]) #toggle the reversal of words
async def toggleReverseWords(ctx):
    global reverseWords
    reverseWords = not reverseWords
    await ctx.send('reversal of words now set to ' + str(reverseWords))

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command(Aliases = ['help', 'Help'])
async def helpMe(ctx):
    embed = discord.Embed(title = "Philip help", description = "Some useful commands")
    embed.add_field(name = "!reverse", value = "Toggles word reversal")
    embed.add_field(name = "!ping", value = "Returns the bot's ping")
    embed.add_field(name = "!joke", value = "Tells a joke")
    embed.add_field(name = "!hangman", value = "Plays hangman")
    await ctx.send(embed = embed)

@client.command(aliases = ["joke", "telljoke"])
async def tellJoke(ctx):
    jokeQuestion = [
    "What do you call bears without ears?",
    "Why don't blind people skydive?",
    "As a scarecrow people say I'm outstanding at my job",
    "What do cannonballs do when they're in love?",
    "How long is a chinese man's name",
    "What do you get when you cross an insomniac, a dislexic, and an agnostic?",
    "Where does the general keep his armies?"]
    #7 jokes

    jokeAnswer = [
    "B",
    "It scares the hell out of their dogs",
    "but hay, its in my jeans",
    "make bb's",
    "no, really, it is.",
    "Someone who lays awake at night wondering of there's a dog",
    "In his sleevies"]
    #7 answers

    jokeNumber = random.randint(0, len(jokeQuestion) - 1)
    await ctx.send(jokeQuestion[jokeNumber])
    await ctx.send(jokeAnswer[jokeNumber])

@client.command()
async def clear(ctx, amount = 0):
    global valid_users
    if str(ctx.author) in valid_users:
        await ctx.channel.purge(limit = amount + 1)


client.load_extension("cogs.hangMan")
client.run('***REMOVED***')
