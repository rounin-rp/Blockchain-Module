```
Easy Blockchain module written in python

#Features :
	-> Data Persistence
	-> Currently Holds 8 transactions on one block.
	-> Easy to understand and implement 
	-> Fast
	-> Proof of Work Consensus
	-> Uses concept of Merkle Tree

#How to use :
	-> import the module in a python file or interpreter
	-> create an object of 'Blockchain' class :
		>>> bc = Blockchain()
	-> to insert data use:
		>>> bc.addTransaction(sender,reciever)
	-> it will automatically mine after the number of transactions reaches more than 8
	-> data will be saved automatically
