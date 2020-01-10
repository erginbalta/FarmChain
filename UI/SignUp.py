import services.UserService as usr
import services.MinerService as mnr
import socket
import threading

def sendSignUpInfo(packet):
    minersInfo = usr.checkOnlineMiners()
    skt = socket.socket()
    for i in minersInfo:
        host = i[1]
        port = i[2]
        skt.connect((host,port))
        skt.send(packet)
    skt.close()


def signUpScreen():
    print("x"*20)
    password = input("Password : ")
    name = input("Name : ")
    surname = input("Surname : ")
    company = input("Company : ")
    status = input("Status : ")
    print("x"*20)
    packet = usr.userInfoPacket(password,name,surname,company,status)
    userInfo = usr.getUserConnectionInfo()
    thread = threading.Thread(target=sendSignUpInfo,args=(packet,))
    skt = socket.socket()
    skt.bind((userInfo[0],int(userInfo[1])))
    thread.start()
    while(True):
        c,addr = skt.accept()
        result = c.recv(1024)
        if result != None:
            print(result)
            break

