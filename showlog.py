import time,os,json

maxlen = 20
def getstring(str):
    vailible = 20-len(str)
    capacityright = vailible//2
    right = " "*capacityright
    left = " " * (vailible-capacityright)
    return left+str+right 
def getAllLog(allNodes):
    with open("commitLog.json") as file:
        try:
            data=json.load(file)
            print()
            for item in allNodes:
                if item not in data:
                    data[item] =[]
            maxlen=max(len(data[item]) for item in allNodes)
            for i in range(maxlen):
                entry ="|"
                for item in allNodes:
                    if len(data[item])>i:
                        ite = data[item][i]
                        entry+=getstring("("+str(ite["term"])+","+str(ite["number"])+")") +"|"
                    else: entry+=getstring("")+"|"
                print(entry)

        except Exception as e:
            pass
            #print(e)
while True:
    try:
        print("To exit, press Ctrl C\n\n")
        with open("mininet.json")as fi:
            if fi.read() =="": print("Wait for mininet start!")
            else:
                fi.seek(0)
                allNodes = ["Node "+str(i) for i in range(1,json.load(fi)['num']+1)]
                top ="|"
                for item in allNodes:
                    top+=getstring(item)+"|"
                print(top) 
                getAllLog(allNodes)

        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        break