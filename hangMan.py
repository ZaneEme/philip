
import random

# setup variables
chosenWordString = "a"
temporaryUnderScoresArray = [] #what's printed to and used in the actual game
guessedLetters = [] #letters that have already been guessed
guessesRemaining = 7
gameRunning = True
words = ["secretary", "substantial", "imported", "jellyfish", "abundant", "misled", "geese", "forsake", "pollute", "blueberry", "oranges", "cactus"]
guessedChar = ''
wordsMatch = False
wordContainsChar = False

def chooseRandomFromList(wordList): #choose a random word from the list
    wordNum = random.randint(0, len(wordList) - 1)
    chosenWordString = words[wordNum] #testing, for some reason doesn't actually work? No idea
    return chosenWordString


def setTemporaryUnderScoresArray(): #create a list of underscores the same length as the word
    for i in range(0, len(chosenWordString)):
        temporaryUnderScoresArray.append('_')

#Main code area

chosenWordString = chooseRandomFromList(words)
print("\nWelcome to Hangman!")
setTemporaryUnderScoresArray()

while gameRunning == True:
    print(str(temporaryUnderScoresArray)) #Print the array that shows guessed letters
    guessedChar = input("Take a guess: \n")

    for a in range(0, len(chosenWordString)): #if the word contains the guessed character replace the underscores
        if chosenWordString[a] == guessedChar:
            temporaryUnderScoresArray.pop(a)
            temporaryUnderScoresArray.insert(a, guessedChar)
            wordContainsChar = True

    if wordContainsChar:
        print("The word does have a(n) " + guessedChar + " in it!\n")
    else:
        guessesRemaining = guessesRemaining - 1
        print("Sorry, the word does not contain " + guessedChar)
        print("You have " + str(guessesRemaining) + " guesses left")

    if guessesRemaining == 0:
        print("You have used all of your guesses. The correct word was " + chosenWordString)
        gameRunning = False
        break

    for a in range(0, len(temporaryUnderScoresArray)): #test if the game array matches the word
        if chosenWordString[a] == temporaryUnderScoresArray[a]:
            wordsMatch = True
        else:
            wordsMatch = False
            break

    if wordsMatch == True:
        print("\nGood job! You guessed the word correctly!")
        print(temporaryUnderScoresArray)
        break

    wordContainsChar = False
    guessedLetters.append(guessedChar) #add the guessed character to the list
