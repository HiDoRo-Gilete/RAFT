import sys,os
sys.path.insert(0,"./RAFT")
import node
import math,json
import pygame

PAUSE = 1
RESUME = 2
GREEN = (140, 193, 78)
BLACK =(0,0,0)
RED = (204, 63, 53)

class MININET():
    def __init__(self,num):
        self.num = num
        self.t_update=0
        data={
            "num": num,
            "listen_ports":{}
        }
        self.currentLeader =[]
        for i in range(1,num+1):
            data['listen_ports']['node'+str(i)]=[]
            for j in range(1,num+1):
                data['listen_ports']['node'+str(i)].append("localhost:50"+str(j)+str(i))
        with open('mininet.json','w') as file:
            file.write(json.dumps(data,indent=4))
        self.disconnect=[]
        self.Nodes=[]
        self.createNode()
        arr=os.listdir('./commitLog')
        for f in arr: os.remove('./commitLog/'+f)
        
    
    def createNode(self):
        PI=3.14159
        degree = 2*PI/self.num
        width=1280
        height =720
        
        self.Nodes= [node.NODE(self.generatePort(i+1),i+1,(width/2+200*math.cos(i*degree+PI/2)+200,
                        height/2-200*math.sin(i*degree+PI/2)),'mininet.json') for i in range(0,int(self.num))]        
        #self.Nodes[2].role="Leader"

    def draw(self,screen):
        self.t_update+=1
        for node in self.Nodes:
            node.display(screen)
        for i in range(self.num-1):
            for j in range(i+1,self.num):
                color = GREEN
                #print([self.Nodes[i].pos,self.Nodes[j].pos],self.disconnect)
                if [self.Nodes[i].pos,self.Nodes[j].pos] in self.disconnect: 
                    color = RED
                pygame.draw.line(screen,color,self.Nodes[i].pos,self.Nodes[j].pos,2)
        if self.t_update == 180:
            self.currentLeader =[]
            self.t_update = 0
            for i in range(self.num):
                if self.Nodes[i].role == "Leader":
                    id = self.Nodes[i].id
                    self.currentLeader.append({'id':id,'address':'localhost:50'+str(id)+str(id)})
            with open('mininet.json', 'r+') as file:
                file_data = json.load(file)
                file_data['leader_information']=self.currentLeader
                file.seek(0)
                json.dump(file_data, file, indent=4)
                file.truncate()
    def checkHoverLine(self):
        x,y =pygame.mouse.get_pos()
        for i in range(self.num-1):
            for j in range(i+1,self.num):
                x0,y0 =self.Nodes[i].pos
                x1,y1=self.Nodes[j].pos
                b,a = x1-x0,y0-y1
                c=-y0*b-x0*a
                if abs(a*x+b*y+c)/math.sqrt(a*a+b*b) <=3:
                    if [(x0,y0),(x1,y1)] in self.disconnect:
                        self.disconnect.remove([(x0,y0),(x1,y1)])
                        self.Nodes[i].reconnect(str(j+1))
                        self.Nodes[j].reconnect(str(i+1))
                    else:
                        self.disconnect.append([(x0,y0),(x1,y1)])
                        self.Nodes[i].disconnect(str(j+1))
                        self.Nodes[j].disconnect(str(i+1))
                    return
                    
    def killProcess(self):
        for i in range(self.num):
            self.Nodes[i].stop()
            self.Nodes[i].waitForKillAllThread()
            with open('mininet.json','w') as file:
                file.write("")

    def changeStateNode(self,i):
        if self.Nodes[i].status==RESUME:
            self.Nodes[i].stop()
        else:
            self.Nodes[i].start()
    def generatePort(self,i):
        port = {}
        for j in range(1,self.num+1):
            port[str(j)]={'port':"localhost:50"+str(j)+str(i),'isstop':False}
        return port
