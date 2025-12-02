# all imports
# used for actually running the game
import pygame 
import random 
# used for multiplayer
import socket
import threading
import sys
# spellcheck
from spellchecker import SpellChecker # uses to check validity of words
spell = SpellChecker()


# server setup
# https://www.techwithtim.net/tutorials/python-online-game-tutorial/server
# tutorial in case this is wrong
server = "test"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as error:
    str(error)

s.listen(2)

# pygame setup
pygame.init()
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth,screenHeight))
clock = pygame.time.Clock()
running = True


# word setup
allLetters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
letterFrequency = [0.0797, 0.0203, 0.0413, 0.0381, 0.1174, 0.0135, 0.0284, 0.0215, 0.0865, 0.0020, 0.0088, 0.0535, 0.0270, 0.0742, 0.0594, 0.0277, 0.0019, 0.0744, 0.0815, 0.0676, 0.0322, 0.0109, 0.0085, 0.0029, 0.0165, 0.0045]
inputWord = ("")
allEnteredWords = []

def generateCharacters(lengthCharacters, lengthWord): # Generates a string of characters that has at least 1 valid word containing it
    # lengthWord is more of a suggestion than a restriction, generatedString will be of length lengthWord but spellcheck may make a correction to a word of similar, but not the same length
    # i.e. lengthWord = 5 may return words of length 4,5,6
    
    # random.choices() solves previously seen lag, as there are less loops spent generating words with unlikely characters such as x,y,z that would be very unlikely to generate a real word
    
    while True:
        generatedString = random.choices(allLetters, letterFrequency, k=lengthWord) # letters are weighted by how often they appear in common words
        generatedString = ''.join(generatedString) # turns the list returned by random.choices() into a string which can be spellchecked
        generatedWord = spell.correction(generatedString) # generated string is put through spell correction to find a valid word
        if generatedWord != None:
            if generatedWord.find("'") == -1: # some generated words contained ', e.g. (www's), which then generated characters impossible to type
                if len(generatedWord) > 3: # words with length <=3 aren't allowed to be submitted, so they shouldn't be allowed to generate characters
                    start = random.randint(0, len(generatedWord)-lengthCharacters)
                    print (generatedWord)
                    return (generatedWord[start:start+lengthCharacters])
        

incorrect = False
correct = False
incorrectTimer = 0
generatedCharacters = generateCharacters(2, 5)
round = 0 # increments by 1 when a round ends, incorrect or correct word used
roundTimer = 0
lives = 3

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
                            if inputWord not in allEnteredWords: # checks if word already given before
                                correct = True
                                allEnteredWords.append(str(inputWord))
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
        generatedCharacters = str(generateCharacters(2, 5))
        round += 1
        roundTimer = 0
        correct = False
    elif roundTimer >= 600:
        round += 1
        roundTimer = 0
        incorrect = True
        lives -= 1
        if lives == 0:
            pygame.quit()
    
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
        
    GCTextSurface = font.render(generatedCharacters, True, (colour))
    
    # draw to screen
    
    screen.fill("red") # background color
    # these 2 rects form the countdown timer, showing how much time is left
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(((screenWidth-600)/2), (screenHeight/2 + 100), 600, 10))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(((screenWidth-600)/2 + (600 - roundTimer)), (screenHeight/2 + 100), roundTimer, 10))
    
    heartIcon = pygame.image.load("heart.png").convert()
    
    # prints 3 heart icons, evenly spaced, above the timer
    for i in range(lives):
        screen.blit(heartIcon, (((screenWidth-35*lives)/2+35*i), (screenHeight/2+50)))
    
    
    screen.blit(inputWordTextSurface, (xPosition , yPosition))
    screen.blit(GCTextSurface, (GCxPosition, GCyPosition))
    pygame.display.flip()
    
    roundTimer += 1
    clock.tick(60)

pygame.quit()