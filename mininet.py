import sys
sys.path.insert(0,"./RAFT")
import node
import math,json

PAUSE = 1
RESUME = 2

class MININET():
    def __init__(self,num):
        self.num = num
        data={
            "num": num,
            "ports":["localhost:"+str(50000+i) for i in range(1,num+1)]
        }
        with open('mininet.json','w') as file:
            file.write(json.dumps(data,indent=4))
        self.Nodes=[]
        self.createNode()
        with open('commitLog.json','w') as file:
            file.write("")
        
    
    def createNode(self):
        PI=3.14159
        degree = 2*PI/self.num
        width=1280
        height =720
        self.Nodes= [node.NODE('localhost:'+str(50000+i+1),i+1,(width/2+200*math.cos(i*degree+PI/2)+200,
                        height/2-200*math.sin(i*degree+PI/2)),'mininet.json') for i in range(0,int(self.num))]        
        #self.Nodes[2].role="Leader"

    def draw(self,screen):
        for node in self.Nodes:
            node.display(screen)
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
