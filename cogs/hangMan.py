import discord
from discord.ext import commands
import random

class hangMan(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cheatMode = False

    @commands.command(aliases = ["cheatman", "cheatMan", "enableCheats", "cheatmode"])
    async def turnOnCheats(self, ctx):
        self.cheatMode = not self.cheatMode
        if self.cheatMode:
            await ctx.send("Turning on cheatMode for hangMan")
        else:
            await ctx.send("turning off cheatMode for hangMan")

    @commands.command()
    async def hangman(self, ctx):
        author = ctx.author
        wordContainsChar = False
        wordList = ["banana", "choclolate", "coffee", "pancakes", "oranges", "waffles", "omelettes", "sandwich", "linguini", "alfredo", "burrito", "quesadilla", "apple", "grapefruit", "avocado", "coconut"]
        guessedChar = 'a'
        tempUnderscoreArray = []
        guessesLeft = 7
        chosenWord = "a"
        gameRunning = True
        input = 'a'
        guessedLetters = []
        correctIncorrectString = "No letters guessed yet."
        guessesRemainingString = "You have 7 guesses remaining"
        stringVal = "a"
        letterIsLegal = False

        def check(m):
                return m.author == author

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
        #await ctx.send(chosenWord)
        #await ctx.send("Welcome to hangman")

        gameEmbedOne = discord.Embed(title = "Welcome to Hangman!", color = 0x008200)
        gameEmbedOne.set_author(name = ctx.author)
        gameEmbedOne.add_field(name = "Word progress", value = f"{tempUnderscoreArray}", inline = False)
        gameEmbedOne.add_field(name = 'Information', value = f"{correctIncorrectString}\n{guessesRemainingString}", inline = False)
        gameEmbedOne.add_field(name = "\u200b", value = "Enter a Letter:")

        if self.cheatMode:
            await ctx.send(wordList)

        while gameRunning == True:
            #await ctx.send(tempUnderscoreArray) #Print the array that shows guessed letters
            #await ctx.send("Take a guess: \n")
            await ctx.send(embed = gameEmbedOne)

            input = await self.client.wait_for('message') #wait for the person who started it to guess a letter

            if input.content == "quitgame":
                await ctx.send("ending the game")
                gameRunning = False
                break

            guessedChar = input.content
            stringVal = ""

            for a in range(0, len(chosenWord)): #if the word contains the guessed character replace the underscores
                if chosenWord[a] == guessedChar:
                    tempUnderscoreArray.pop(a)
                    tempUnderscoreArray.insert(a, guessedChar)
                    wordContainsChar = True
                    gameEmbedOne.set_field_at(index = 0, name = "word progress", value = f"{tempUnderscoreArray}", inline = False)

            if wordContainsChar: #test if the word has the guesses character in it or not
                correctIncorrectString = f"The word does have a(n) {guessedChar} in it!"
                guessesRemainingString = f"You have {guessesLeft} guesses left"
                stringVal = f"{correctIncorrectString}\n{guessesRemainingString}"
                gameEmbedOne.set_field_at(index = 1, name = "Information", value = stringVal, inline = False)
            else:
                guessesLeft = guessesLeft - 1
                correctIncorrectString = f"Sorry, the word does not contain {guessedChar}"
                guessesRemainingString = f"You have {guessesLeft} guesses left"
                stringVal = f"{correctIncorrectString}\n{guessesRemainingString}"
                gameEmbedOne.set_field_at(index = 1, name = "Information", value = stringVal, inline = False)


            if guessesLeft == 0: #test if all guesses have been used
                stringVal = f"{correctIncorrectString}\n{guessesRemainingString}\nYou have used all of your guesses. The correct word was {chosenWord}"
                gameEmbedOne.set_field_at(index = 1, name = "Information", value = stringVal, inline = False)
                gameRunning = False
                break

            for a in range(0, len(tempUnderscoreArray)): #test if the game array matches the word
                if chosenWord[a] == tempUnderscoreArray[a]:
                    wordsMatch = True
                else:
                    wordsMatch = False
                    break

            if wordsMatch == True: #test if the guessed word matches the chosen word
                await ctx.channel.purge(limit = 2)
                await ctx.send(f"Good job! You guessed the word correctly! with {guessesLeft} guesses remaining.")
                await ctx.send(chosenWord)
                gameRunning = False
                break

            wordContainsChar = False
            guessedLetters.append(guessedChar) #add the guessed character to the list
            await ctx.channel.purge(limit = 2)

def setup(client):
    client.add_cog(hangMan(client))
