import os
import json as js


def fileCreator():
    if not os.path.exists("/datas"):
        os.makedirs("/datas")
    else:
        print("File Allready Exists")

def blockChain():
    pass
