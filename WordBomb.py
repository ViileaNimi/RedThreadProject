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

incorrect = False
incorrectTimer = 0

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
                    inputWord = ""
                else:
                    incorrect = True
                    incorrectTimer = 0
    
    xPosition = (screenWidth - 17*len(inputWord))/2 # default x and y position of word
    yPosition = screenHeight/2
    if incorrect == True: # turns word black and shakes for 0.5s if word is incorrect
        colour = (0,0,0)
        incorrectTimer += 1
        xPosition, yPosition = (xPosition + random.randint(-5,5)), (yPosition + random.randint(-1,1))
        if incorrectTimer >= 30: # 30f = 0.5s
            incorrect = False
            incorrectTimer = 0
    else:
        colour = (255,255,255)
    
    font = pygame.font.SysFont('Consolas', 30) # monospace font so that text centering is easier
    text_surface = font.render(inputWord, True, (colour))
    
    # draw to screen
    screen.fill("red")
    screen.blit(text_surface, (xPosition , yPosition))
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()