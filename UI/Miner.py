import services.MinerService as mnr
import services.LogInService as lgn
import services.UserService as usr
import socket
import threading


def startClient(packet):
    freeMiners = usr.checkOnlineMiners()
    miners = []
    for i in freeMiners:
        miners.append([i[1],i[2]])
    skt = socket.socket()
    for j in miners:
        skt.connect((j[0],j[1]))
        skt.send(packet)
    skt.close()

def sendChain(packet):
    freeMiners = usr.checkOnlineMiners()
    miners = []
    for i in freeMiners:
        miners.append([i[1],i[2]])
    skt = socket.socket()
    for j in miners:
        skt.connect((j[0],j[1]))
        skt.send(packet)
    skt.close()

def sendResponse(packet):
    host = packet[1]
    port = packet[2]
    skt = socket.socket()
    skt.connect((host,port))
    skt.send(packet)
    skt.close()

def minerScreen(userId):
    mnr.checkHost(userId)
    mnr.makeOnline(userId)
    info = mnr.getMinerInfo()
    skt = socket.socket()
    skt.bind((info[0],info[1]))
    skt.listen(5)
    print("x"*20)
    print("server started and listened ...")
    print("x"*20)
    while(True):
        c,addr = skt.accept()
        result = c.recv(1024)
        if result == None:
            print("x" * 20)
            print("Network Listening .....")
            ext = int(input("press 0 to exit..."))
            print("x" * 20)
            if ext == 0:
                mnr.makeOffline(userId)
                break
        else:
            if result[0] == "TRN":
                threadRace = threading.Thread(target=mnr.startRace)
                threadRace.start()
                rsl = mnr.startRace()
                if rsl[0] == True:
                    winPacket = mnr.winPacketCreator(rsl[1])
                    threadClient = threading.Thread(target=startClient, args=(winPacket,))
                    threadClient.start()

                    mnr.addBlockchain(result[1])
                    blk = mnr.findLastBlock()
                    threadChain = threading.Thread(target=sendChain, args=(blk,))
                    threadChain.start()


            else:
                rslt = mnr.packetSeparator(result)
                if rsl !=  None:
                    threadSend = threading.Thread(target=sendResponse, args=(rslt,))
                    threadSend.start()

def minerEnter():
    while(True):
        print("x" * 20)
        userId = input("Enter User Id : ")
        password = input("Enter Password : ")
        x = lgn.minerLogIn(userId, password)
        if x == True:
            minerScreen(userId)
        else:
            print("x"*10)
            print(">>Wrong Username or Password>>")
