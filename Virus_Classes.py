import pygame, random, time
from pygame.locals import *
from pygame import mixer

#Creates sprite for the enemy / virus
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x , y):
        super().__init__()
        self.imageList = ["img/virus.png" , "img/virus1.png"] #gets the image the to be used as the enemy sprites
        self.currentImagePosition = 0
        self.currentImage = pygame.image.load(self.imageList[self.currentImagePosition])
        self.surf = pygame.Surface((40,40))
        self.x = x
        self.y = y 
        self.rect = self.surf.get_rect(center = (self.x ,self.y))
        self.direction = "left"
        self.imageReset = 0

    #Move function for the movement of the enemy
    def move(self, destroyed, playerScore, speed):
        if self.direction == "left":
            self.rect.move_ip(-speed, 0)
        if self.direction == "right":
            self.rect.move_ip(speed, 0)
    
    #To tell that it moves left
    def left(self):
        self.rect.top += 32
        self.direction = "left"

    #To tell that it moves right
    def right(self):
        self.rect.top += 32
        self.direction = "right"

    #resets the images when you lose the game
    def reset(self):
        self.rect = self.surf.get_rect(center = (self.x, self.y))

    #Continuouly draws the sprites onto the window every 60 FPS
    def draw(self, window):

        if self.imageReset == 60 and self.currentImagePosition == 1:
            self.currentImagePosition = 0
            self.imageReset = 0

        if self.imageReset == 60 and self.currentImagePosition == 0:
            self.currentImagePosition = 1
            self.imageReset = 0

        self.imageReset +=1
        self.currentImage = pygame.image.load(self.imageList[self.currentImagePosition])
        window.blit(self.currentImage, self.rect)

#Was supposed to be a boss class that gives more points when killed most function are the 
#same as the enemy class
class Boss(pygame.sprite.Sprite):
    def __init__(self, x , y):
        super().__init__()
        self.imageList = ["img/boss.png"]
        self.currentImagePosition = 0
        self.currentImage = pygame.image.load(self.imageList[self.currentImagePosition])
        self.surf = pygame.Surface((40,40))
        self.x = x
        self.y = y 
        self.rect = self.surf.get_rect(center = (self.x ,self.y))
        self.direction = "left"
        self.imageReset = 0

    def move(self, destroyed, playerScore, speed):
        if self.direction == "left":
            self.rect.move_ip(-speed, 0)
        if self.direction == "right":
            self.rect.move_ip(speed, 0)
    
    def left(self):
        self.rect.top += 32
        self.direction = "left"

    def right(self):
        self.rect.top += 32
        self.direction = "right"

    def reset(self):
        self.rect = self.surf.get_rect(center = (self.x, self.y))

    def draw(self, window):

        if self.imageReset == 60 and self.currentImagePosition == 0:
            self.currentImagePosition = 0
            self.imageReset = 0

        self.imageReset +=1
        self.currentImage = pygame.image.load(self.imageList[self.currentImagePosition])
        window.blit(self.currentImage, self.rect)

'''Lets spawns the enemies and it also controls how far apart they art and make sure the enemy
"fall off" the screen'''
class EnemySpawner(pygame.sprite.Sprite):
    virusList = []
    def __init__(self):
        self.edgeBuffer = 50 
        self.virusBuffer = 20 
        self.virusWidth = 32 

        for i in range (self.edgeBuffer, 500, self.virusWidth + self.virusBuffer):
            for j in range (self.edgeBuffer, 300, self.virusWidth + 32):
                self.virusList.append(Enemy(i,j))

#The doctor id the player that character plays as and this class makes the sprite for it
class Doctor(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight):
        super().__init__()
        self.image = pygame.image.load("img/doctor.png")
        self.surf = pygame.Surface((32, 32))
        self.rect = self.surf.get_rect(midbottom = (screenWidth / 2.0, screenHeight))

    def move(self, screenWidth, screenHeight):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < screenWidth:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, window):
        window.blit(self.image, self.rect)

#Makes the syringe to fight off the enemies
class Syringe(pygame.sprite.Sprite):
    def __init__(self, doctor):
        super().__init__()
        self.image = pygame.image.load("img/syringe.png")
        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(center = (doctor.rect.midtop))
        self.fired = False

    def move(self):
        self.rect.move_ip(0, -5)

    def draw(self, window):
        window.blit(self.image, self.rect)

#creates the background of the game
class Background():
    def __init__(self, DISPLAYSURFACE):
        self.backgroundImage = pygame.image.load("img/bgIMG.jpeg")
        self.rectBGImage = self.backgroundImage.get_rect()
        self.moveSpeed = 0.5
        self.x1 = 0
        self.y1 = 0
        self.x2 = -(self.rectBGImage.width + self.moveSpeed)
        self.y2 = 0

    #updates the speed of the background as it moves
    def update(self):
        self.x1 += self.moveSpeed
        self.x2 += self.moveSpeed

        if self.x1 >= self.rectBGImage.width:
            self.x1 = -(self.rectBGImage.width + self.moveSpeed)

        if self.x2 >= self.rectBGImage.width:
            self.x2 = -(self.rectBGImage.width + self.moveSpeed)

    #renders the image of the background
    def render(self, DISPLAYSURFACE):
        DISPLAYSURFACE.blit(self.backgroundImage,(self.x1 , self.y1))
        DISPLAYSURFACE.blit(self.backgroundImage,(self.x2, self.y2))
