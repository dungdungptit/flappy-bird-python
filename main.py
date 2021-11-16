from numpy import true_divide
import pygame
import sys
import random
import math
from settings import*
from enemy import*

from pygame import font

# Setup
pygame.init()
screen = pygame.display.set_mode((width, heigth))
clock = pygame.time.Clock()

# images
background = pygame.image.load("images/bgg.png").convert_alpha()
bird = pygame.image.load("images/ping_bird (1).png").convert_alpha()
pipe = pygame.image.load("images/pipe.png").convert_alpha()
rotatedPipe = pygame.image.load("images/rotated_pipe.png").convert_alpha()
button = pygame.image.load("images\pixlr-bg-result.png").convert_alpha()

# sounds
point = pygame.mixer.Sound("sounds/sfx_point.wav")
hit = pygame.mixer.Sound("sounds/sfx_hit.wav")
shuriken_sound = pygame.mixer.Sound("sounds/shuriken.wav")
pygame.mixer.init(size=-16, channels=2)  # Initialize Sound Mixer
pygame.mixer.set_num_channels(16)  # Set channels to 16 from 8 to avoid sounds not playing
pygame.mixer.music.load('sounds/themesong.mp3')  # Load in theme song

class Game:
    def __init__(self):
        self.gameOn = True
        self.pause = False
        self.birdX = 100
        self.birdY = 100
        self.pipesX = [width, width+180, width+360, width+540, width+720, width+900, width+1080, width+1260]
        self.lowerPipeY = [self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe()]
        self.upperPipeY = [self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe()]
        self.gravity = 0
        self.pipeVel = 0
        self.flap = 0
        self.score = 0
        self.rotateAngle = 0
        self.isGameOver = False
        self.playSound = True

    # di chuyển ống
    def movingPipe(self):
        for i in range(0,8):
            self.pipesX[i] += -self.pipeVel
        
        for i in range(0,8):
            if(self.pipesX[i] < -50):
                self.pipesX[i] = width + 100
                self.lowerPipeY[i] = self.randomPipe()
                self.upperPipeY[i] = self.randomRotatedPipe()

    # sinh random vị trí đặt ống phía dưới
    def randomPipe(self):
        return random.randrange(int(heigth/2)+100, heigth-150)
    
    # sinh random vị trí đặt ống phía trên
    def randomRotatedPipe(self):
        return random.randrange(-int(heigth/2)+100, -100)

    # chuyển động của chú chim
    def flapping(self):
        self.birdY += self.gravity
        if(self.isGameOver == False):
            self.flap -= 1
            self.birdY -= self.flap
        if(self.birdY+bird.get_height() >= heigth):
            self.birdY = heigth - bird.get_height() - 10
    
    # xét va chạm với ống, naruto
    def isCollide(self, tmp):
        for i in range(0,8):
            # va chạm với ống mà naruto đang đứng trên đó
            if i == tmp: 
                if(self.birdX >= self.pipesX[i] and self.birdX <= (self.pipesX[i]+pipe.get_width())
                and (self.birdY+bird.get_height()-15+100) >= self.lowerPipeY[i]):
                    return True
                elif(self.birdX == self.pipesX[i] and (self.birdY <= self.lowerPipeY[i])):
                    if(self.isGameOver == False):
                        self.score += 1
                        pygame.mixer.Sound.play(point)
                continue
            
            
            # va chạm với các ống còn lại
            if(self.birdX >= self.pipesX[i] and self.birdX <= (self.pipesX[i]+pipe.get_width())
                and ((self.birdY+bird.get_height()-15) >= self.lowerPipeY[i] or 
                (self.birdY) <= self.upperPipeY[i]+rotatedPipe.get_height()-15)):
                    return True

            # tính điểm
            elif(self.birdX == self.pipesX[i] and (self.birdY <= self.lowerPipeY[i] and self.birdY >= self.upperPipeY[i])):
                if(self.isGameOver == False):
                    self.score += 1
                    pygame.mixer.Sound.play(point)
        
        if(self.birdY <= 0):
            return True
        
        elif(self.birdY+bird.get_height() >= heigth):
            self.gravity = 0
            return True

        return False

    # xét va chạm với phi tiêu
    def isCollide2(self, shuriken):
        distance = math.sqrt((self.birdX - shuriken.x)**2 + (self.birdY - shuriken.y)**2)
        if distance < 60:
            return True
        else:
            return False
    
    # gameover
    def gameOver(self, tmp, shuriken):
        if(self.isCollide(tmp) or self.isCollide2(shuriken)):
            self.isGameOver = True

            if(self.playSound):
                pygame.mixer.Sound.play(hit)
                self.playSound = False

            if(self.birdY+bird.get_height() >= heigth):
                self.birdY = heigth - bird.get_height() - 10
            
            self.pipeVel = 0
            self.flap = 0
            self.rotateAngle = -90
        
        if self.isGameOver == True:
            self.screenText("Game Over!", (255,255,255), 450, 300, 84, "Fixedsys", bold=True)
            self.screenText("Press Enter To Play Again", (255,255,255), 400, 600, 48, "Fixedsys", bold=True)
            pygame.mixer.Sound.stop(shuriken_sound)

    def screenText(self, text, color, x,y, size, style, bold=False):
        font = pygame.font.SysFont(style, size, bold=bold) # Create font object
        screen_text = font.render(text, True, color) # Create Text Label
        screen.blit(screen_text, (x,y))  # Draw Label To Screen

    def text_objects(self,text,font):
        textSurface= font.render(text,True,black)
        return textSurface,textSurface.get_rect() 

    # button onclick
    def button(self,msg,x,y,w,h,ic,ac,action=None):   
        mouse = pygame.mouse.get_pos()
        click =pygame.mouse.get_pressed()
        
        if x+w >mouse[0] >x and y+h >mouse[1]>y:
            if click[0]==1 and action !=None:
                action()

        smalltext=pygame.font.Font("freesansbold.ttf",25)
        TextSurf, TextRect = self.text_objects(msg, smalltext)
        TextRect.center = ((x+(w/2)),(y+(h/2)))
        screen.blit(TextSurf, TextRect)
    
    # pause game
    def unpause(self):
        self.pause=False

    def paused(self):
        while self.pause:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            screen.blit(background,(0,0))
            largeText = pygame.font.SysFont("comicsansms",115)
            TextSurf, TextRect = self.text_objects("Paused", largeText)
            TextRect.center = ((width/2),(heigth/2))
            screen.blit(TextSurf, TextRect)
            #gameDisplay.fill(white)
            screen.blit(button,(150,350))
            screen.blit(button,(800,350))

            self.button("Continue",190,460,220,70,low_red,red,self.unpause)
            self.button("Quit",840,460,220,70,low_green,green,quit)

            pygame.display.update()
            clock.tick(60)

    # Main start
    def start_menu(self):
        pygame.mixer.music.play(-1)  # Start playing theme song
        pygame.mixer.music.set_volume(.2)
        running = True
        while running:
            screen.blit(background, (0, 0))
            # self.screenText('Press Space To Begin','black',(width/2)-400,(heigth/2)-100,80,'comicsansms', bold=False)
            largeText = pygame.font.SysFont("comicsansms",75)
            TextSurf, TextRect = self.text_objects("Space or click to play game", largeText)
            TextRect.center = ((width/2),(heigth/2))
            screen.blit(TextSurf, TextRect)
            screen.blit(button,(150,350))
            screen.blit(button,(800,350))
            self.button("Play!",190,460,220,70,low_red,red,self.mainGame)
            self.button("Quit",840,460,220,70,low_green,green,quit)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # If space is pressed, start game
                        self.mainGame()  # Starts main_loop
                        pygame.mixer.music.stop()
                        self.death_screen()
                        running = False  # After main_loop (naruto loses), the game quits

    # Main loop
    def mainGame(self):
        tmp = random.randint(0, 8)
        naruto = Naruto(self.pipesX[tmp]-15, self.lowerPipeY[tmp]-85,100,100)
        shuriken = Shuriken(round(naruto.x + 60),round(naruto.y + 30),40,40,-1)
        pygame.mixer.Sound.play(shuriken_sound)
        # check va chạm vào naruto
        check = False
        while self.gameOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if(self.isGameOver == False):
                            self.pipeVel = 5
                            self.gravity = 10
                            self.flap = 20
                            self.rotateAngle = 15
                    
                    if event.key==pygame.K_p:
                        self.pause=True
                        self.paused()

                    if event.key == pygame.K_RETURN:
                        newGame = Game()
                        newGame.mainGame()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.rotateAngle = 0
	        
            # blitting images
            screen.blit(background, (0,0))
            
            # blit pipe and naruto, shuriken
            for i in range(0,8):
                if i == tmp:
                    naruto.x = self.pipesX[i]-15
                    naruto.y = self.lowerPipeY[i]-85
                    
                    
                    if self.isGameOver == False:
                        naruto.draw(screen)
                    shuriken.auto_throw()
                    if shuriken.x < 0:
                        if naruto.x > 100: 
                            pygame.mixer.Sound.play(shuriken_sound)
                        shuriken.x = round(naruto.x + 60)
                        shuriken.y = round(naruto.y + 30)
                     
                    if self.isGameOver == False:
                        shuriken.draw(screen)

                    
                    screen.blit(pipe, (self.pipesX[i], self.lowerPipeY[i]))
                    self.upperPipeY[i] = 0
                else:
                    # lower Pipe
                    screen.blit(pipe, (self.pipesX[i], self.lowerPipeY[i]))
                    # upper pipe
                    screen.blit(rotatedPipe, (self.pipesX[i], self.upperPipeY[i]))

            # vẽ chuyển động quay khi nhấn space 
            screen.blit(pygame.transform.rotozoom(bird, self.rotateAngle, 1), (self.birdX, self.birdY))

            if self.isCollide2(naruto):
                check = True

            if self.isGameOver == True:
                # va vào đầu naruto thì naruto sẽ nằm
                if check == True:
                    screen.blit(pygame.image.load('images/Nd.png'), (naruto.x, naruto.y))
                # còn lại thì sẽ đứng cười
                else:
                    screen.blit(pygame.image.load('images/Nstanding.png'), (naruto.x, naruto.y))
            
            # moving pipe
            self.movingPipe()
            
            # flapping
            self.flapping()
            # game over
            self.gameOver(tmp, shuriken)
            
            # displaying score
            self.screenText(str(self.score), (255,255,255), 600, 50, 68, "Fixedsys", bold=True)
            
            pygame.display.update()
            clock.tick(fps)

falppyBird = Game()
falppyBird.start_menu()