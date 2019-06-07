import discord
from discord.ext import commands
import random

class hangMan(commands.Cog):
    def __init__(self, client): #initialize the cog
        self.client = client
        self.cheatMode = False

    @commands.command()
    async def cheatmode(self, ctx): #if the user is an admin toggle listing of the possible words
        admin_role = discord.utils.get(ctx.guild.roles, name = "Admin")

        if admin_role in ctx.author.roles:
            self.cheatMode = not self.cheatMode
            if self.cheatMode:
                await ctx.send("Turning on cheatMode for hangMan")
            else:
                await ctx.send("Turning off cheatMode for hangMan")
        else:
            await ctx.send("You are not allowed to use that command.")

    @commands.command()
    async def hangman(self, ctx):
        wordContainsChar = False
        wordList = ["banana", "choclolate", "coffee", "pancake", "orange", "waffle", "omelette", "sandwich", "linguini", "alfredo", "burrito",
                    "quesadilla", "apple", "grapefruit", "avocado", "coconut", "hamburger", "peanuts", "honey", "pudding"]
        guessedChar = 'a'
        tempUnderscoreArray = []
        guessesLeft = 7
        chosenWord = "a"
        gameRunning = True
        input = 'a'
        guessedLetters = []
        admin_role = discord.utils.get(ctx.guild.roles, name = "Admin")

        def check(m):
                return m.author != self.client.user and m.channel == ctx.channel #if the last message was in same channel and not sent by bot return True

        def chooseWord(): #choose a random word from the list
            nonlocal chosenWord
            chosenWord = random.choice(wordList)
            return chosenWord

        def setGameUnderscores(): #turn the chosen word from chooseWord() into a list of empty spaces
            nonlocal tempUnderscoreArray; chosenWord
            for _ in range(0, len(chosenWord)):
                tempUnderscoreArray.append("--")


        chooseWord()
        setGameUnderscores()

        #Embed setup for game
        gameEmbedOne = discord.Embed(title = "Welcome to Hangman!", color = 0x008200)
        gameEmbedOne.set_author(name = ctx.author)
        gameEmbedOne.add_field(name = "Word progress", value = f"{tempUnderscoreArray}", inline = False)
        gameEmbedOne.add_field(name = 'Information', value = f"No letters guessed yet.\nYou have 7 guesses remaining.", inline = False)
        gameEmbedOne.add_field(name = "\u200b", value = "Enter a letter:")

        if admin_role in ctx.author.roles: #send the word list if player is an admin and cheats are on
            if self.cheatMode:
                await ctx.send(wordList)

        while gameRunning == True:
            await ctx.send(embed = gameEmbedOne)
            input = await self.client.wait_for('message', check = check) #wait for the person who started it to guess a letter

            if input.content == "quitgame" or input.content == "endgame": #quit if the keyword is entered
                await ctx.send("Ending the game.")
                gameRunning = False
                break

            guessedChar = input.content

            for a in range(0, len(chosenWord)): #if the word contains the guessed character replace the underscores
                if chosenWord[a] == guessedChar:
                    tempUnderscoreArray.pop(a)
                    tempUnderscoreArray.insert(a, guessedChar)
                    wordContainsChar = True
                    gameEmbedOne.set_field_at(index = 0, name = "word progress", value = f"{tempUnderscoreArray}", inline = False)

            if wordContainsChar: #test if the word has the guesses character in it or not
                gameEmbedOne.set_field_at(index = 1, name = "Information", value = f"The word does have a(n) {guessedChar} in it!\nYou have {guessesLeft} guesses left.", inline = False)
            else:
                guessesLeft = guessesLeft - 1
                gameEmbedOne.set_field_at(index = 1, name = "Information", value = f"Sorry, the word does not contain {guessedChar}.\nYou have {guessesLeft} guesses left.", inline = False)


            if guessesLeft == 0: #test if all guesses have been used
                gameEmbedOne.set_field_at(index = 1, name = "Information", value = f"{correctIncorrectString}\n{guessesRemainingString}\nYou have used all of your guesses. The correct word was {chosenWord}.", inline = False)
                gameRunning = False
                break

            for a in range(0, len(tempUnderscoreArray)): #test if the game array matches the word
                if chosenWord[a] == tempUnderscoreArray[a]:
                    wordsMatch = True
                else:
                    wordsMatch = False
                    break

            if wordsMatch == True: #if the guessed word matches the chosen word after the full for loop above, end game
                await ctx.channel.purge(limit = 2)
                await ctx.send(f"Good job! You guessed the word correctly with {guessesLeft} guesses remaining.")
                await ctx.send(chosenWord)
                gameRunning = False
                break

            wordContainsChar = False
            guessedLetters.append(guessedChar) #add the guessed character to the list
            gameEmbedOne.set_field_at(index = 2, name = f"guessed letters: {', '.join(guessedLetters)}", value = "Enter a letter:")
            await ctx.channel.purge(limit = 2) #delete the last embed and quess

def setup(client):
    client.add_cog(hangMan(client))
