
import services.LogInService as lgn
import services.UserService as usr
import socket
import threading


userInfo = lgn.userConnectionObjects()

def startClient(packet):
    skt = socket.socket()
    miner = lgn.getLogInMiner()
    skt.connect((miner[0],int(miner[1])))
    skt.send(packet)
    skt.close()

def trasactionEnterScreen():
    print("x"*20)
    productId = input("Product Id : ")
    productName = input("Product Name : ")
    productNumber = input("Product Number : ")
    fromPlace = input("From Place : ")
    toPlace = input("To Place : ")
    date = input("Date : ")
    print("x" * 20)
    packet = usr.transactionPacketCreator(productId,productName,productNumber,fromPlace,toPlace,date)
    skt = socket.socket()
    skt.bind((userInfo[0],userInfo[1]))
    skt.listen(5)
    threadClient = threading.Thread(target=startClient,args=(packet,))
    threadClient.start()
    result = ""
    while(True):
        c,addr = skt.accept()
        result = c.recv(1024)
        if result != "":
            break
    print(result)







def userScreen():
    while(True):
        print("x" * 20)
        print("1-> Enter Transaction")
        print("x" * 10)
        print("2-> EXIT")
        print("x" * 20)
        ch = int(input("Enter Choice : "))
        if ch==1:
            trasactionEnterScreen()
        elif ch == 2:
            break

def userEnterScreen():
    skt = socket.socket()
    skt.bind((userInfo[0], int(userInfo[1])))
    skt.listen(5)
    while(True):
        print("x" * 20)
        userId = input("Enter User Id : ")
        password = input("Enter Password : ")
        packet = lgn.logInPacketCreator(userId, password)
        threadClient = threading.Thread(target=startClient,args=(packet,))
        threadClient.start()
        result = ""
        while (True):
            c, addr = skt.accept()
            result = c.recv(1024)
            if result != "":
                break
        if result == "True":
            userScreen()
        else:
            print("wrong userId and Password....")



