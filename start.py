import pygame,json
import time
import numpy as np
import sys,random
sys.path.insert(0,"./RAFT")
import math,mininet

from pygame.locals import *

pygame.init()
width,height =1280,700
clock=pygame.time.Clock()
fps=60
pygame.display.set_caption("RAFT Alogisthm")
screen =pygame.display.set_mode((width,height))

#RAFT code===============
#function helper===
def distance(x,y,z,t):
    return math.sqrt((x-z)*(x-z)+(y-t)*(y-t))

#========================

Mininet = None

START = False
RESTART = True
btn1 = pygame.image.load("./images/btn1.png")
btn2 = pygame.image.load("./images/btn2.png")
number=0
WHITE =(230,242,255)
GREEN = (140, 193, 78)
BLACK =(0,0,0)
RED = (204, 63, 53)
h_root=0
def drawLogTable():
    data=None
    with open("commitLog.json") as file:
        if file.read() !="":
            file.seek(0)
            data =json.load(file)
    pygame.draw.rect(screen,(50,50,10),(20,170,Mininet.num*80,400),2)  
    if data!=None:
        nodeId=1
        for node in data:
            for i in range(len(data[node])):
                row = data[node][i]
                if i*30+h_root+40>=0:
                    screen.blit(pygame.font.SysFont("consolas",15).
                    render("("+str(row['term'])+","+str(row['number'])+")",True,GREEN),(23+(nodeId-1)*80,i*30+h_root+240))
            nodeId+=1

    pygame.draw.rect(screen,WHITE,(22,172,Mininet.num*80-4,63))
    for i in range(1,Mininet.num+1):
        if i!= Mininet.num: pygame.draw.line(screen,(50,50,10),(20+i*80,170),(20+i*80,570),2)
    for i in range(1,Mininet.num+1):
        screen.blit(pygame.font.SysFont("consolas",20).
            render("Node "+str(i),True,GREEN),(30+(i-1)*80,180))
        screen.blit(pygame.font.SysFont("consolas",15).
            render("Term,Mes",True,GREEN),(27+(i-1)*80,210))
    pygame.draw.line(screen,(50,50,10),(22,235),(18+Mininet.num*80,235),2)
        
        



while True:
    screen.fill(WHITE)
    screen.blit(btn1,(20,20))
    mousex,mousey = pygame.mouse.get_pos()
    if mousex >40 and mousex <240 and mousey >40 and mousey<100:
        screen.blit(btn2,(20,20))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            if Mininet !=None: Mininet.killProcess()
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button ==1:
            if mousex >40 and mousex <240 and mousey >40 and mousey<100:
                if not START and number>=3:
                    #if Mininet!=None: Mininet.killProcess()
                    Mininet = mininet.MININET(number)
                    START = True
                elif START: 
                    number,h_root=0,0
                    START = False
                    Mininet.killProcess()
            elif not START:
                for i in range (3,8):
                    x,y = 170+i*60,70
                    if distance(mousex,mousey,x,y) <=20:
                        number = i
            elif START:
                for i in range(0,number):
                    PI=3.14159
                    degree = 2*PI/number
                    if distance(mousex,mousey,width/2+200+200*math.cos(i*degree+PI/2),
                    height/2-200*math.sin(i*degree+PI/2)) <=20:
                        Mininet.changeStateNode(i)
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button ==5: #scroll mouse down
            h_root-=10
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button ==4: #scroll mouse up
            h_root+=10
                                

    if START:
        screen.blit(pygame.font.SysFont("consolas",20).
            render("RESTART",True,GREEN),(110,70))
        Mininet.draw(screen)
        #drawLogTable()
    else:
        screen.blit(pygame.font.SysFont("consolas",20).
            render("START",True,GREEN),(120,70))
        for i in range (3,8):
            x,y = 170+i*60,70
            if distance(mousex,mousey,x,y) <=20 or number == i: 
                pygame.draw.circle(screen,RED,(x,y),20)
            else: pygame.draw.circle(screen,GREEN,(x,y),20)
            screen.blit(pygame.font.SysFont("consolas",20).
                render(str(i),True,BLACK),(165+i*60,60))
    pygame.display.update()
    clock.tick(fps)