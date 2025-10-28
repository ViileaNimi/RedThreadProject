# all imports
import pygame # used to run the gmae
import random # used to get random words and characters for question
import enchant # used to check input word

d = enchant.Dict("en_UK") # doesn't work?

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
            elif event.key <= 23 and event.key >= 0: # makes sure it's alphabetical
                inputWord += allLetters[event.key]
            else: # if any other key is pressed, attempt submit entered word
                if d.check(inputWord) == True:
                    print ("True")
                else:
                    print ("False")
    
    font = pygame.font.SysFont('Consolas', 30) # monospace font so that text centering is easier
    text_surface = font.render(inputWord, True, (255, 255, 255))
    
    # draw to screen
    screen.fill("red")
    screen.blit(text_surface, ((screenWidth - 17*len(inputWord))/2,screenHeight/2)) # pos (x, y)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()