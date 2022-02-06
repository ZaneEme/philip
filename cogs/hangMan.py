import discord
from discord.ext import commands
import random


class hangMan(commands.Cog):
    def __init__(self, client):  # Initialize the cog
        self.client = client
        self.cheatMode = False

    #
    # If the user has the admin role, cheatmode allows
    # the user to see a list of all possible words
    #
    @commands.command()
    async def cheatmode(self, ctx):
        admin_role = discord.utils.get(ctx.guild.roles, name="Admin")

        if admin_role in ctx.author.roles:
            self.cheatMode = not self.cheatMode
            if self.cheatMode:
                await ctx.send("Turning on cheatMode for hangMan")
            else:
                await ctx.send("Turning off cheatMode for hangMan")
        else:
            await ctx.send("You are not allowed to use that command.")

    #
    # Main command for the game. Chooses a random word from wordlist,
    # and plays a game of standard Hangman.
    #
    @commands.command()
    async def hangman(self, ctx):
        wordContainsChar = False
        wordList = [
            "banana",
            "choclolate",
            "coffee",
            "pancake",
            "orange",
            "waffle",
            "omelette",
            "sandwich",
            "linguini",
            "alfredo",
            "burrito",
            "quesadilla",
            "apple",
            "grapefruit",
            "avocado",
            "coconut",
            "hamburger",
            "peanut",
            "honey",
            "pudding",
            "icecream",
            "broccoli",
            "watermelon",
            "burrito",
            "cheeseburger",
            "sushimi",
            "noodles",
            "barbecue",
            "macaroni",
            "sirloin",
            "wonton",
            "lemonade",
            "zucchini",
            "blueberry",
            "raspberry",
            "boisenberry",
            "lobster",
            "peanutbutter",
            "spaghetti",
            "lasagna",
            "breadsticks",
            "casserole",
            "gingerbread",
            "tamale",
            "cupcake",
            "stuffing",
            "ravioli",
            "meatballs",
            "croissant",
            "milkshake",
        ]

        game_thumbnails = [
            "https://i.imgur.com/44Jb4k2.png",
            "https://i.imgur.com/gXczhhM.png",
            "https://i.imgur.com/OHkzTXu.png",
            "https://i.imgur.com/1cgkwRQ.png",
            "https://i.imgur.com/ntOTFmt.png",
            "https://i.imgur.com/GwmPeX7.png",
            "https://i.imgur.com/jy490gk.png",
            "https://i.imgur.com/TR4gWeH.png",
        ]

        guessedChar = "a"
        tempUnderscoreArray = []
        guessesLeft = 7
        chosenWord = "a"
        gameRunning = True
        input = "a"
        guessedLetters = []
        admin_role = discord.utils.get(ctx.guild.roles, name="Admin")

        # Check if the last message sent was in the same channel as the bot
        # and if the last message wasn't sent by the bot
        def check(m):
            return m.author != self.client.user and m.channel == ctx.channel

        # Choose a random word from the list
        def chooseWord():
            nonlocal chosenWord
            chosenWord = random.choice(wordList)
            return chosenWord

        # Turn the random word from chooseWord() into a list of empty space
        def setGameUnderscores():
            nonlocal tempUnderscoreArray
            chosenWord
            for _ in range(0, len(chosenWord)):
                tempUnderscoreArray.append("--")

        chooseWord()
        setGameUnderscores()

        # Embed setup for game into Discord channel
        gameEmbedOne = discord.Embed(title="Welcome to Hangman!", color=0x008200)
        gameEmbedOne.set_author(name=ctx.author)
        gameEmbedOne.set_thumbnail(url="https://i.imgur.com/44Jb4k2.png")
        gameEmbedOne.add_field(
            name="Word progress",
            value=f"{', '.join(tempUnderscoreArray)}",
            inline=False,
        )
        gameEmbedOne.add_field(
            name="Information",
            value=f"No letters guessed yet.\nYou have 7 guesses remaining.",
            inline=False,
        )
        gameEmbedOne.add_field(name="\u200b", value="Enter a letter:")

        # Send the word list if player is an admin and cheats are on
        if admin_role in ctx.author.roles:
            if self.cheatMode:
                await ctx.send(wordList)

        # Main game loop
        while gameRunning == True:
            await ctx.send(embed=gameEmbedOne)
            input = await self.client.wait_for(
                "message", check=check
            )  # Wait for the person who started it to guess a letter

            if (
                input.content == "quitgame" or input.content == "endgame"
            ):  # Quit if the keyword is entered
                await ctx.send("Ending the game.")
                gameRunning = False
                break

            guessedChar = input.content

            # Check if the word contains guessed letter,
            # if true replace underscores with letter
            for a in range(0, len(chosenWord)):
                if chosenWord[a] == guessedChar:
                    tempUnderscoreArray.pop(a)
                    tempUnderscoreArray.insert(a, guessedChar)
                    wordContainsChar = True
                    gameEmbedOne.set_field_at(
                        index=0,
                        name="word progress",
                        value=f"{', '.join(tempUnderscoreArray)}",
                        inline=False,
                    )

            # Test if the word has the guessed character in it or not
            if wordContainsChar:
                gameEmbedOne.set_field_at(
                    index=1,
                    name="Information",
                    value=f"The word does have a(n) {guessedChar} in it!\nYou have {guessesLeft} guesses left.",
                    inline=False,
                )
            else:
                # Change game thumbnail, and subtract a guess
                guessesLeft = guessesLeft - 1
                gameEmbedOne.set_thumbnail(url=game_thumbnails[7 - guessesLeft])

                gameEmbedOne.set_field_at(
                    index=1,
                    name="Information",
                    value=f"Sorry, the word does not contain {guessedChar}.\nYou have {guessesLeft} guesses left.",
                    inline=False,
                )

            # Test if all guesses have been used and end game
            if guessesLeft == 0:
                gameEmbedOne.set_field_at(
                    index=1,
                    name="Information",
                    value=f"You have {guessesLeft} guesses left.\nThe correct word was {chosenWord}.",
                    inline=False,
                )

                gameEmbedOne.remove_field(index=2)
                await ctx.send(embed=gameEmbedOne)
                gameRunning = False
                break

            # Test if the guess array matches the chosen word
            for a in range(0, len(tempUnderscoreArray)):
                if chosenWord[a] == tempUnderscoreArray[a]:
                    wordsMatch = True
                else:
                    wordsMatch = False
                    break

            # if the guessed word matches the chosen word, end game
            if wordsMatch == True:
                await ctx.channel.purge(limit=2)
                gameEmbedOne.set_field_at(
                    index=0,
                    name="word progress",
                    value=f"{' '.join(tempUnderscoreArray)}",
                    inline=False,
                )
                gameEmbedOne.set_field_at(
                    index=1,
                    name="Information",
                    value=f"Good job! You guessed the word correctly with {guessesLeft} guesses remaining.",
                    inline=False,
                )
                gameEmbedOne.remove_field(index=2)

                gameRunning = False
                await ctx.send(embed=gameEmbedOne)
                break

            wordContainsChar = False
            guessedLetters.append(guessedChar)  # add the guessed character to the list
            gameEmbedOne.set_field_at(
                index=2,
                name=f"guessed letters: {', '.join(guessedLetters)}",
                value="Enter a letter:",
            )
            await ctx.channel.purge(limit=2)  # delete the last embed and guess


def setup(client):
    client.add_cog(hangMan(client))
