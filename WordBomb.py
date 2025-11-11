# all imports
import pygame # used to run the gmae
import random # used to get random words and characters for question
from spellchecker import SpellChecker # uses to check validity of words
spell = SpellChecker()

# pygame setup
pygame.init()
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth,screenHeight))
clock = pygame.time.Clock()
running = True

allLetters = "abcdefghijklmnopqrstuvwxyz"
inputWord = ("")

'''
to get a valid question, use english-words to generate a list of words,
use a random number generator to pick a word at random, then use another random
number generator to get a set of consecutive characters in that word?

to test words, run them through a spell check which invalidates the word
if it can be corrected or isn't recognisable?
'''   

def generateCharacters(length): # Generates a string of characters that has at least 1 valid word containing it
    while True:
        generatedString = ""
        lengthWord = random.randint(4,9) # uses this to generate a string of characters with length of 4-9
        for i in range(lengthWord):
            generatedString += random.choice(allLetters)
        generatedWord = spell.correction(generatedString) # generated string is put through spell correction to find a valid word
        if generatedWord != None:
            start = random.randint(0, len(generatedWord)-length)
            return (generatedWord[start:start+length])
        

incorrect = False
correct = False
incorrectTimer = 0
generatedCharacters = generateCharacters(2)
round = 0 # increments by 1 when a round ends, incorrect or correct word used
roundTimer = 0

# main game loop
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Updates - make it check for holding keys down, with a 50ms delay
            
            event.key -= 97 # letter A starts at 97, this reduces to 0 so it can be used for allLetters[]
            if event.key == -89: # backspace
                inputWord = inputWord[:-1] # slice notation to remove last character
            elif event.key <= 25 and event.key >= 0: # makes sure it's alphabetical
                inputWord += allLetters[event.key]
            else: # if any other key is pressed, attempt submit entered word
                if spell.correction(inputWord) == inputWord and len(inputWord) >= 3: # the spellcheck has a problem with 2 letter words, always allowing them
                    for i in range(len(inputWord)): # loops through the word
                        if inputWord[i:i+2] == generatedCharacters: # compares every collection of [length] characters to the required characters needed
                            correct = True
                            inputWord = ""
                        else:
                            pass
                    if correct != True:
                        incorrect = True
                        incorrectTimer = 0
                else:
                    incorrect = True
                    incorrectTimer = 0
    
    if correct == True:
        generatedCharacters = str(generateCharacters(2))
        round += 1
        roundTimer = 0
        correct = False
    elif roundTimer >= 600:
        round += 1
        roundTimer = 0
        incorrect = True
    
    xPosition = (screenWidth - 17*len(inputWord))/2 # default x and y position of word
    yPosition = screenHeight/2
    GCxPosition = (screenWidth - 17*len(generatedCharacters))/2
    GCyPosition = (screenHeight/2) - 40
    
    if incorrect == True: # turns word black and shakes for 0.5s if word is incorrect
        colour = (0,0,0)
        incorrectTimer += 1
        xPosition, yPosition = (xPosition + random.randint(-5,5)), (yPosition + random.randint(-2,2))
        GCxPosition, GCyPosition = (GCxPosition + random.randint(-5,5)), (GCyPosition + random.randint(-2,2))
        if incorrectTimer >= 30: # 30f = 0.5s
            incorrect = False
            incorrectTimer = 0
    else:
        colour = (255,255,255)
    
    font = pygame.font.SysFont('Consolas', 30) # monospace font so that text centering is easier
    inputWordTextSurface = font.render(inputWord, True, (colour))
        
    generatedCharactersTextSurface = font.render(generatedCharacters, True, (colour))
    
    # draw to screen
    screen.fill("red")
    screen.blit(inputWordTextSurface, (xPosition , yPosition))
    screen.blit(generatedCharactersTextSurface, (GCxPosition, GCyPosition))
    pygame.display.flip()
    
    roundTimer += 1
    clock.tick(60)

pygame.quit()