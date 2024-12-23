import pygame
import time
import numpy as np
import grpc,sys,random
sys.path.insert(0,"./RAFT")
import raft_pb2
import raft_pb2_grpc
from concurrent import futures
from threading import Thread
import math,json

REQUESTVOTE = 100
REPLYVOTE=200
REQUESTREPLICATE=300
REPLYREPLICATE=400
WAITFORLEADER = 500
WAITFORREPLYVOTE =600
WAITFORREPLYREPLICATE=700

RED = (204, 63, 53)
GREEN = (140, 193, 78)
BLACK =(0,0,0)
PAUSE = 1
RESUME = 2

class Log:
    def __init__(self,term,mes):
        self.term = term
        self.mes = mes
class mininetInfor:
    def __init__(self,fileconfig,id):
        with open(fileconfig,'r') as file:
            data =json.load(file)
        self.num=int(data['num'])
        self.getID={}
        for i in range(1,self.num+1): 
            self.getID[str(i)]={"port":"localhost:50"+str(id)+str(i),
                              "ack":0,"sentLength":0}
        self.fileconfig = fileconfig
    def updateCurrentLeader(self,leaderInfo):
        with open(self.fileconfig, 'r+') as file:
            file_data = json.load(file)
            file_data['leader_information']=leaderInfo
            file.seek(0)
            json.dump(file_data, file, indent=4)
            file.truncate()
    def updateCommitLog(self,description,logmessage):
        try:
            file = open('./commitLog/'+description+".json","w")
            file_data={}
            entry =[]
            for log in logmessage:
                entry.append({"term":log.term,"number":log.mes})
            file_data['Log Commit'] = entry
            json.dump(file_data, file, indent=4)
        except Exception as e:
            print('-----',e,'------')

