
import services.SearchService as src
import socket
import threading



def startClient(packet):
    freeMiner = src.checkOnlineMiners()
    skt = socket.socket()
    skt.connect((freeMiner[1],int(freeMiner[2])))
    skt.send(packet)
    skt.close()


def searchProduct():
    result = []
    print("x" * 20)
    userInput = input("Enter Product Name : ")
    print("result wait....")
    info = src.getCustomerInfo()
    packet = src.packetCreator(userInput,info[0],info[1])
    skt = socket.socket()
    skt.bind((info[0],int(info[1])))
    skt.listen(5)
    threadClient = threading.Thread(target=startClient,args=(packet,))
    threadClient.start()
    print("x"*20)
    print("thread started...")
    print("x"*20)
    while(True):
        c,addr = skt.accept()
        result = c.recv(1024)
        if result != []:
            break
    for i in result[1]:
        print(i +"\n")
