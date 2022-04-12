####################################################
#                                                  #
#   AS 91906 – 3.7 - Develop a Computer Program    #
#            Copyright 2022 Tom Tamaira            #
#                     12 Apr 2022                  #
#                                                  #
####################################################
# Changelog:
# Added empty or invalid entry high score file check

import random,os
from time import sleep

import pygame

#Car class
class Car:
    def __init__(self,path,width,height,x,y,speed=None):
        self.img=pygame.image.load(path)#Load the image of car
        self.width=width#Setting its width
        self.height=height#Setting its height
        self.x=x#Setting its x coorindate
        self.y=y#Setting its y coordinates
        self.speed=speed#Setting its speed

    #This magic method will help in changing y coordinate of car
    def __add__(self,other):
        if type(other)==Car:#If added value belongs to car class
            self.y=self.y+other.y#Add other y parameter to self y parameter
        else:#Otherwise just add other to self y
            self.y=self.y+other

#Defining a car racing class
class CarRacing:
    def __init__(self):

        pygame.init()#Initializing pygame
        self.display_width = 800#Window width
        self.display_height = 600#Window height
        self.root_path = os.getcwd()#Retrieve current working directory
        self.white = (255, 255, 255)#white colro for displaying text
        self.clock = pygame.time.Clock()#Generate the pygame clock object
        self.gameDisplay = None#Initially set the display to equal none
        try:#If socre file exists then
            self.fileRead()#Read the text file to read high score
        except:#If score file is deleted then
            self.HiScore=0#Set high score as zero
            self.fileWrite()#Write and make new score file
        self.initialize()#Call game data initialization


    #This function will get and set data for game like images, lengths, widths, x, y
    def initialize(self):

        self.crashed = False#Set car crash value to false

        self.carImg = [pygame.image.load(os.path.dirname(__file__) + "/img/car1.png"),58,121]#A list containing the directory, width and height of the player's car model
        self.car_x_coordinate = (self.display_width * 0.45)#Set player car on x axis
        self.car_y_coordinate = (self.display_height * 0.8)#Set player car on y axis
        self.car_width = self.carImg[1]#Player car width
        self.car_height=self.carImg[2]#Player car height

        #Enemy cars as car objects are created
        self.enemies = [Car(os.path.dirname(__file__) + "/img/car2.png",59,119,random.randrange(240+25, 500,100),-119),
                            Car(os.path.dirname(__file__) + "/img/car3.png",60,125,random.randrange(240+25, 500,100),-125),
                            Car(os.path.dirname(__file__) + "/img/car4.png",65,132,random.randrange(240+25, 500,100),-132),
                            Car(os.path.dirname(__file__) + "/img/truck2.png",84,221,random.randrange(240+25, 500,100),-221),
                            Car(os.path.dirname(__file__) + "/img/policecar.png",74,155,random.randrange(240+25, 500,100),-155)]#A list containing the image, width, height of enemy cars



        self.enemy_car=random.choice(self.enemies)#Select a car randomly
        self.enemy_car_width = self.enemy_car.width#Retrieve car width from the enemy_car list, width is 2nd entity of list
        self.enemy_car_height = self.enemy_car.height#Retrieve car height from the enemy_car list, width is 2nd entity of list

        self.enemy_car_startx = random.randrange(240+25, 500,100)#Randomly select enemy car starting x from a list of three elements
        self.enemy_car_starty = self.enemy_car.y#Enemy car y axis will be -600, ie not displayed on screen
        self.enemy_car_speed = random.choice([4,5,7,10])#Set the speed of the enemy car


        # Background
        #Two bg images will be used one will be used at start, and other will be deployed at y -600
        #When 1st image reach's 600 the 2nd image (y=-600) will reach at zero and will be displayed on screen, thus two images will be displyed one after other
        self.bgImg = pygame.image.load(os.path.dirname(__file__) + "/img/backGrass.png")#Retrieve BG image of road and grass
        self.bg_x1 = 0#Set initial x of image 1
        self.bg_x2 = 0#Set initial x of image 2
        self.bg_y1 = 0#Set inital y of 1st image
        self.bg_y2 = -600#Set inital y of 1st image
        self.bg_speed = 6#Background speed
        self.count = 0#Var to track player score

    #Display player car image function
    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg[0], (car_x_coordinate, car_y_coordinate))#Blit shows image or text on screen at specified coordinates

    #This function will set the game window title, width and height
    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))#Window size
        pygame.display.set_caption('AS 91906 by Tom Tamaira')#Title
        self.run_car()#Run the game

    #This function will start the game
    def run_car(self):
        self.gameDisplay.fill((34, 139, 24))#fill the background with green. Not doing this will make the text display blurred so it is necessary
        playerX_change = 0
        while not self.crashed:#Continuous loop until player car crash

            #This for loop will take all the types of events of either keyboard's key presses or mouse presses etc
            for event in pygame.event.get():#Getting any event
                if event.type == pygame.QUIT:#If event to detect pressing the cross on the window to close it
                    self.crashed = True#Set crashed to true
                if event.type == pygame.KEYDOWN:#Check if key is pressed down and is kept down then
                    if event.key == pygame.K_LEFT:#If key pressed is left arrow
                        playerX_change = -10#Rate of x motion changed to equal -10
                    if event.key == pygame.K_RIGHT:#If key pressed is right arrow
                        playerX_change = 10#Rate of x motion changed to equal 10
                if event.type == pygame.KEYUP:#when that pressed key is released then
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        playerX_change = 0#Rate of x motion changed to equal 0

            self.car_x_coordinate+=playerX_change
            self.back_ground_road()#Displaying the background

            self.run_enemy_car(self.enemy_car.img,self.enemy_car_startx, self.enemy_car_starty)#Display the enemy car
            self.enemy_car_starty += self.enemy_car_speed#incrementing enemy car's y to make it look like it is moving

            if self.enemy_car_starty > self.display_height:#If enemy car reaches the bottom end of the screen
                self.count += 1#Update the score
                self.enemy_car=random.choice(self.enemies)#Selecting a random image for enemy and also its width and height
                self.enemy_car_width = self.enemy_car.width#Enemy width
                self.enemy_car_height = self.enemy_car.height#Enemy height

                self.enemy_car_startx = random.randrange(240+25, 500,100)#Randomly select enemy car starting x from a list of three elements
                self.enemy_car_speed = random.choice([3,5,7,10])#Set the speed of the enemy car
                self.enemy_car_starty = 0 - self.enemy_car_height#Make a new enemy car y position



            self.car(self.car_x_coordinate, self.car_y_coordinate)#Display the player car
            self.highscore(self.HiScore,'High Score',580,0)#Display the high score
            self.highscore(self.count)#Display the current score of the player


            #If enemy car hits the player car
            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True#Make crash variable true
                    if self.count>self.HiScore:#Check if current score is higher than high score
                        self.HiScore=self.count#Set current score as new high score
                        self.fileWrite()#Write updated high score to file
                    self.display_message("Game Over!")#Display game over message message

            #If player car goes off course
            if self.car_x_coordinate < 240-15 or self.car_x_coordinate > 540-30:
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
    def run_enemy_car(self,img, thingx, thingy):
        self.gameDisplay.blit(img, (thingx, thingy))#Player car will blit or display at specified coordinates

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
        fil.write(str(self.HiScore))#Write high score after converting to string in the text file
        fil.close()#Close text file

#Main run
if __name__ == '__main__':
    car_racing = CarRacing()#creating game
    car_racing.racing_window()#running it
