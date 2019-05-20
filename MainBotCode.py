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

@client.command(aliases = ["quit", "quitbot", "q"])
async def quitBot(ctx): #quit the bot
    valid_users = ['Zane#9722']
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

@client.command()
async def helpMe(ctx):
    embed = discord.Embed(title = "chatBot help", description = "Some useful commands")
    embed.add_field(name = "!reverse", value = "Toggles word reversal")
    embed.add_field(name = "!ping", value = "Returns the bot's ping to the server")
    embed.add_field(name = "!joke", value = "tells a joke")
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

    jokeAnswer = [
    "B",
    "It scares the hell out of their dogs",
    "but hay, its in my jeans",
    "make bb's",
    "no, really, it is.",
    "Someone who lays awake at night wondering of there's a dog",
    "In his slee"]

    jokeNumber = random.randint(0, len(jokeQuestion) - 1)
    await ctx.send(jokeQuestion[jokeNumber])
    await ctx.send(jokeAnswer[jokeNumber])


wordList = ["banana", "choclolate", "coffee", "pancakes"]
guessedChar = 'a'
tempUnderscoreArray = []
guessesLeft = 7
chosenWord = "a"

@client.command(aliases = ["hangman", "Hangman", "HangMan"])
async def hangMan(ctx):

    def chooseWord():
        global chosenWord
        chosenWord = random.choice(wordList)
        return chosenWord

    def setGameUnderscores():
        global tempUnderscoreArray; chosenWord
        for _ in range(0, len(chosenWord)):
            tempUnderscoreArray.append("--")
            #TODO: use string instead of list maybe??
    chooseWord()
    setGameUnderscores()
    await ctx.send(chosenWord)
    await ctx.send(tempUnderscoreArray)

client.run('NTc4MzY4NTI3NzY2MTI2NjEz.XN15Vw.TbHe8gQ2jGVkxbyqXTC2kiUxiS4')
