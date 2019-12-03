
import random as rnd

class Transaction:
    transactionId = ""
    productName = ""
    productNumber = ""
    fromPlace = ""
    toPlace = ""
    date = ""

    def __init__(self,productId,productName,productNumber,fromPlace,toPlace,date):
        self.transactionId = "TRN" + str(rnd.randint(1000,9999))
        self.productId = productId
        self.productName = productName
        self.productNumber = productNumber
        self.fromPlace = fromPlace
        self.toPlace = toPlace
        self.date = date




    def transactionCreator(self):

        transaction = {"id":self.transactionId, "productId":self.productId, "productName":self.productName,
                       "productNumber":self.productNumber, "from":self.fromPlace,
                       "to":self.toPlace, "data":self.date}
        return transaction



