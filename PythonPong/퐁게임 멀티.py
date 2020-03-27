import pygame
from pygame.locals import *
import socket
import threading
from time import sleep

screensize = (640,480)

HOST = '192.168.137.1'
PORT = 5555
player = 1
other =0
BLACK = (0,0,0)
p1score = 0
p2score = 0


class Pong(object):
    def __init__(self, screensize):

        self.screensize = screensize
        self.centerx = int(screensize[0]*0.5)
        self.centery = int(screensize[1]*0.5)
        self.radius = 8

        self.rect = pygame.Rect(self.centerx-self.radius,self.centery-self.radius,self.radius*2, self.radius*2)

        self.color = (100,100,255)

        self.direction = [1,1]

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
            self.direction[0] = 1
            self.speedx+=abs(player_paddle2.centery-self.centery)/30

        if self.rect.colliderect(player_paddle1.rect):
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
    def hello(self):
        print("hello")

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
    def hello(self):
        print("hello")

flag = 0
list=[PlayerPaddle1(screensize),PlayerPaddle2(screensize)]

def main():
    print("메인 시작")
    print("화면열림")
    pygame.init()
    global p1score
    global p2score
    global other
    global player
    global flag

    playerNumber=str(player)
    #아래 플레이어 번호 지정 하고 패들 정해주는거
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screensize)


    pong = Pong(screensize)
    list[0] = PlayerPaddle1(screensize)
    list[1] = PlayerPaddle2(screensize)
    running = True
    drawscore(screen)

    t=threading.Thread(target=move)
    t.start()
    #recv 해서 문자열 확인하고 your_paddle direction 해줘야댐
    
    
    
    while running:
        #fps limiting/reporting phase
        clock.tick(64)
        #event handling phase`
         
        for event in pygame.event.get():
           
            #print(player,"의 이벤트가 들어왔습니다.")
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    #my_paddle.direction = -1
                    client.send((playerNumber+"DU").encode())
                    print("DU보냄")
                elif event.key == K_DOWN:
                    client.send((playerNumber+"DD").encode())
                    print("DD보냄")
                    #my_paddle.direction = 1
                elif event.key == K_r:
                    client.send("restart".encode())

            if event.type == KEYUP:
                if event.key == K_UP and list[player].direction == -1:
                    #my_paddle.direction = 0
                    client.send((playerNumber+"UU").encode())
                    print("UU보냄")
                elif event.key == K_DOWN and list[player].direction == 1:
                    #my_paddle.direction = 0
                    client.send((playerNumber+"UD").encode())
                    print("UD보냄")


        #object updating phase
        list[0].update()
        list[1].update()
        pong.update(list[0], list[1])

        #CODE TASK: make some text on the screen over everything else saying you lost/won, and then exit on keypress
        #CODE BONUS: allow restarting of the game (hint: you can recreate the Pong/Paddle objects the same way we made them initially)
        
        #TODO : 이거 다시 초기화 할때 몇번 플레이언지 확인하고 패들 해줘야댐
        if pong.hit_edge_left:
            print ('Player 2 Win')
            p2score+=1
            #if p2score==10:
            #    player2_won()
            pong = Pong(screensize)
            list[0]=PlayerPaddle1(screensize)
            list[1]=PlayerPaddle2(screensize)

        elif pong.hit_edge_right:
            print ('Player 1 Win')
            p1score+=1
            #if p1score==10:
            #    player1_won()
            pong = Pong(screensize)
            list[0]=PlayerPaddle1(screensize)
            list[1]=PlayerPaddle2(screensize)

        if flag == 1:
            list[0]=PlayerPaddle1(screensize)
            list[1]=PlayerPaddle2(screensize)
            pong = Pong(screensize)
            p1score=0
            p2score=0
            flag = 0

        #rendering phase
        screen.fill((255,255,255))

        list[0].render(screen)
        list[1].render(screen)
        pong.render(screen)
        drawscore(screen)
        pygame.display.flip()

    pygame.quit()

def move():
    global flag
    print("you are",player)
    while 1:
        key=client.recv(1024).decode()
        print(key)
        print("와일이 돌고 있습니다.")
        if key=="restart":
            flag = 1
        if key[0]=="0":
            if key == "0DU":
                list[0].direction = -1
            if key == "0DD":
                list[0].direction = 1
            if key == "0UU":
                list[0].direction = 0
            if key == "0UD":
                list[0].direction = 0
        if key[0]=="1":
            if key == "1DU":
                list[1].direction = -1
            if key == "1DD":
               list[1].direction = 1
            if key == "1UU":
                list[1].direction = 0
            if key == "1UD":
                list[1].direction = 0            


        sleep(0.001)


def player1_won():
    print("Player 1 Won")
def player2_won():    
    print("Player 2 Won")

print("접속 전")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))
player=int(client.recv(1024).decode())
print("player =",player)

if player==1:
    other=0
elif player==0:
    other = 1
flag=client.recv(1024).decode()
print(flag)
if flag == "waiting":
    flag=client.recv(1024).decode()
if flag=="start":
    main()

