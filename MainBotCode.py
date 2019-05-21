import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix = '!')
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


@client.command(aliases = ["hangman", "Hangman", "HangMan"])
async def hangMan(ctx):

    author = ctx.author
    wordContainsChar = False
    wordList = ["banana", "choclolate", "coffee", "pancakes"]
    guessedChar = 'a'
    tempUnderscoreArray = []
    guessesLeft = 7
    chosenWord = "a"
    gameRunning = True
    input = 'a'
    guessedLetters = []


    def check(m):
            return m.author ==  author

    def chooseWord():
        nonlocal chosenWord
        chosenWord = random.choice(wordList)
        return chosenWord

    def setGameUnderscores():
        nonlocal tempUnderscoreArray; chosenWord
        for _ in range(0, len(chosenWord)):
            tempUnderscoreArray.append("--")


    chooseWord()
    setGameUnderscores()
    await ctx.send(chosenWord)
#    await ctx.send(tempUnderscoreArray)
    await ctx.send("Welcome to hangman")

    while gameRunning == True:
        await ctx.send(tempUnderscoreArray) #Print the array that shows guessed letters
        await ctx.send("Take a guess: \n")
        input = await client.wait_for('message', check = check) #wait for the person who started it to guess a letter
        guessedChar = input.content


        for a in range(0, len(chosenWord)): #if the word contains the guessed character replace the underscores
            if chosenWord[a] == guessedChar:
                tempUnderscoreArray.pop(a)
                tempUnderscoreArray.insert(a, guessedChar)
                wordContainsChar = True

        if wordContainsChar: #check to see if the word has the guesses character in it or not
            await ctx.send(f"The word does have a(n) {guessedChar} in it!\n")
        else:
            guessesLeft = guessesLeft - 1
            await ctx.send(f"Sorry, the word does not contain {guessedChar}")
            await ctx.send(f"You have {guessesLeft} guesses left")

        if guessesLeft == 0: #check to see if all guesses have been used
            await ctx.send(f"You have used all of your guesses. The correct word was {chosenWord}")
            gameRunning = False
            break

        for a in range(0, len(tempUnderscoreArray)): #test if the game array matches the word
            if chosenWord[a] == tempUnderscoreArray[a]:
                wordsMatch = True
            else:
                wordsMatch = False
                break

        if wordsMatch == True:
            await ctx.send("\nGood job! You guessed the word correctly!")
            await ctx.send(tempUnderscoreArray)
            break

        wordContainsChar = False
        guessedLetters.append(guessedChar) #add the guessed character to the list


client.run('NTc4MzY4NTI3NzY2MTI2NjEz.XN15Vw.TbHe8gQ2jGVkxbyqXTC2kiUxiS4')
