####################################################
#                                                  #
#   AS 91906 – 3.7 - Develop a Computer Program    #
#            Copyright 2022 Tom Tamaira            #
#                     2 Apr 2022                   #
#                                                  #
####################################################
# Changelog:
# First Revision
# Fixed blurry text L81~

import random,os
from time import sleep

import pygame

#Defining a car racing class
class CarRacing:
    def __init__(self):

        pygame.init()#Initializing pygame
        self.display_width = 800#Window width
        self.display_height = 600#Window height
        self.root_path = os.getcwd()#Retrieve current working directory
        self.white = (255, 255, 255)#Set RGB code of text to white
        self.clock = pygame.time.Clock()#Generate the pygame clock object
        self.gameDisplay = None#Initially set the display to equal none
        self.fileRead()#Scan text file for high score data

        self.initialize()#Call game data initialization

    #This function will get and set data for game like images, lengths, widths, x, y
    def initialize(self):

        self.crashed = False#Set car crash value to false

        self.carImg = [pygame.image.load(os.path.dirname(__file__) + "/img/car1.png"),58,121]#A list containing the directory, width and height of the player's car model
        self.car_x_coordinate = (self.display_width * 0.45)#Set player car on x axis
        self.car_y_coordinate = (self.display_height * 0.8)#Set player car on y axis
        self.car_width = self.carImg[1]#Player car width
        self.car_height=self.carImg[2]#Player car height

        # enemy cars
        self.enemies = [[pygame.image.load(os.path.dirname(__file__) + "/img/car2.png"),59,119],
                            [pygame.image.load(os.path.dirname(__file__) + "/img/car3.png"),60,125],
                            [pygame.image.load(os.path.dirname(__file__) + "/img/car4.png"),65,132],
                            [pygame.image.load(os.path.dirname(__file__) + "/img/truck2.png"),84,221],
                            [pygame.image.load(os.path.dirname(__file__) + "/img/policecar.png"),74,155]]#A list containing the image, width, height of enemy cars

        self.enemy_car=random.choice(self.enemies)#Select a car randomly
        self.enemy_car_width = self.enemy_car[1]#Retrieve car width from the enemy_car list, width is 2nd entity of list
        self.enemy_car_height = self.enemy_car[2]#Retrieve car height from the enemy_car list, width is 2nd entity of list

        self.enemy_car_startx = random.randrange(240+25, 500,100)#Randomly select enemy car starting x from a list of three elements
        self.enemy_car_starty = -600#Enemy car y axis will be -600, ie not displayed on screen
        self.enemy_car_speed = 5#Set the speed of the enemy car


        # Background
        #Two bg images will be used one will be used at start, and other will be deployed at y -600
        #When 1st image reach's 600 the 2nd image (y=-600) will reach at zero and will be displayed on screen, thus two images will be displyed one after other
        self.bgImg = pygame.image.load(os.path.dirname(__file__) + "/img/backGrass.png")#Retrieve BG image of road and grass
        self.bg_x1 = 0#Set initial x of image 1
        self.bg_x2 = 0#Set initial x of image 2
        self.bg_y1 = 0#Set inital y of 1st image
        self.bg_y2 = -600#Set inital y of 1st image
        self.bg_speed = 3#Background speed
        self.count = 0#Var to track player score

    #Display player car image function
    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg[0], (car_x_coordinate, car_y_coordinate))#Blit shows image or text on screen at specified coordinates

    #This function will set windows title, width and height
    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))#Window size
        pygame.display.set_caption('AS 91906 by Tom Tamaira')#Title
        self.run_car()#Run the game

    #This function will start the game
    def run_car(self):
        self.gameDisplay.fill((34, 139, 24))#Fill BG with green. Without this function the text would be blurry.

        while not self.crashed:#Continuous loop until player car crash

            #This for loop will take all the types of events of either keyboard's key presses or mouse presses etc
            for event in pygame.event.get():#Getting any event
                if event.type==pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                if event.type == pygame.QUIT:#If event to detect pressing the cross on the window to close it
                    self.crashed = True#Set crashed to true

                if event.type == pygame.KEYDOWN:#Checking if event for keyboard key press
                    if event.key == pygame.K_LEFT:#Checking if event for keyboard left arrow key press
                        self.car_x_coordinate -= 100#Make car move left
                        print ("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    if event.key == pygame.K_RIGHT:#Checking if event for keyboard right arrow key press
                        self.car_x_coordinate += 100#Make car move right
                        print ("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    print ("x: {x}, y: {y}".format(x=self.car_x_coordinate, y=self.car_y_coordinate))


            self.back_ground_road()#Displaying the background

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)#Display the enemy car
            self.enemy_car_starty += self.enemy_car_speed#Increasing enemy car's y axis to make it look like it is moving

            if self.enemy_car_starty > self.display_height:#If enemy car reaches the bottom end of the screen
                self.enemy_car_starty = 0 - self.enemy_car_height#Make a new enemy car y position
                self.enemy_car_startx = random.randrange(240+25, 500,100)#Take enemey car x randomly as one of the three position in three lanes
                self.enemy_car=random.choice(self.enemies)#Selecting a random image for enemy and also its width and height
                self.enemy_car_width = self.enemy_car[1]#Enemy width
                self.enemy_car_height = self.enemy_car[2]#Enemy height

            self.car(self.car_x_coordinate, self.car_y_coordinate)#Display the player car
            self.highscore(self.HiScore,'High Score',600,0)#Display the high score
            self.highscore(self.count)#Display the current score of the player
            self.count += 1#Update the score
            if self.count % 1000 == 0 and self.count!=0:#After score is a multiple of x1000, then increase speed by 3
                self.enemy_car_speed += 1#Increase speed of enemy car
                self.bg_speed += 1#Increase BG speed

            #If enemy car hits the player car
            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True#Make crash variable true
                    if self.count>self.HiScore:#Check if current score is higher than high score
                        self.HiScore=self.count#Set current score as new high score
                        self.fileWrite()#Write updated high score to file
                    self.display_message("Game Over!")#Display game over message message

            #If player car goes off course
            if self.car_x_coordinate < 240 or self.car_x_coordinate > 540:
                self.crashed = True#Set crash variable to true to end the game
                if self.count>self.HiScore:#Check if current score is higher than high score
                    self.HiScore=self.count#Set current score as new high score
                    self.fileWrite()#Write updated high score to file
                self.display_message("Game Over!")#Display game over message

            pygame.display.flip()#Continuously update game screen to show any changes
            self.clock.tick(60)#FPS hard-limit


    #Display text function
    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)#Set font type and size for message
        text = font.render(msg, True, (255, 255, 255))#Set font color to RGB White
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))#Display the message on screen
        font = pygame.font.SysFont("comicsansms", 40, True)
        text = font.render('Press R to restart', True, (255, 0, 0))#Set font type and size for instructions
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 400 - text.get_height() // 2))#Show on screen
        pygame.display.flip()#Display changes on screen
        self.clock.tick(60)

        while self.crashed:#Loop will run as R is not pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:#Check if key is pressed
                    if event.key == pygame.K_r:#If pressed key is R
                        self.crashed=False#Set the crash variable to false to start game again and to break while loop above
                        break#Break for loop

        car_racing.initialize()#Again initializing the game specifications and data
        car_racing.racing_window()#Setting window and running game

    #Displaying the background on screen
    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))#Show 1st background image on screen
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))#Show 2nd background image on screen

        self.bg_y1 += self.bg_speed#Increasing value of the y axis of background 1
        self.bg_y2 += self.bg_speed#Increasing value of the y axis of background 2
        if self.bg_y1 >= self.display_height:#If 1st background reaches y=600
            self.bg_y1 = -600#Set its position to -600 where it starts again moving from top to bottom

        if self.bg_y2 >= self.display_height:#If the 2nd background y=600
            self.bg_y2 = -600#Set its position to -600 where it starts again moving from top to bottom

    #Show player car on screen
    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car[0], (thingx, thingy))#Player car will blit or display at specified coordinates

    #Show both current score and high score on screen
    def highscore(self, count,high='Score',x=0,y=0):
        font = pygame.font.SysFont("lucidaconsole", 20)#Retrieve system font
        text = font.render(high+" : " + str(count), True, self.white)#Render the font white on the score text
        self.gameDisplay.blit(text, (x, y))#Display the scores on the screen


    #This will read the text file
    def fileRead(self):
        fil=open(os.path.dirname(__file__) + '/score.txt')#Open scores text file
        self.HiScore=int(fil.read())#Retrieve the first line and convert it from string to integer
        fil.close()#Close text file

    #This will write score to text file
    def fileWrite(self):
        fil=open(os.path.dirname(__file__) + '/score.txt','w')#Open text file in write mode
        self.HiScore=fil.write(str(self.HiScore))#Write high score after converting to string in the text file
        fil.close()#Close text file

#Main run
if __name__ == '__main__':
    car_racing = CarRacing()#creating game
    car_racing.racing_window()#running it
