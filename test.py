import Blockchain
from random import randint


users = ['Rajat','Vivek','Gautam','Shaurya','DJ','Samrath','Vijender','Utkarsh']
n = len(users)

bc = Blockchain.Blockchain()

count = 0

while(count < 9):
    sender = randint(0,n-1)
    reciever = randint(0,n-1)
    if(not sender ==  reciever):
        bc.addTransaction(users[sender],users[reciever])
        count+=1

print(bc)
