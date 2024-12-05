import grpc,sys,random,json,time
sys.path.insert(0,"./RAFT")
import raft_pb2
import raft_pb2_grpc
from threading import Thread
num =0
def sendLog(add):
    try:
        with grpc.insecure_channel(add) as channel:
            stub = raft_pb2_grpc.RAFTStub(channel)
            response = stub.AddEntry(raft_pb2.request_entry(number=num))
            print('.')
            time.sleep(0.2)
            print('.')
            time.sleep(0.2)
            print('.')
            print("Connect to leader running at ",add)
            print("message is sent and wait for commit")
    except Exception as e:
        #print('Leader at '+add+" is down!")
        pass
while num != -1:
    logOk=False
    try:
        num = int(input("Input number to append to leader's entry(-1 to exit): "))
        logOk=True
    except:
        logOk=False
    if num!=-1 and logOk:
        addr=[]
        with open('mininet.json','r') as file:
            if file.read() != "":
                file.seek(0)
                data= json.load(file)
                if data != None and 'leader_information' in data:
                    for item in data['leader_information']:
                        addr.append(item['address'])
            while addr == []:
                print("Wait for leader!(press ctrl C to exit!)")
                if file.read() != "":
                    file.seek(0)
                    data= json.load(file)
                    if data != None and 'leader_information' in data:
                        for item in data['leader_information']:
                            addr.append(item['address'])
                time.sleep(2)
        for add in addr:
            thr = Thread(target=sendLog,args=(add,))
            thr.start()
            time.sleep(0.5)
            

            