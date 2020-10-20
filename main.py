"""
Halloween Bingo by F. Milburn
October, 2020

To play:
    space bar will draw the next monster for display
    monsters can only be drawn after 5 seconds has elapsed
    start a new game with the "n" key on the keyboard
    quit the game with "q" key or by closing the window
"""

# import modules
import pygame
from pygame import mixer
import random
import os

# set up the game
pygame.init()
screen = pygame.display.set_mode((1200, 800))   # window width, height
pygame.display.set_caption('Monster Bingo')     # window caption
icon = pygame.image.load('jack-o-lantern.png')  # window icon
pygame.display.set_icon(icon)

# background screen
bgd = pygame.image.load('background.jpg')

# empty list of monsters that will be popped from the randomized monster list
popMonster = []

# X, Y location for drawing a monster
monsterX = 200
monsterY = 200

# declare the monster images in a list
monster = [
    '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg',          # red
    '9.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.jpg', '16.jpg',   # green
    '17.jpg', '18.jpg', '19.jpg', '20.jpg', '21.jpg', '22.jpg', '23.jpg', '24.jpg',  # blue
    '25.jpg', '26.jpg', '27.jpg', '28.jpg', '29.jpg', '30.jpg', '31.jpg', '32.jpg',  # purple
    '33.jpg', '34.jpg', '35.jpg', '36.jpg', '37.jpg', '38.jpg', '39.jpg', '40.jpg']  # yellow


# initializes a new game by shuffling monsters, clearing any drawn monster from the last game, and playing intro music
def init_game():

    # shuffle the monster images and clear the popMonster list
    random.shuffle(monster)
    popMonster.clear()

    # play background sound
    # JS Bach Toccata & Fugue in D-minor BWV 565 from www.ctunes.eu
    mixer.music.load("bach_toccata.mp3")
    mixer.music.play()


# displays instructions until the game has started
def display_instructions():

    yellow = (255, 255, 0)
    red = (255, 0, 0)

    tiny_font = pygame.font.Font("Deutsch.ttf", 16)
    small_font = pygame.font.Font("Deutsch.ttf", 50)
    large_font = pygame.font.Font("Deutsch.ttf", 100)

    text = large_font.render("Hello", True, red)
    screen.blit(text, (300, 300))
    text = large_font.render("Monsters!", True, red)
    screen.blit(text, (230, 400))

    text = small_font.render("For next monster", True, yellow)
    screen.blit(text, (850, 150))
    text = small_font.render("press space", True, yellow)
    screen.blit(text, (850, 220))
    text = small_font.render("For new game", True, yellow)
    screen.blit(text, (850, 360))
    text = small_font.render("press n", True, yellow)
    screen.blit(text, (850, 430))

    text = tiny_font.render("F Milburn  Halloween 2020", True, yellow)
    screen.blit(text, (980, 750))


# game global parameters and initialization
gameStarted = False      # displays instructions until true
updateWaitTime = 5000    # time to wait before allowing a new Bingo game update in milliseconds
updateTime = 0           # time at which a new update can occur
playing = True           # turns false when game is exited
init_game()              # initialize a new game

# game loop
while playing:

    # set the background (R, G, B)
    background = (0, 0, 0)
    screen.fill(background)

    # provision to end game by closing window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    # check for pressed key and user input
    if event.type == pygame.KEYDOWN:

        # check if a request to draw a new monster was made by pressing the space bar
        # and that sufficient time has passed to allow an update to game play
        if event.key == pygame.K_SPACE and pygame.time.get_ticks() > updateTime:

            # set the game start to true and determine when next update to game play is allowed
            gameStarted = True
            updateTime = pygame.time.get_ticks() + updateWaitTime

            # pop a new monster image from the shuffled monster list for display
            popMonster.append(monster.pop())
            newMonster = pygame.image.load(popMonster[-1])

            # determine the type monster (there are 8 numbered types arranged sequentially in order of the 5 colors)
            # and play the associated sound for the monster
            stringNumber = popMonster[-1].split('.')
            monsterNumber = int(stringNumber[0]) % 8
            if monsterNumber == 7:
                scarySound = mixer.Sound("monster.wav")
            elif monsterNumber == 6:
                scarySound = mixer.Sound("house.wav")
            elif monsterNumber == 5:
                scarySound = mixer.Sound("ghost.wav")
            elif monsterNumber == 4:
                scarySound = mixer.Sound("cyclops.wav")
            elif monsterNumber == 3:
                scarySound = mixer.Sound("clown.wav")
            elif monsterNumber == 2:
                scarySound = mixer.Sound("cat.wav")
            elif monsterNumber == 1:
                scarySound = mixer.Sound("bug.wav")
            elif monsterNumber == 0:
                scarySound = mixer.Sound("witch.wav")

            scarySound.play()

        # check to see if a new game is requested with the n key
        elif event.key == pygame.K_n:
            init_game()
            gameStarted = False

        # check to see if a quit game is requested with the q key
        elif event.key == pygame.K_q:
            playing = False

    # draw the background image
    screen.blit(bgd, (0,0))

    # if the game has started then update the game state
    if gameStarted:

        # display the newest Monster
        screen.blit(newMonster, (monsterX, monsterY))

        # display the older Monsters
        xCoord = 830
        yCoord = 50
        for i in range(0, len(popMonster)):
            smallMonster = pygame.image.load(popMonster[i])
            smallMonster = pygame.transform.scale(smallMonster, (64, 64))
            screen.blit(smallMonster, (xCoord, yCoord))
            xCoord += 64
            if (i + 1) % 5 == 0:
                yCoord += 64
                xCoord = 830

    # else game has not started, give instructions for playing
    else:
        display_instructions()

    # update the display
    pygame.display.update()
