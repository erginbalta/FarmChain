import socket
import struct
import threading
import time
import traceback
import P2P.p2p as p




def menu():
    while(True):
        print("x" * 20)
        print("1-> Search")
        print("x" * 10)
        print("2-> User Enter")
        print("x" * 10)
        print("3-> Miner Enter")
        print("x" * 10)
        print("4-> Sign Up")
        print("x"*10)
        print("5-> Exit")
        print("x" * 20)
        choice = int(input("Enter choice >> "))
        if (choice == 1):
            pass
        elif (choice == 2):
            pass
        elif (choice == 3):
            pass
        elif (choice == 4):
            pass
        elif (choice == 5):
            break
        else:
            print(">> Enter Number <<")

def main():
    peer = p.Peer()
    peerConn = p.PeerConnection()


if __name__ == '__main__':
    main()

madenciler = {
    "m1":["host","port","madenciId"],
    "m2":["host","port","madenciId"],
    "m3":["host","port","madenciId"]
}
