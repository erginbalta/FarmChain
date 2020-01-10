import random
import socket
from datetime import datetime
import mysql.connector
from contextlib import closing
import hashlib
import datetime
import json



database = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3307",
    passwd="ergin00000",
    database="farmchain"
)

def timeRace():
    dttm = datetime.datetime.now()
    currentDateTime = str(dttm).split(' ')
    currentTime = currentDateTime[1]
    return currentTime

def getDateTime():
    dt = str(datetime.datetime.now()).split(' ')
    d = str(dt[0]).split('-')
    t = str(dt[1]).split(':')
    date = ""
    time = ""
    for i in range(len(d)):
        date = date + str(d[i])
    for j in range(len(t) - 1):
        time = time + str(t[j])

    dateTime = str(date) + str(time)
    return dateTime

def hashCreator():
    dateTime = getDateTime()
    result = hashlib.sha256(dateTime.encode()).hexdigest()

    return result

def findFreePort():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def saveMiner(userId):
    hst = socket.gethostname()
    host = socket.gethostbyname(hst)
    port = str(findFreePort())
    status = True

    mycursor = database.cursor()
    sql = "insert into miners (host,port,userId,status) values (%s,%s,%s,%s);"
    values = (host,port,status)
    mycursor.execute(sql,values,status)
    database.commit()
    print(str(mycursor.rowcount) +"Miner Saved...")

def getMinerInfo():
    hst = socket.gethostname()
    host = socket.gethostbyname(hst)
    port = str(findFreePort())

    return [host,port]

def checkHost(userId):
    hst = socket.gethostname()
    host = socket.gethostbyname(hst)
    port = str(findFreePort())

    mycursor = database.cursor()
    sql = "select * from miners where userId='" +str(userId) +"';"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if result != []:
        if host != result[1]:
            sql = "update miners set host='" +host +"' where userId'=" +str(userId) +"';"
            print("Host Updated...")
        else:
            print("Host Same...")
    else:
        print("There is no Miner like this...")

def makeOnline(userId):
    hst = socket.gethostname()
    host = socket.gethostbyname(hst)
    port = str(findFreePort())

    mycursor = database.cursor()
    sql = "update miners set status=true where userId='" +str(userId) +"';"
    mycursor.execute(sql)
    database.commit()
    checkHost(userId)
    print(">>>ONLINE>>>")

def makeOffline(userId):
    mycursor = database.cursor()
    sql = "update miners set status=false where userId='" + str(userId) + "';"
    mycursor.execute(sql)
    database.commit()
    print(">>>OFFLINE>>>")

def seeTransactionQueue():
    data = []
    with open("/datas/transactionQueue.json",'r') as outfile:
        data = json.load(outfile)
    for i in data:
        print("x"*10)
        print(i)
    print("x"*10)

def seeBlockchain():
    data = []
    with open("/datas/blockchain.json",'r') as file:
        data = json.load(file)
    for i in data:
        print("x"*10)
        print(i)
    print("x"*10)

def findLastBlock():
    with open("/datas/blockchain.json",'r') as f:
        blockchain = json.load(f)
        ind = len(blockchain)-1
    return ["BLK",blockchain[ind]]

def addBlock(block):
    data = []
    with open("/datas/blockchain.json",'r') as file:
        data = json.load(file)
        data.append(block)

    with open("/datas/blockchain.json",'w') as f:
        json.dump(data,f)

    return None

def addBlockchain(transaction):
    hsh = hashCreator()
    timestamp = getDateTime()
    data = []
    length = 0
    previousHash = ""
    chain={}
    with open("/datas/blockchain.json",'r') as f:
        blockchain = json.load(f)
        blockchainLength = len(blockchain)
        previousBlock = blockchain[blockchainLength-1]
        previousHash = previousBlock['hash']
        chain = {
            "hash":str(hsh),
            "previousHash":str(previousHash),
            "transaction":transaction,
            "timestamp":str(timestamp)
        }
        data.append(chain)
    with open("/datas/blockchain.json",'w') as file:
        json.dump(data,file)
    print("x"*10)
    print("Transaction Added Blockchain")
    print("x"*10)

def addTransactionQueue(transaction):
    transactionQueue = []
    with open("/datas/transactionQueue.json",'r') as outfile:
        transactionQueue = json.load(outfile)
        transactionQueue.append(transaction)

    with open("/datas/transactionQueue.json",'w') as f:
        json.dump(transactionQueue,f)

def winPacketCreator(count):
    packetType = "WNN"
    packet = [packetType,count]
    return packet

def writeUserRecord(userInfo):
    users = []
    userId = ""
    with open("/datas/userInformation.json", 'r') as outfile:
        users = json.load(outfile)
        users.append(userInfo)

    with open("/datas/userInformation.json", 'w') as f:
        json.dump(users, f)
    return userInfo[0]



def startRace():
    count = 0
    result = []
    while(True):
        num = random.randint(0, 9999)
        hsh = hashlib.sha256(str(num).encode('utf-8')).hexdigest()
        if count == 1000:
            result = [False,count]
        if str(hsh).startswith("000"):
            result = [True, count]
            break
        else:
            count = count + 1

    return result



def logInOperation(packet):
    userInfo = packet[1]
    username = userInfo[0]
    password = userInfo[1]
    data = []
    with open('/datas/userInformation.json','r') as file:
        users = json.load(file)
        for user in users:
            if username == user['userId'] and password == user['password']:
                return True
    return False

def searchBlockchain(key):
    senderPacket = []
    block = []
    with open('/datas/blockchain.json','r') as file:
        block = json.load(file)
        for i in block:
            trans = i['transaction']
            name = trans['productName']
            if key == name:
                senderPacket.append(i)
    return senderPacket


def packetSeparator(packet):
    packetType = packet[0]
    if packetType == "SRC":
        response = [searchBlockchain(packet[1]),packet[2],packet[3]]
        return response
    elif packetType == "ENT":
        response = [logInOperation(packet),packet[2],packet[3]]
        return response
    elif packetType == "INF":
        response = [writeUserRecord(packet[1]),packet[2],packet[3]]
        return response
    elif packetType == "WNN":
        time = packet[1]
        myTime = timeRace()
        if int(time[0]) < int(myTime[0]) or int(time[1]) < int(myTime[1]) or float(time[2]) < float(myTime[2]):
            addBlockchain(packet[1])
            return True
        return False
    elif packetType == "BLK":
        addBlock(packet[1])




