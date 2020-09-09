from hashlib import sha256
import pickle
from datetime import datetime
from multiprocessing import Process
from random import randint


class Queue():
    def __init__(self):
        self.item = []
    
    def insert(self,item):
        self.item.append(item)
    
    def delete(self):
        item = self.item[0]
        self.item.pop(0)
        return item
    def size(self):
        return len(self.item)


class Transaction():
    
    #CREATE YOUR TRANSACTION CLASS AS PER REQUIREMENT

    def __init__(self):
        self.sender = None
        self.reciever = None
        self.hash = None
        self.timestamp = None
        self.nonce = None
    
    def __str__(self):
        return self.hash
    
    def initiate(self,sender,reciever):
        self.sender = sender
        self.reciever = reciever
        self.timestamp = str(datetime.now())
        self.nonce = randint(2**3,2**50)
        temp = sha256()
        temp.update(
            str(self.sender).encode()+
            str(self.reciever).encode()+
            str(self.nonce).encode()
        )
        self.hash = temp.hexdigest()

class Block():
    
    def __init__(self,height=0,parent_hash = '0'*64):
        self.height = height
        self.hash = None
        self.parent_hash = parent_hash
        self.transaction = None
        self.nonce = None
    
    def __str__(self):
        return str(self.hash)
    
    def _getAllHash(self):
        #This method is hardcoded
        #Please change this according to your transaction size
        hash12 = sha256(
            str(self.transaction[0].hash).encode()+
            str(self.transaction[1].hash).encode()
        ).hexdigest()
        hash34 = sha256(
            str(self.transaction[2].hash).encode()+
            str(self.transaction[3].hash).encode()
            ).hexdigest()
        hash56 = sha256(str(self.transaction[4].hash).encode()+
        str(self.transaction[5].hash).encode()
        ).hexdigest()
        hash78 = sha256(
            str(self.transaction[6].hash).encode()+
            str(self.transaction[7].hash).encode()
            ).hexdigest()
        hash1234 = sha256(
            str(hash12).encode()+
            str(hash34).encode()
            ).hexdigest()
        hash5678 = sha256(
            str(hash56).encode()+
            str(hash78).encode()
            ).hexdigest()
        hash12345678 = sha256(
            str(hash1234).encode()+
            str(hash5678).encode()
            ).hexdigest()
        return hash12345678

    
    def mine(self):
        allhash = self._getAllHash()
        height = self.height
        parent_hash = self.parent_hash
        while True:
            #Proof of work
            nonce = randint(2**3,2**50)
            hashNonce = sha256(
                str(height).encode()+
                str(parent_hash).encode()+
                str(nonce).encode()
                ).hexdigest()
            Hash = sha256(
                str(allhash).encode()+
                str(hashNonce).encode()
                ).hexdigest()
            if(Hash[0:4] == '0000'): #proof of work ---> hash begining with leading four 0's
                break
        self.hash = Hash
        self.nonce = nonce


class Blockchain():

    def __init__(self):
        self.mainChain = self._loadBlockchain()
        self.transactionQueue = self._loadTransactionQueue()
        self.transactionQueueSize = self.transactionQueue.size()
    
    def __str__(self):
        blockchain = '.'*100+"\n\n"
        if len(self.mainChain) == 0:
            blockchain = None
        else:
            for block in self.mainChain:
                blockstr = ''
                blocktrans = ''
                try:
                    for tans in block.transaction:
                        blocktrans+="#"*50+"\n"
                        blocktrans+='\tsender : '+str(tans.sender)+"\n"
                        blocktrans+='\treciever : '+str(tans.reciever)+"\n"
                        blocktrans+='\ttimestamp : '+str(tans.timestamp)+"\n"
                        blocktrans+='\tnonce : '+str(tans.nonce)+"\n"+"#"*50+"\n"
                except:
                    blocktrans+="No transactions"
                blockstr+="height : "+str(block.height)+"\n"
                blockstr+="parent hash : "+str(block.parent_hash)+"\n"
                blockstr+="transactions......\n"+blocktrans+"\n"
                blockstr+="nonce : "+str(block.nonce)+"\n"
                blockstr+="hash : "+str(block.hash)+"\n"
                blockchain+=blockstr+"\n\n"+"."*100+"\n"
        return blockchain
    
    def _loadBlockchain(self):
        blockchain = []
        try:
            f = open('.blockchain.txt','rb')
            blockchain = pickle.load(f)
            f.close()
        except:
            block = None
        return blockchain
    
    def _loadTransactionQueue(self):
        q = Queue()
        try:
            f = open('.transactionQueue.txt','rb')
            q = pickle.load(f)
            f.close()
        except:
            pass
        return q
    
    def _saveBlockchain(self):
        f = open('.blockchain.txt','wb')
        pickle.dump(self.mainChain,f)
        f.close()
        g = open('.transactionQueue.txt','wb')
        pickle.dump(self.transactionQueue,g)
        g.close()

    
    def _getPreviousBlock(self):
        if len(self.mainChain) > 0:
            return self.mainChain[-1]
        return None
    
    def getTransactionList(self):
        tlist = []
        count = 0
        while(count < 8):
            count+=1
            tlist.append(self.transactionQueue.delete())
            #print(type(tlist[-1]))
        #print("#EXITING getTransactionList")
        return tlist
    
    def mine(self):
        #print("#GOT TO mine")
        transactionList = self.getTransactionList()
        prev_block = self._getPreviousBlock()
        h = 0
        ph = '0'*64
        if(not prev_block == None):
            h = prev_block.height + 1
            ph = prev_block.hash
        block = Block(h,ph)
        block.transaction = transactionList
        block.mine()
        #print("#EXITING mine")
        return block
    
    def Mine(self):
        #print("#GOT TO MINE")
        block = self.mine()
        #print(block)
        self.mainChain.append(block)
        #print("#EXITING MINE...")

    
    def addTransaction(self,sender,reciever):
        t = Transaction()
        t.initiate(sender,reciever)
        self.transactionQueue.insert(t)
        self.transactionQueueSize = self.transactionQueue.size()
        if(self.transactionQueueSize > 8):
            self.Mine()
        
        self._saveBlockchain()
