# Evil Hangman in Python 3.9.6 by Joseph Calles

import os
import random

def clearScreen() :
    os.system('cls' if os.name == 'nt' else 'clear')
# END clearScreen()

def chooseGame() :

    while (True) :

        print("Would you like you play normal hangman or evil hangman?")
        choice = input("Choose ('normal' or 'evil') : ")

        if (choice == "normal" or choice == "evil") : 
            break
        else:
            print("I dont understand")
            continue

    return choice
# END chooseGame()

def getNumLetters(excludedValues) :

    while True :

        letters = input("How many letters to you want to play with? : ")

        try:
            letters = int(letters)
            if letters < 1 or letters > 31 or letters in excludedValues :
                print("there are no words with that many letters, pick again")
                continue
            break
        except :
            print("I dont understand")
            continue

    return letters
# END getNumLetters()

def getNumGuesses() :

    while True:

        guesses = input("How many guesses to you want to play with? : ")

        try:
            guesses = int(guesses)
            if guesses < 1 :
                print("please pick a number greater than 0")
                continue
            break
        except:
            print("I dont understand")
            continue

    return guesses
# END getNumGuesses()

def getLetterGuess(guessedList) :

    while True :

        while True :
            guess = input("Pick a letter to guess (type '!' to show history): ")
            if (guess.isalpha() and len(guess) == 1) : 
                break
            elif guess == "!":
                print("Guessed: ", end="")
                print(guessedList)
            else :
                print("I don't understand")
                continue
        
        if guess in guessedList :
            print("You have already guessed that letter")
            print("Guessed: ", end="")
            print(guessedList)
            continue
        else :
            break

    guessedList.append(guess)
    guessedList.sort()

    return (guess, guessedList)
# END getLetterGuess()

def getWordKey(workingKey, word, guess) :

    key = ""

    i = 0
    while i < len(word) :
        if word[i] == guess :
            key += guess
        else :
            key += workingKey[i]
        i = i + 1
          
    return key
# END getWordKey()

def getNewWordFamily(workingKey, currentWordFamily, guess) :

    # initialize a storage for pairs {wordKey : wordList}
    # where all words in wordList follow the pattern of wordKey
    associativeArray = {}

    for word in currentWordFamily :

        # replace '-' with guess where in word
        wordKey = getWordKey(workingKey, word, guess)

        # insert the word into the associativeArray with respect to the wordKey
        if wordKey in associativeArray :
            associativeArray[wordKey].append(word)
        else :
            associativeArray[wordKey] = [word]

    print("Word families: (guess = " + guess + ")")

    # print out all keys and count of members
    for (key, value) in sorted(associativeArray.items(), key=lambda x : -len(x[1])) :
        print(key, " : ", len(value))
    print("")

    # return largest word family (the 'evil' part of 'evil hangman')
    return max(associativeArray.items(), key=lambda x : len(x[1]))
# END getNewWordFamily()

def evilHangmanGameLoop(currentWordFamily, totalGuesses) :

    # initialize working key as string of all '-'
    workingKey = '-' * len(currentWordFamily[0])

    guessedList = []
    guesses = totalGuesses

    while guesses > 0 :

        (guess, guessedList) = getLetterGuess(guessedList)
        guesses -= 1

        clearScreen()
        print("Guessed: ", end="")
        print(guessedList)
        print("Guesses remaining: " + str(guesses) + " / " + str(totalGuesses))

        # choose the word family with the most members
        (workingKey, currentWordFamily) = getNewWordFamily(workingKey, currentWordFamily, guess)

        # if no backup options remain, conceed that the user has won
        if len(currentWordFamily) == 1 and '-' not in workingKey :
            print("You won! The word was \"" + currentWordFamily[0] + "\"")
            return None
        elif guesses > 0:
            print("The word is: \"" + workingKey + "\"")

    # once the user runs out of guesses 
    print ("You ran out of guesses. Better luck next time!")
    print("The word was \"" +
          currentWordFamily[random.randint(0, len(currentWordFamily) - 1)] + "\"")

    return None
# END evilHangmanGameLoop()

def normalHangmanGameLoop(currentWordFamily, totalGuesses) :

    # pick a random word from currentWordFamily
    word = currentWordFamily[random.randint(0, len(currentWordFamily) - 1)]

    # initialize working key as string of all '-'
    workingKey = '-' * len(currentWordFamily[0])

    guessedList = []
    guesses = totalGuesses

    while guesses > 0 :

        (guess, guessedList) = getLetterGuess(guessedList)
        guesses -= 1

        clearScreen()

        print("Guessed: ", end="")
        print(guessedList)
        print("Guesses remaining: " + str(guesses) + " / " + str(totalGuesses))

        # replace '-' with guess where in word 
        workingKey = getWordKey(workingKey, word, guess)

        if '-'not in workingKey : # if all letters have been guessed
            print("You won! The word was \"" + word + "\"")
            return None
        elif guesses > 0 : 
            print("The word is: \"" + workingKey + "\"")

    # once the user runs out of guesses 
    print("You ran out of guesses. Better luck next time!")
    print("The word was \"" + word + "\"")

    return None
# END normalHangmanGameLoop()

def main() :

    clearScreen()

    # initalize list for word lists
    wordFamilies = [[] for i in range(32)]

    wordCount = 0       #
    index = 0           #
    excludedValues = [] # list of invalid word lengths

    dictionary = open("dictionary.txt", "r")

    # extract words from dictionary and arrange them for use
    for word in dictionary :
        wordFamilies[len(word) - 1].append(word.replace("\n", ""))
        wordCount += 1
        
    # find invalid word lengths
    while index < 32 :
        if len(wordFamilies[index]) == 0 :
            excludedValues.append(index)
        index += 1

    dictionary.close()

    print("Welcome to hangman! There are " + str(wordCount) + " words in my dictionary.")

    # get user preferences
    choice = chooseGame()
    letters = getNumLetters(excludedValues)
    guesses = getNumGuesses()

    currentWordFamily = wordFamilies[letters]

    clearScreen()

    # start main game loop
    if choice == "evil" :
        evilHangmanGameLoop(currentWordFamily, guesses)
    elif choice == "normal" :
        normalHangmanGameLoop(currentWordFamily, guesses)

    return None
# END main()

if __name__ == "__main__" :
    main() 
