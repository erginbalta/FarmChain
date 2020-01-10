import mysql.connector
import socket
from contextlib import closing
import json

packetType = "ENT"
database = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3307",
    passwd="ergin00000",
    database="farmchain"
)

#start server and client at the same time and listen server
#send packet to miner

def findFreePort():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def checkMiner(userId):
    mycursor = database.cursor()
    sql = "select * from miners where userId='" +str(userId) +"';"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    if result != []:
        return True
    else:
        return False

def minerLogIn(userId,password):
    data = []
    x = checkMiner(userId)
    if x == True:
        with open("C:/repos/FarmChain/datas/userInformation.json",'r') as f:
            user = json.load(f)
            for i in user:
                if userId == i['userId'] and password == i['password']:
                    return True
            else:
                return False

def getFreeMiners():
    mycursor = database.cursor()
    sql = "select * from miners where status=1;"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result

def getLogInMiner():
    result = getFreeMiners()
    info = result[0]
    host = info[1]
    port = info[2]
    return [host,port]

def userConnectionObjects():
        hst = socket.gethostname()
        host = socket.gethostbyname(hst)
        port = findFreePort()
        return [host,port]

def logInPacketCreator(userId,password):
    info = userConnectionObjects()
    packet = [packetType,[userId,password],info[0],info[1]]
    return packet