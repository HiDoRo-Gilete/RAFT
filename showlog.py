import time,os,json

maxlen = 20
def getstring(str):
    vailible = 20-len(str)
    capacityright = vailible//2
    right = " "*capacityright
    left = " " * (vailible-capacityright)
    return left+str+right 
def getAllLog(allNodes):
        arr2d = []
        for node in allNodes:
            try:
                f= open("./commitLog/"+node+".json",'r')
                data=json.load(f)['Log Commit']
                arr2d.append(data)
            except Exception as e:
                #print(e)
                arr2d.append([])
        maxlen = max(len(item) for item in arr2d)
        for i in range(maxlen):
                entry ="|"
                for j in range(len(allNodes)):
                    if len(arr2d[j])>i:
                        ite = arr2d[j][i]
                        entry+=getstring("("+str(ite["term"])+","+str(ite["number"])+")") +"|"
                    else: entry+=getstring("")+"|"
                print(entry)

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