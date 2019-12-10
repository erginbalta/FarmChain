import mysql.connector
import socket
from contextlib import closing

packetType = "ENT"
database = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3307",
    passwd="ergin00000",
    database="farmchain"
)

def findFreePort():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def createLogInPacket(userId,password):
    info = [str(userId).lower(),str(password)]
    packet = [packetType,info]
    return packet

def checkMiner(userId):
    mycursor = database.cursor()
    sql = "select * from miners where minerId=" +str(userId) +";"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    if result != []:
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
    return result[0]

def userConnectionObjects():
    if checkMiner() == False:
        hst = socket.gethostname()
        host = socket.gethostbyname(hst)
        port = findFreePort()
        info = [str(host),str(port)]
        return info

