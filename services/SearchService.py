# create search request and sending packets.
# header of the sending packet is SRC
import mysql.connector
from contextlib import closing
import socket
import services.PacketService as pack

database = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3307",
    passwd="ergin00000",
    database="farmchain"
)

packetHeader = "SRC"

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


def getCustomerInfo():
    hst = socket.gethostname()
    cusHost = socket.gethostbyname(hst)
    cusPort = findFreePort()

    return [cusHost,cusPort]

def sendSearchRequest(productName):
    productName = str(productName).lower()
    while(True):
        miner = checkOnlineMiners()
        if miner != []:
            break
        print("...wait...")
    minerHost = miner[1]
    minerPort = miner[2]
    #1-> start server and client at the same time
    #2-> send packet to online miner
    #3-> while receive request from miner, listen network

def packetCreator(packetBody):
    packetType = pack.Packet.packetType[0]
    packetType = str(packetType)
    packet = [packetType,packetBody]
    return packet


