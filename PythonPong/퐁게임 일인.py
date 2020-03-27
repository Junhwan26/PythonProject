import pygame
import random
from pygame.locals import *


class Pong(object):
    def __init__(self, screensize):

        self.screensize = screensize
        self.centerx = int(screensize[0]*0.5)
        self.centery = random.randrange(0,screensize[1]) 
        self.radius = 8

        self.rect = pygame.Rect(self.centerx-self.radius,
                                self.centery-self.radius,
                                self.radius*2, self.radius*2)

        self.color = (100,100,255)

        self.direction = [-1,-1]

        self.speedx = 3
        self.speedy = 4
        #CODE TASK: change speed/radius as game progresses to make it harder
        #CODE BONUS: adjust ratio of x and y speeds to make it harder as game progresses

        self.hit_edge_left = False
        self.hit_edge_right = False

    def update(self, player_paddle2, player_paddle1):

        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy

        self.rect.center = (self.centerx, self.centery)

        if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1]-2:
            self.direction[1] = -1

        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True

        #CODE TASK: Change the direction of the pong, based on where it hits the paddles (HINT: check the center points of each)

        if self.rect.colliderect(player_paddle2.rect):
            #print("반사")
            self.direction[0] = 1
            self.speedx+=abs(player_paddle2.centery-self.centery)/30

        if self.rect.colliderect(player_paddle1.rect):
            #print("반사")
            self.direction[0] = -1
            self.speedx+=abs(player_paddle1.centery-self.centery)/30

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
        pygame.draw.circle(screen, (0,0,0), self.rect.center, self.radius, 1)

pygame.font.init()
comic = pygame.font.SysFont('Comic Sans MS', 30)

def drawscore(screen):
    score = comic.render(str(p1score) + " - " + str(p2score), False, BLACK)
    screen.blit(score, (300,30))

class PlayerPaddle1(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.centerx = 5
        self.centery = int(screensize[1]*0.5)
        self.height = 100
        self.width = 10
        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)
        self.color = (255,100,100)
        #CODE TASK: 어렵게 할라면 패들 사이즈를 바꿔라
        self.speed = 6
        self.direction = 0
    def update(self):
        self.centery += self.direction*self.speed
        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)

class PlayerPaddle2(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.centerx = screensize[0]-5
        self.centery = int(screensize[1]*0.5)
        self.height = 100
        self.width = 10
        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)
        self.color = (100,255,100)
        #CODE TASK: Adjust size of Player paddle as match progresses to make it more difficult
        self.speed = 6
        self.direction = 0

    def update(self):
        self.centery += self.direction*self.speed
        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)

BLACK = (0,0,0)
p1score = 0
p2score = 0

def main():
    pygame.init()
    global p1score
    global p2score

    #아래 플레이어 번호 지정 하고 패들 정해주는거
    clock = pygame.time.Clock()
    pong = Pong(screensize)
    my_paddle = PlayerPaddle1(screensize)
    your_paddle = PlayerPaddle2(screensize)

    running = True
    drawscore(screen)


    #recv 해서 문자열 확인하고 your_paddle direction 해줘야댐
    while running:
        #fps limiting/reporting phase
        clock.tick(64)
        #event handling phase`

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    my_paddle.direction = -1
                elif event.key == K_DOWN:
                    my_paddle.direction = 1

            if event.type == KEYUP:
                if event.key == K_UP and my_paddle.direction == -1:
                    my_paddle.direction = 0
                elif event.key == K_DOWN and my_paddle.direction == 1:
                    my_paddle.direction = 0
            
            if event.type == KEYDOWN:
                if event.key == K_w:
                    your_paddle.direction = -1
                elif event.key == K_s:
                    your_paddle.direction = 1

            if event.type == KEYUP:
                if event.key == K_w and your_paddle.direction == -1 :
                    your_paddle.direction = 0
                if event.key == K_s and your_paddle.direction == 1 :
                    your_paddle.direction = 0

        #object updating phase
        my_paddle.update()
        your_paddle.update()
        pong.update(my_paddle, your_paddle)

        #CODE TASK: make some text on the screen over everything else saying you lost/won, and then exit on keypress
        #CODE BONUS: allow restarting of the game (hint: you can recreate the Pong/Paddle objects the same way we made them initially)
        
        if pong.hit_edge_left:
            print ('Player 2 Win')
            p2score+=1
            if p2score==10:
                player2_won()
            pong = Pong(screensize)
            player_paddle1 = PlayerPaddle1(screensize)
            player_paddle2 = PlayerPaddle2(screensize)

        elif pong.hit_edge_right:
            print ('Player 1 Win')
            p1score+=1
            if p1score==10:
                player1_won()
            pong = Pong(screensize)
            player_paddle1 = PlayerPaddle1(screensize)
            player_paddle2 = PlayerPaddle2(screensize)            

        #rendering phase
        screen.fill((255,255,255))

        my_paddle.render(screen)
        your_paddle.render(screen)
        pong.render(screen)
        drawscore(screen)
        pygame.display.flip()

    pygame.quit()



def player1_won():
    print("1")
def player2_won():
    print("2")

screensize = (640,480)
screen = pygame.display.set_mode(screensize)


main()

