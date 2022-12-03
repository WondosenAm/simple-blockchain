# Importing necessary packages
import datetime
import hashlib
import json


# define Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        
        # a genesis block which is the first block in the chain
        self.Add_block(proof=1,transaction=0, previous_hash='0') 
    
    # define a function which accept input from console/user
    def get_transaction_value(self):
        
        print('Please enter transaction to add to the block')
        
        sender = input('Enter the recipient of the transaction: ')
        recipient = input('Enter the recipient of the transaction: ')

        amount = float(input('Enter your transaction amount '))

        return sender, recipient, amount
    
    # function to add new transaction
    def add_new_transaction(self,sender,recipient,  amount=1.0):
        transaction=[]
        data = {'sender': sender,

                'recipient': recipient,

                'amount': amount}

        transaction.append(data)
        return transaction
    
    # create a block
    def Add_block(self, proof, transaction,previous_hash):
        
        block = {
           'index': len(self.chain) + 1,
           'timestamp': str(datetime.datetime.now()),
           'proof': proof,
           'transaction':transaction,
           'previous_hash': previous_hash
        }

        self.chain.append(block)
        return block
    
    # used get the last block in the chain
    def last_block(self):
        last_block = self.chain[-1]
        return last_block
    
    # concensus algorithm which used for proofing purpose
    def proof_of_work(self, previous_proof):
        # miners proof submitted
        new_proof = 1
        difficulty=2
        # status of proof of work
        check_proof = False
        while check_proof is False:
            
            hashop = hashlib.sha256(str(new_proof ** difficulty - previous_proof ** difficulty).encode()).hexdigest()
            
            
            if hashop[:2] == '00':
                check_proof = True
            else:
               
                new_proof += 1
        return new_proof

    # generate a hash of an entire block
    def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # check if the blockchain is valid
    def verify_chain(self, chain):
       
        previous_block = chain[0] # the first block in the chain
        
        index = 1 # index of the blocks 
        while index < len(chain):
            
            block = chain[index]
            
            # check if the current block link to previous block has is the same as the hash of the previous block
            if block["previous_hash"] != self.hash_block(previous_block):
                return False

            # get the previous proof from the previous block
            previous_proof = previous_block['proof']

            
            current_proof = block['proof']

            
            hashOp = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            
            if hashOp[:2] != '00':
                return False
           
            previous_block = block
            index += 1
        return True
    


# initiate class object 
blockchain = Blockchain()


# create a block
def mine_add_block():
    
    last_block = blockchain.last_block()
    previous_proof = last_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash_block(last_block)
    
    sender,recipient, amount = blockchain.get_transaction_value()

    transaction=blockchain.add_new_transaction(sender,recipient, amount)
   
    block = blockchain.Add_block(proof,transaction, previous_hash)
    response = {'message': 'Block mined!',
               'index': block['index'],
               'timestamp': block['timestamp'],
               'proof': block['proof'],
                'transaction':block['transaction'],
               'previous_hash': block['previous_hash']}
    return response



def wholeBlockchain():
    response = {'The whole block chain \n': blockchain.chain}
    return response


def chain_length(): 
    return len(blockchain.chain)


# Check validity of blockchain
def valid():
	valid = blockchain.verify_chain(blockchain.chain)
	
	if valid:
		msg = {'message': 'The Blockchain is valid.'}
	else:
		msg = {'message': 'The Blockchain is not valid.'}
	return msg


# if not blockchain.verify_chain(blockchain.chain):

#        print('Blockchain manipulated')

#     Break

option=True
while(option):
    print('\nchoose a task that allows working with a blockchain. ')
    print('1. Add a new block')
    print('2. Show the last block')
    print('3. Show the whole block')
    print('4. Verify the blockchain')
    print('5. Verify and print the blockchain')
    print('6. Change data of particular block')
    print('7. Show number of blocks')
    print('8. End the script \n' )

    value = int(input('please enter your choice: '))

    if value==1:
        print(mine_add_block())

    elif value == 2:
        print(blockchain.last_block())

    elif value == 3:
        print(wholeBlockchain())

    elif value == 4:
        print(valid())

    elif value == 5:
        print(valid())
        print(wholeBlockchain())

    elif value == 6:
        if len(blockchain.chain) >= 1:

            blockchain.chain[0] = 1

    elif value == 7:
        print("Block Length: ",chain_length())
        
    elif value ==8:
        option = None
        break
    else :
        print('\n Unknown Option Selected!')