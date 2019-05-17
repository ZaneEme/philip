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
    if str(ctx.author) in valid_users:
        await ctx.send("quitting the bot")
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
async def help(ctx):
    embed = discord.Embed(title = "chatBot help", description = "some useful commands")
    embed.add_field(name = "philicia", value = "tells her I love her <3")
    embed.add_field(name = "!toggleReverseWords", value = "toggles whether all words will be reversed or not")
    embed.add_field(name = "!ping", value = "returns the bot's ping to the server")
    await ctx.send(embed = embed)



client.run('***REMOVED***')
