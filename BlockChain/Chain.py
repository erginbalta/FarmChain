from Domain import Transaction as trn
import hashlib as hsh

class Chain:
    hash = ""
    prevHash = ""
    transaction = []
    timeStamp = ""

    def __init__(self,hash,prevHash,transaction,timeStamp):
        self.hash = hash
        self.prevHash = prevHash
        self.transaction = transaction
        self.timeStamp = timeStamp


    def createChain(self):
        chain = {
            "hash":self.hash,
            "previousHash":self.prevHash,
            "transaction": self.transaction,
            "timeStamp":self.timeStamp
        }
        return chain

    def createHash(self):
        trans = trn.Transaction()
        hash = hsh.sha256(str(trans.transactionId).encode()).hexdigest()
        return hash
