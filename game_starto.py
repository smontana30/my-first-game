import pygame
import time
import random

pygame.init()

crash_sound = pygame.mixer.Sound("Car Screech And Crash-SoundBible.com-1414562045.wav")
pygame.mixer.music.load("JoJo Part 3 Stardust Crusaders - Opening 2 FullSono Chi no Kioku end of THE WORLD (online-audio-converter.com).wav")

display_width = 800
display_height = 600

#how to define colors in pygames
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,150,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53,112,255)
car_width = 73
pause = True

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Race car game")
clock = pygame.time.Clock()
carImg = pygame.image.load('racecar.png')



def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " +str(count), True, black)
    gameDisplay.blit(text, (0,0))

def things(thingx, thingy, thingw, thingh, color, count):
     pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    # for i in range(count):
    #     if (thingx > 800):
    #         thingx = thingx / 5
    #     pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    #     thingx *= 2.8


def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)


    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)


        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, width, height, inactive, active, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active,(x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactive,(x,y,width , height))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(width / 2)), (y + (height / 2)))
    gameDisplay.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def paused():

    pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)


    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)


        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 110)
        TextSurf, TextRect = text_objects("Race car game", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Go!", 150,450,100,50, green, bright_green, game_loop)
        button("Quit", 550,450,100,50, red, bright_red, quitgame)
        # pygame.draw.rect(gameDisplay, red,(550,450,100,50))

        pygame.display.update()
        clock.tick(15)




def game_loop():
    global pause
    pygame.mixer.music.play(-1)

    x = (display_width * .45)
    y = (display_height * .8)

    x_change = 0
    #how we make our blocks that we want the car to avoid
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
    dodged = 0
    things_count = 1
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            print(event)
            #these if statements add movement to the car
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        #adding the new x coordinate to the car location func
        x += x_change

        #add white background then adds car pick
        gameDisplay.fill(white)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color, 1)
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)
        #need to add minus car_width bc if not add the boundry of the rightside
        # is off
        if x > display_width - car_width or x < 0:
            crash()
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx =  random.randrange(0, display_width)
            dodged += 1
            thing_speed += .5
            # thing_width += (dodged * 1.2)
            things_count += 1

        if y < thing_starty + thing_height:
            print("y crossover")
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                print("x crossover")
                crash()

        pygame.display.update()
        clock.tick(60)

#make the game_loop func run
game_intro()
game_loop()
pygame.quit()
quit()
