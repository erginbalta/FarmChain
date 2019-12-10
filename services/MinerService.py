import os
import random
import socket
from datetime import datetime
import mysql.connector
from contextlib import closing
import hashlib
import struct
import threading
import datetime
import traceback
import TcpServerNode
import services.PacketService as pack
import json
import time

Node = TcpServerNode.Node()
NodeConnection = TcpServerNode.NodeConnection()

database = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3307",
    passwd="ergin00000",
    database="farmchain"
)

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


def saveMiner():
    hst = socket.gethostname()
    host = socket.gethostbyname(hst)
    port = str(findFreePort())
    status = True

    mycursor = database.cursor()
    sql = "insert into miners (host,port,status) values (%s,%s,%s);"
    values = (host,port,status)
    mycursor.execute(sql,values,status)
    database.commit()
    print(str(mycursor.rowcount) +"Miner Saved...")


def checkHost(minerId):
    hst = socket.gethostname()
    host = socket.gethostbyname(hst)
    port = str(findFreePort())

    mycursor = database.cursor()
    sql = "select * from miners where minerId=" +str(minerId) +";"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if result != []:
        if host != result[1]:
            sql = "update miners set host='" +host +"' where minerId=" +str(minerId) +";"
            print("Host Updated...")
        else:
            print("Host Same...")
    else:
        print("There is no Miner like this...")





def makeOnline(minerId):
    hst = socket.gethostname()
    host = socket.gethostbyname(hst)
    port = str(findFreePort())

    mycursor = database.cursor()
    sql = "update miners set status=true where minerId=" +str(minerId) +";"
    mycursor.execute(sql)
    database.commit()

    checkHost(minerId)

    #1-> start server and client at the same time
    #2-> listen network

def checkUserEntry(packet):
    userId = packet[0]
    userPsw = packet[1]


def addBlockchain(transaction):
    hsh = hashCreator()
    timestamp = getDateTime()
    data = []
    length = 0
    previousHash = ""
    chain={}
    with open("/datas/blockchain.json",'r') as f:
        data = json.load(f)
        blockchain = data['blockchain']
        blockchainLength = len(blockchain)
        previousBlock = blockchain[blockchainLength-1]
        previousHash = previousBlock['previousHash']
        chain = {
            "hash":str(hsh),
            "previousHash":str(previousHash),
            "transaction":transaction,
            "timestamp":str(timestamp)
        }
        data['blockchain'].append(chain)
    with open("/datas/blockchain.json",'w') as file:
        json.dump(data,file)

def minerRace():
    cnt = 0
    a = str(datetime.datetime.now()).split(' ')
    b = str(a[1]).split(':')
    strt = b[2]
    strt = float(strt)
    while (True):
        timestamp = time.time()
        timestamp = str(timestamp)
        tm = timestamp.split('.')
        msg = "WIN"
        msg = str(tm[1]) + msg
        hsh = hashlib.sha256(msg.encode()).hexdigest()
        x = str(datetime.datetime.now()).split(' ')
        y = str(x[1]).split(':')
        fnsh = y[2]
        fnsh = float(fnsh)
        result = fnsh - strt
        if int(result) == 15:
            print("LOSER timeout...")
            break
        if msg.startswith('000'):
            print("ok")
            print(strt)
            print(fnsh)
            print(result)
            print(msg)
            print(hsh)
            break
        else:
            print("wait")
            cnt = cnt + 1
            print(cnt)




