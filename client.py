import grpc,sys,random,json,time
sys.path.insert(0,"./RAFT")
import raft_pb2
import raft_pb2_grpc

num =0
while num != -1:
    logOk=False
    try:
        num = int(input("Input number to append to leader's entry(-1 to exit): "))
        logOk=True
    except:
        logOk=False
    if num!=-1 and logOk:
        portleader=None
        with open('mininet.json','r') as file:
            if file.read() != "":
                file.seek(0)
                data= json.load(file)
                if data != None and 'leader_addr' in data:
                    portleader=data['leader_addr']
            while portleader == None:
                print("Wait for leader!(press ctrl C to exit!)")
                if file.read() != "":
                    file.seek(0)
                    data= json.load(file)
                    if data != None and 'leader_addr' in data:
                        portleader=data['leader_addr']
                time.sleep(1)
        try:
             with grpc.insecure_channel(portleader) as channel:
                stub = raft_pb2_grpc.RAFTStub(channel)
                print("Connect to leader running at ",portleader)
                response = stub.AddEntry(raft_pb2.request_entry(number=num))
                print("message is sent and wait for commit")
        except Exception as e:
            print(e)