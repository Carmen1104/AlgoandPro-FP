import pygame, random, time
from pygame.locals import *
from pygame import mixer
from Virus_Classes import Enemy
from Virus_Classes import EnemySpawner
from Virus_Classes import Doctor
from Virus_Classes import Syringe
from Virus_Classes import Background

def main():
    pygame.init()
    FPS = 60
    clock = pygame.time.Clock()
    speed = 1
    score = 0
    wait = 0
    imageReset = 0

    #colors
    red = (255, 0 ,0)
    black = (0, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)
    

    #font
    font = pygame.font.SysFont("Verdana", 60)
    smallfont = pygame.font.SysFont("Verdana", 20)
    gameOverFont = smallfont.render("Game over", True , black)

    #window
    screenWidth = 500
    screenHeight = 600

    backgroundImage = pygame.image.load("img/bgImage.png")
    DISPLAYSURFACE = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Attack on Virus!!")

    INCREASE_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INCREASE_SPEED, 3000)

    #music
    mixer.init()
    mixer.music.load("audio.mp3")
    mixer.music.set_volume = 0.8
    mixer.music.play()

    #start game
    background = Background(DISPLAYSURFACE)
    doctor = Doctor(screenWidth, screenHeight)
    syringeList = []
    EnemySpawner()
    enemyGroup = pygame.sprite.Group()
    
    for i in EnemySpawner.virusList:
        enemyGroup.add(i)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                
            if event.type == INCREASE_SPEED:
                speed += 0.1

        background.update()  
        background.render(DISPLAYSURFACE)

    #to check on the doctor
        doctor.draw(DISPLAYSURFACE)
        doctor.move(screenWidth, screenHeight)

    #score
        scoreText = smallfont.render("Score: " + str(score), True, white)
        DISPLAYSURFACE.blit(scoreText, (0,0))

    #enemy
        if len(enemyGroup) == 0:
            EnemySpawner.virusList = []
            EnemySpawner()
            enemyGroup = pygame.sprite.Group()
            for i in EnemySpawner.virusList:
                enemyGroup.add(i)
            
        #syringe 
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys [K_SPACE] and wait > 25:
            syringeList.append(Syringe(doctor))
            wait = 0
                
        for i in syringeList:
            if i.rect.top < 2:
                syringeList.remove(i)
            i.move()
            i.draw(DISPLAYSURFACE)

        for enemy in enemyGroup:
                
            enemy.move(False, 0, speed)
            enemy.draw(DISPLAYSURFACE)

            if enemy.rect.left < 0:
                enemy.right()
            if enemy.rect.right > 500:
                enemy.left()
            if enemy.rect.bottom > 600:
                DISPLAYSURFACE.fill(green)
                DISPLAYSURFACE.blit(gameOverFont, (200,250))
                DISPLAYSURFACE.blit(scoreText, (215,300))
                pygame.display.update()
                time.sleep(4)
                EnemySpawner.virusList = []
                EnemySpawner()
                enemyGroup = pygame.sprite.Group()
                    
                for i in EnemySpawner.virusList:
                    enemyGroup.add(i)
                for resetEnemy in enemyGroup:
                    resetEnemy.reset()
                score = 0
                speed = 1
        
            for syringe in syringeList:
                if pygame.sprite.spritecollide(enemy, syringeList, False):
                    enemy.kill()
                    syringeList.remove(syringe)
                    score = score + 10
                        
        pygame.display.update()
        imageReset +=1
        wait += 1
        clock.tick(FPS)

#Test (Run Code)
main()
