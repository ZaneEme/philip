import discord
from discord.ext import commands
import random

class hangMan(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command(aliases = ["hangman", "Hangman", "HangMan"])
    async def hangMan(self, ctx):

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
    #    await ctx.send(chosenWord)
        await ctx.send("Welcome to hangman")

        while gameRunning == True:
            await ctx.send(tempUnderscoreArray) #Print the array that shows guessed letters
            await ctx.send("Take a guess: \n")
            input = await self.client.wait_for('message') #wait for the person who started it to guess a letter
            guessedChar = input.content


            for a in range(0, len(chosenWord)): #if the word contains the guessed character replace the underscores
                if chosenWord[a] == guessedChar:
                    tempUnderscoreArray.pop(a)
                    tempUnderscoreArray.insert(a, guessedChar)
                    wordContainsChar = True

            if wordContainsChar: #check to see if the word has the guesses character in it or not
                await ctx.send(f"The word does have a(n) {guessedChar} in it!\n")
                await ctx.send(f"You have {guessesLeft} guesses left")
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

def setup(client):
    client.add_cog(hangMan(client))
