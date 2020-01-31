import mysql.connector
import socket
from contextlib import closing
import json
import random

packetType= ["INF","TRN","USR"]
database = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3307",
    passwd="ergin00000",
    database="farmchain"
)

def userIdCreator():
    data = []
    numericId = 0
    id = ""
    with open("/datas/userInformation.json",'r') as f:
        user = json.load(f)
        numericId = len(user) + 1
        id = str(packetType[2])+str(numericId)
    return id

def transactionIdCreator():
    idKey = packetType[1]
    numericId = random.randint(10000,99999)
    id = idKey+str(numericId)
    return id

def getUserConnectionInfo():
    hst = socket.gethostname()
    usrHost = socket.gethostbyname(hst)
    usrPort = findFreePort()
    return [usrHost,usrPort]

def findFreePort():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def checkOnlineMiners():
    mycursor = database.cursor()
    sql = "select * from miners where status = 1;"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result

def minerInfo():
    result = checkOnlineMiners()
    info = result[0]
    host = result[1]
    port = result[2]
    return [host,port]

def userInfoPacket(password,name,surname,company,status):
    info = getUserConnectionInfo()
    userId = userIdCreator()
    name = str(name).lower()
    surname = str(surname).lower()
    company = str(company).lower()
    status = str(status).lower()
    packet = [packetType[0],[userId,password,name,surname,company,status],info[0],info[1]]
    return packet

def transactionPacketCreator(productId,productName,productNumber,fromPlace,toPlace,date):
    info = getUserConnectionInfo()
    transactionId = transactionIdCreator()
    productName = str(productName).lower()
    fromPlace = str(fromPlace).lower()
    toPlace = str(toPlace).lower()
    packet = [packetType[1],[transactionId,productId,productName,productNumber,fromPlace,toPlace,date],info[0],info[1]]
    return packet




