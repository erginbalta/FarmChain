import socket
import struct
import threading
import time
import traceback

def debug(msg):
    print("[%s] %s" %(str(threading.currentThread().getName()), msg))

class Peer:
    def __init__(self, maxPeer, serverPort, id = None, serverHost= None):
        self.debug = 0
        self.maxPeer = int(maxPeer)
        self.serverPort = int(serverPort)
        if serverHost:
            self.serverHost = serverHost
        else:
            self.id = '%s:%d' %(self.serverHost, self.serverPort)
        self.peerLock = threading.Lock()
        self.peers = {}
        self.shutDown = False
        self.handlers = {}
        self.router = None

    def __debug(self, msg):
        if self.debug:
            debug(msg)

    def __handlePeer(self, clientSock):
        self.__debug("New child " +str(threading.currentThread().getName()))
        self.__debug("Connected " +str(clientSock.getPeerName()))

        host, port = clientSock.getPeerName()
        peerConn = PeerConnection(None, host, port, clientSock, debug=False)
        try:
            msgType, msgData = peerConn.recvData()
            if msgType:
                msgType = str(msgType).upper()
            if msgType not in self.handlers:
                self.__debug("not handled: %s: %s" %(msgType, msgData))
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()

        self.__debug("Disconnecting " +str(clientSock.getPeerName()))

    def __runStabilizer(self, stabilizer, delay):
        while not self.shutDown:
            stabilizer()
            time.sleep(delay)

    def setId(self, id):
        self.id = id

    def startStabilizer(self, stabilizer, delay):
        t = threading.Thread(target= self.__runStabilizer, args= [stabilizer, delay])
        t.start()

    def addHandler(self, msgType, handler):
        assert len(msgType) == 4
        self.handlers[msgType] = handler

    def addRouter(self, router):
        self.router = router

    def addPeer(self, peerId, host, port):
        if peerId not in self.peers and (self.maxPeer == 0 or len(self.peers) < self.maxPeer):
            self.peers[peerId] = (host, int(port))
            return True
        else:
            return False

    def getPeer(self, peerId):
        return self.peers[peerId]


    def removePeer(self, peerId):
        if peerId in self.peers:
            del self.peers[peerId]

    def addPeerAt(self, lock, peerId, host, port):
        self.peers[lock] = (peerId, host, int(port))

    def getPeerAt(self, lock):
        if lock not in self.peers:
            return None
        return self.peers[lock]

    def removePeerAt(self, lock):
        if lock in self.peers:
            del self.peers[lock]

    def getPeerId(self):
        return self.peers.keys()

    def numberOfPeers(self):
        return len(self.peers)

    def maxPeersReached(self):
        assert self.maxPeer == 0 or len(self.peers) <= self.maxPeer
        return self.maxPeer > 0 and len(self.peers) == self.maxPeer

    def makeServerSocket(self, port, backlog=5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(backlog)
        return s

    def sendToPeer(self, peerId, msgType, msgData, waitReply=True):
        if self.router:
            nextpId, host, port = self.router(peerId)
        if not self.router or nextpId:
            self.__debug("unable to route %s to %s" %(msgType, peerId))
            return None
        return self.connectAndSend(host, port, msgType, msgData, pid=nextpId, waitReply=waitReply)

    def connectAndSend(self, host, port, msgType, msgData, pid=None, waitReply=True):
        msgReply = []
        try:
            peerConn = PeerConnection(pid, host, port, debug=self.debug)
            peerConn.sendData(msgType, msgData)
            self.__debug("Sent %s: %s" %(pid, msgType))

            if waitReply:
                onceReply = peerConn.recvData()
                while (onceReply != (None, None)):
                    msgReply.append(onceReply)
                    self.__debug("Got reply %s: %s" %(pid, str(msgReply)))
                    onceReply = peerConn.recvData()
            peerConn.close()
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
        return msgReply

    def checkLivePeers(self):
        toDelete = []
        for pid in self.peers:
            isConnect = False
            try:
                self.__debug("Check Live %s" %(pid))
                host, port = self.peers[pid]
                peerConn = PeerConnection(pid, host, port, debug=self.debug)
                peerConn.sendData('PING', '')
                isConnect=True
            except:
                toDelete.append(pid)

            if isConnect:
                peerConn.close()

        self.peerLock.acquire()
        try:
            for pid in toDelete:
                if pid in self.peers:
                    del self.peers[pid]
        finally:
            self.peerLock.release()

    def mainLoop(self):
        s = self.makeServerSocket(self.serverPort)
        s.settimeout(2)
        self.__debug("Server Started %s (%s : %d)" %(self.id, self.serverHost, self.serverPort))

        while not self.shutDown:
            try:
                self.__debug("Listening for Connection ... ")
                clientSock, clientAddr = s.accept()
                clientSock.settimeout(None)

                t = threading.Thread(target= self.__handlePeer, args= [clientSock])
                t.start()
            except KeyboardInterrupt:
                print("Keybord Interrupt : Stop mainloop")
                self.shutDown = True
                continue
            except:
                if self.debug:
                    traceback.print_exc()
                    continue
        self.__debug("Main Loop Exiting")
        s.close()

#-----------------------------------------------------------

class PeerConnection:
    def __init__(self, peerId, host, port, sock=None, debug=False):
        self.id = peerId
        self.debug = debug

        if not sock:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, int(port)))
        else:
            self.s = sock
        self.sd = self.s.makefile('rw',0)

    def __makeMsg(self, msgType, msgData):
        msgLen = len(msgData)
        msg = struct.pack("!4sL%ds" % msgLen, msgType, msgLen, msgData)
        return msg

    def __debug(self, msg):
        if self.debug:
            debug(msg)

    def sendData(self, msgType, msgData):
        try:
            msg = self.__makeMsg(msgType, msgData)
            self.sd.write(msg)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return False
        return True

    def recvData(self):
        try:
            msgType = self.sd.read(4)
            if not msgType:
                return (None, None)
            lenStr =  self.sd.read(4)
            msgLen = int(struct.unpack("!L", lenStr)[0])
            msg = ""
            while (len(msgType) != msgLen):
                 data = self.sd.read(min(2048, msgLen - len(msg)))
                 if not len(data):
                     break
                 msg = msg + data
            if len(msg) != msgLen:
                 return (None, None)

        except KeyboardInterrupt:
                raise
        except:
            if self.debug:
                traceback.print_exc()
            return (None, None)

        return (msgType, msg)

    def close(self):
        self.s.close()
        self.s = None
        self.sd = None

    def __str__(self):
        return "|%s|" %(id)

