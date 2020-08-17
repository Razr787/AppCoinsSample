from json import loads

from web3 import Web3, HTTPProvider
from contract_adress import ContractAdress

from user import User, UserSol

web3 = Web3(HTTPProvider("http://127.0.0.1:8545", request_kwargs={"timeout": 60}))


def get_params(sender):
    return {"from": sender, "gasPrice": web3.eth.gasPrice, "gas": 6721975,
            "nonce": web3.eth.getTransactionCount(sender)}

# Read HelloWorld Contract
with open("build/contracts/HelloWorld.json", "r") as f_handler:
    contract_info = loads(f_handler.read())
    f_handler.close()

# Get HelloWorld Contract
helloworld_contract = web3.eth.contract(ContractAdress.HELLOWORLD.value, abi=contract_info["abi"])

#########################
# TESTAR MULTIPLE USERS #
#########################

# users = [["hello joao", 24],["hello mafalda", 25]]

# helloworld_contract.functions.addUserVerbose(users[0]).call()
# helloworld_contract.functions.addMultipleUsersVerbose(users).call()
# tx_params = helloworld_contract.functions.addMultipleUsersVerbose(users).buildTransaction(get_params(web3.eth.accounts[0]))
# txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
# print("TXID: {}".format(txid))
# print("\nAdd User (Transaction):\n{}".format(web3.eth.getTransaction(txid)))

# receipt = web3.eth.getTransactionReceipt(txid)
# print("\nNewUser (Event):")
# for elem in helloworld_contract.events.NewUser().processReceipt(receipt):
#     print(" - event: {}".format(elem))

# print("\nUSER: {}".format(helloworld_contract.functions.getUser(2).call()))

#############################
# END: ESTAR MULTIPLE USERS #
#############################

#####################
# TESTAR DATA CLASS #
#####################

# user = User("pedro", 35)
# helloworld_contract.functions.addUserVerbose(user.values()).call()
# print("\nUSER: {}".format(helloworld_contract.functions.getUser(5).call()))

user = UserSol(name="joao", age="25")
helloworld_contract.functions.addUserVerbose(user.say_values()).call()
# print("\nUSER: {}".format(helloworld_contract.functions.getUser(5).call()))

##########################
# END: TESTAR DATA CLASS #
##########################