class NODE(raft_pb2_grpc.RAFT):
    def __init__(self,port,id,pos,file):
        #backend
        self.mininet = mininetInfor(file,id)
        self.timeout=0
        self.comitLength=0
        self.getTimeout()
        self.currentTerm =0
        self.thread = None
        self.ports = port
        self.role ="Folower"
        self.voteFor=None
        self.currentLeader=None
        self.voteReceive=[]
        self.id=id
        self.log=[]
        self.lastTerm=0
        self.routine=360
        self.allthreads =[]
        #frontend
        self.thr_runserver()
        self.status= RESUME
        self.pos = pos
        #var to draw line between 2 point
        self.timedrawline=None

    def thr_runserver(self):
        for p in self.ports:
            thr= Thread(target=self.runserver,args=(p))
            thr.start()
            self.allthreads.append(thr)
    def runserver(self,pId):
        server=grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        raft_pb2_grpc.add_RAFTServicer_to_server(self,server)
        #print("Node "+str(self.id)+" at "+self.port)
        server.add_insecure_port(self.ports[pId]['port'])
        server.start()
        while not self.ports[pId]['isstop']:
            time.sleep(0.1)
        server.stop(None)

    def initTimedrawline(self):
        self.timedrawline=[0 for i in range(self.mininet.num)]
        #print(self.timedrawline)
    #override service===========================================================================
    def RequestVote(self, request, context):  #service 1
        if request.currentTerm >self.currentTerm:
            self.currentTerm=request.currentTerm
            self.role="Follower"
            self.voteFor=None
        
        self.lastTerm=0
        if len(self.log) >0: self.lastTerm=self.log[len(self.log)-1].term
        logOK = (request.lastTerm>self.lastTerm) or (request.lastTerm==self.lastTerm and request.logLength>=len(self.log))
        if self.currentTerm == request.currentTerm and logOK and (self.voteFor ==request.nodeId or self.voteFor == None):
            self.voteFor=request.nodeId
            return raft_pb2.reply_vote_mesage(nodeId=self.id,currentTerm=self.currentTerm,isVote=True,replyType=REPLYVOTE)
        else:
            return raft_pb2.reply_vote_mesage(nodeId=self.id,currentTerm=self.currentTerm,isVote=False,replyType=REPLYVOTE)


    def ReplicateLog(self, request, context): #service 2
        if request.currentTerm > self.currentTerm:
            self.currentTerm=request.currentTerm
            self.voteFor=None
            #cancel election timer
        if request.currentTerm == self.currentTerm:
            self.role = "Follower"
            self.currentLeader=request.leaderId
            self.getTimeout()
        logOk = len(self.log)>=request.prefixLength and (request.prefixLength == 0 
                                or self.log[request.prefixLength-1].term == request.prefixTerm)
        if request.currentTerm==self.currentTerm and logOk:
            self.AppendEntries(request.prefixLength,request.commitLength,request.suffix)
            Ack= request.prefixLength+ len(request.suffix)
            return raft_pb2.reply_replicate_massage(nodeId=self.id,currentTerm=self.currentTerm,ack=Ack,
                                                    result=True,replyType=REPLYVOTE)
        else: return raft_pb2.reply_replicate_massage(nodeId=self.id,currentTerm=self.currentTerm,ack=0,
                                                    result=False,replyType=REPLYVOTE)
    def AppendEntries(self,prefixLen,leaderCommit,suffix): 
        if len(suffix) > 0 and len(self.log) >prefixLen:
            index= min(len(self.log),prefixLen+len(suffix))-1
            if self.log[index].term != suffix[index-prefixLen].term:
                self.log=[]
                for i in range(prefixLen):
                    self.log=[Log(self.log[i].term,self.log[i].mes)]
        if prefixLen+len(suffix)>len(self.log):
            for i in range(len(self.log)-prefixLen,len(suffix)):
                self.log.append(Log(suffix[i].term,suffix[i].mes))
        if leaderCommit >self.comitLength:
            for i in range(self.comitLength,leaderCommit):
                print("Node "+str(self.id)+" commit entry (term: "+str(self.log[i].term)+" mes: "+str(self.log[i].mes)+")")
            self.comitLength=leaderCommit
            self.mininet.updateCommitLog("Node "+str(self.id),self.log[0:leaderCommit])
    def AddEntry(self, request, context): #service 3
        self.log.append(Log(self.currentTerm,request.number))
        return raft_pb2.reply_entry(result=True)
    #======================================================================================
    def getTimeout(self):
        fps=60
        self.timeout=min(self.timeout+random.randint(6*fps,10*fps),15*fps-random.randint(0,2*fps))
    def start(self):
        for p in self.ports:
            self.ports[p]["isstop"] = False
        self.status=RESUME
        self.timeout=0
        if self.role!= "Leader": self.getTimeout()
        self.thr_runserver()
    def stop(self):
        for p in self.ports:
            self.ports[p]["isstop"] = True
        self.status=PAUSE
        print("Node "+str(self.id)+" has been stopped!")
    def drawline(self):
        if self.timedrawline == None: 
            self.initTimedrawline()
        v=4
        w = 10
    def requestVote(self):
        self.voteReceive =[]
        self.getTimeout()
        self.currentTerm +=1
        self.role="Candidate"
        self.voteFor=self.id
        self.voteReceive.append(self.id)
        self.lastTerm=0
        if len(self.log) >0: self.lastTerm = self.log[len(self.log)-1].term
        for node in self.mininet.getID:
            if str(self.id) != node:
                nod = self.mininet.getID[node]
                thr = Thread(target=self.sendRequestVote,args=(nod['port'],))
                thr.start()
                self.allthreads.append(thr)
    def sendRequestVote(self,port):
        try:
            with grpc.insecure_channel(port) as channel:
                stub = raft_pb2_grpc.RAFTStub(channel)
                response = stub.RequestVote(raft_pb2.request_vote_message(nodeId=self.id,currentTerm=self.currentTerm,
                                                logLength=len(self.log),lastTerm=self.lastTerm,requestType=REQUESTVOTE))
            
                print("Reply Vote from node "+str(response.nodeId)+" to Node "+str(self.id)+". Result: "+str(response.isVote))
                if self.role=="Candidate" and self.currentTerm == response.currentTerm and response.isVote:
                    self.voteReceive.append(response.nodeId)
                    if len(self.voteReceive) >= (self.mininet.num+1)/2:
                        self.role="Leader"
                        self.currentLeader=self.id
                        leaderInfo={}
                        #leaderInfo['id'],leaderInfo['address']=self.id,'localhost:50'+str(self.id)*2
                        #self.mininet.updateCurrentLeader(leaderInfo)
                        self.timeout=0
                        for node in self.mininet.getID:
                            if node != str(self.id):
                                nod = self.mininet.getID[node]
                                nod['sentLength']=len(self.log)
                                nod['ack'] = 0
                                self.replicateLog(node)
        except Exception as e:
            #print(e)
            print("no reply from port "+port+" for vote request")
    def replicateLog(self,folower):
        prefixLen=self.mininet.getID[folower]['sentLength']
        suffix=[]
        for i in range(prefixLen,len(self.log)):
            suffix.append(self.log[i])
        prefixTerm=0
        if prefixLen>0: prefixTerm = self.log[prefixLen-1].term
        thr = Thread(target=self.sendReplicateLog,args=(self.mininet.getID[folower]['port'],prefixLen,prefixTerm,suffix,))
        thr.start()
        self.allthreads.append(thr)
    def sendReplicateLog(self,port,preLen,preTerm,suff):
        try:
            with grpc.insecure_channel(port) as channel:
                stub = raft_pb2_grpc.RAFTStub(channel)
                message = raft_pb2.request_replicate_message()
                message.leaderId=self.id
                message.currentTerm=self.currentTerm
                message.prefixLength= preLen
                message.prefixTerm=preTerm
                message.commitLength=self.comitLength
                message.requestType=REQUESTREPLICATE
                for item in suff: 
                    message.suffix.add(term=item.term,mes=item.mes)
                response = stub.ReplicateLog(message)
            print("Reply Replicate from node "+str(response.nodeId)+" to Node "+str(self.id)+". Result: "+str(response.result))
            if response.currentTerm ==self.currentTerm and self.role == "Leader":
                if response.result and response.ack >= self.mininet.getID[str(response.nodeId)]['ack']:
                    self.mininet.getID[str(response.nodeId)]['ack'] = response.ack
                    self.mininet.getID[str(response.nodeId)]['sentLength'] = response.ack
                    #self.CommitLogEntries()
                elif self.mininet.getID[str(response.nodeId)]['sentLength'] >0:
                    self.mininet.getID[str(response.nodeId)]['sentLength'] -=1
                    #self.replicateLog(response.nodeId)
            elif response.currentTerm >self.currentTerm:
                self.currentTerm = response.currentTerm
                self.role="Follower"
                self.voteFor = None
                self.getTimeout()
        except Exception as e:
            #print(e)
            print("no reply from port "+port+" for replicate request")
            #cancel election timer
    def CommitLogEntries(self):
        while self.comitLength < len(self.log):
            acks = 0
            for nod in self.mininet.getID:
                acklen = self.mininet.getID[nod]['ack']
                if acklen>self.comitLength:
                    acks +=1
            if acks>=(self.mininet.num)//2:
                self.comitLength+=1
                print("Node "+str(self.id)+" (Leader) is commit entry (term: "+str(self.log[self.comitLength-1].term)
                      +" mes: "+str(self.log[self.comitLength-1].mes)+")")
                self.mininet.updateCommitLog("Node "+str(self.id),self.log)
            else:
                break
    def waitForKillAllThread(self):
        while(len(self.allthreads)!=0):
            for thr in self.allthreads:
                if not thr.is_alive():
                    self.allthreads.remove(thr)
    
    def disconnect(self,nodeId):
        self.mininet.getID.pop(nodeId)
        self.ports[nodeId]['isstop']=True
        time.sleep(0.15)
        self.ports.pop(nodeId)
        self.mininet.num-=1
    def reconnect(self,nodeId):
        self.mininet.getID[nodeId]={"port":"localhost:50"+str(self.id)+nodeId,
                              "ack":0,"sentLength":0}
        self.ports[nodeId]={'port':'localhost:50'+nodeId+str(self.id),'isstop':False}
        thr= Thread(target=self.runserver,args=(nodeId))
        thr.start()
        self.allthreads.append(thr)
        self.mininet.num+=1

    def display(self,screen):
        fps=60
        color = GREEN
        self.CommitLogEntries()

        if self.status != PAUSE:
            if self.timeout!=0: self.timeout-=1
            elif self.role !="Leader":  self.requestVote()
            else:
                if self.routine !=0: self.routine-=1
                else:
                    self.routine = 6*fps
                    for node in self.mininet.getID:
                        if node!= str(self.id):
                            self.replicateLog(node)
        else:
            color=RED
        pygame.draw.circle(screen,color,self.pos,20)
        screen.blit(pygame.font.SysFont("consolas",20).
            render(str(self.id),True,color),(self.pos[0]-5,self.pos[1]+30))
        if self.role == "Leader":
            screen.blit(pygame.font.SysFont("consolas",20).
            render("Leader",True,color),(self.pos[0]-30,self.pos[1]-50))
        elif self.status != PAUSE:
            pygame.draw.line(screen,BLACK,(self.pos[0]-35,self.pos[1]+60),(self.pos[0]+35,self.pos[1]+60),5)
            pygame.draw.line(screen,GREEN,(self.pos[0]-35,self.pos[1]+60),(self.pos[0]+35-70*self.timeout/(15*fps),self.pos[1]+60),5)
        self.drawline()
    