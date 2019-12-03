import os
import random
import socket
import mysql.connector
from contextlib import closing
import struct
import threading
import time
import traceback
import TcpServerNode
import services.PacketService as pack

Node = TcpServerNode.Node()
NodeConnection = TcpServerNode.NodeConnection()

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

def packetOperation(packet):
    packetHeader = packet[0]
    packetBody = packet[1]
    pack.Packet.packetRouter(packetHeader)