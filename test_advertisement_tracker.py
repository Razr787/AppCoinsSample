from json import loads

from web3 import Web3, HTTPProvider
from contract_adress import ContractAdress

web3 = Web3(HTTPProvider("http://127.0.0.1:8545", request_kwargs={"timeout": 60}))


def get_params(sender):
    return {"from": sender, "gasPrice": web3.eth.gasPrice, "gas": 6721975,
            "nonce": web3.eth.getTransactionCount(sender)}

# Read AppCoins Contract
with open("build/contracts/AppCoins.json", "r") as f_handler:
    contract_info = loads(f_handler.read())
    f_handler.close()

# Get AppCoins Contract
appcoins_contract = web3.eth.contract(ContractAdress.APPCOINS.value, abi=contract_info["abi"])

# Read AdvertisementTracker Contract
with open("build/contracts/AdvertisementTracker.json", "r") as f_handler:
    contract_info = loads(f_handler.read())
    f_handler.close()

# Get AdvertisementTracker Contract
advertisement_tracker_contract = web3.eth.contract(ContractAdress.ADVERTISEMENTTRACKER.value, abi=contract_info["abi"])

def print_balances_general(func, coin, call=False):
    i = 0
    for account in web3.eth.accounts:
        print(" - Account {}: {} {}".format(i, func(account).call() if call else func(account), coin))
        i += 1


def print_balances_ether():
    # Ether Balances
    print("\nEther Balances:")
    print_balances_general(web3.eth.getBalance, "ETH")


def print_balances_appcoins():
    # AppCoins Balances
    print("\nAppCoins Balances:")
    print_balances_general(appcoins_contract.functions.balanceOf, "APPC", True)

###### APPROVE ######
tx_params = appcoins_contract.functions.approve(ContractAdress.APPCOINSIAB.value, 10000)\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
###### END: APPROVE ######

###### CREATE CAMPAIGN ######
print("\n\n###### CREATE CAMPAIGN ######")

tx_params = advertisement_tracker_contract.functions.createCampaign(txid, "packageName", [1,2,3], 1, 100, 1, 3, "endPoint")\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid_1 = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid_1))
print("\nTransfer (Transaction):\n{}".format(web3.eth.getTransaction(txid_1)))

receipt = web3.eth.getTransactionReceipt(txid_1)
print("\nCampaignLaunched (Event):\n{}".format(
    advertisement_tracker_contract.events.CampaignLaunched().processReceipt(receipt)))

print("\n###### END: CREATE CAMPAIGN ######")
###### END: CREATE CAMPAIGN ######

###### CANCEL CAMPAIGN ######
print("\n\n###### CANCEL CAMPAIGN ######")

tx_params = advertisement_tracker_contract.functions.cancelCampaign(txid)\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid_1 = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid))
print("\nTransfer (Transaction):\n{}".format(web3.eth.getTransaction(txid_1)))

receipt = web3.eth.getTransactionReceipt(txid_1)
print("\nCampaignCancelled (Event):\n{}".format(
    advertisement_tracker_contract.events.CampaignCancelled().processReceipt(receipt)))

print("\n###### END: CANCEL CAMPAIGN ######")
###### END: CANCEL CAMPAIGN ######

###### BULK REGISTER POA ######
print("\n\n###### BULK REGISTER POA ######")

tx_params = advertisement_tracker_contract.functions.bulkRegisterPoA(txid, txid, txid, 1)\
    .buildTransaction(get_params(web3.eth.accounts[1]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid))
print("\nTransfer (Transaction):\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nBulkPoARegistered (Event):\n{}".format(
    advertisement_tracker_contract.events.BulkPoARegistered().processReceipt(receipt)))

print("\n###### END: BULK REGISTER POA ######")
###### END: BULK REGISTER POA ######

###### BULK CANCEL CAMPAIGN ######
print("\n\n###### BULK CANCEL CAMPAIGN ######")

tx_params = advertisement_tracker_contract.functions.cancelMultipleCampaigns([txid, txid_1, txid])\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid_1 = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid))
print("\nTransfer (Transaction):\n{}".format(web3.eth.getTransaction(txid_1)))

receipt = web3.eth.getTransactionReceipt(txid_1)
print("\nCampaignCancelled (Event):")
for elem in advertisement_tracker_contract.events.CampaignCancelled().processReceipt(receipt):
    print(" - event: {}".format(elem))
    

print("\n###### END: BULK CANCEL CAMPAIGN ######")
###### END: BULK CANCEL CAMPAIGN ######

###### BULK CREATE CAMPAIGN ######
print("\n\n###### BULK CREATE CAMPAIGN ######")

tx_params = advertisement_tracker_contract.functions.createMultipleCampaigns(
    [txid, txid_1],
    ["packageName2", "packageName3"], 
    [[4,5,6],[7,8,6]],
    [1, 3],
    [100, 300],
    [1,2], 
    [3,6],
    ["endPoint1","endPoint3"])\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid_1 = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid_1))
print("\nTransfer (Transaction):\n{}".format(web3.eth.getTransaction(txid_1)))

receipt = web3.eth.getTransactionReceipt(txid_1)
print("\nCampaignLaunched (Event):")
for elem in advertisement_tracker_contract.events.CampaignLaunched().processReceipt(receipt):
    print(" - event: {}".format(elem))


print("\n###### END: BULK CREATE CAMPAIGN ######")
###### END: BULK CREATE CAMPAIGN ######

###### BULK BULK REGISTER POA ######
print("\n\n###### BULK BULK REGISTER POA ######")

tx_params = advertisement_tracker_contract.functions.bulkRegisterPoaOfMultipleCampaigns(
    [txid, txid_1], [txid, txid_1], [txid, txid_1], [1,2])\
    .buildTransaction(get_params(web3.eth.accounts[1]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid))
print("\nTransfer (Transaction):\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nBulkPoARegistered (Event):")
for elem in advertisement_tracker_contract.events.BulkPoARegistered().processReceipt(receipt):
    print(" - event: {}".format(elem))

print("\n###### END: BULK BULK REGISTER POA ######")
###### END: BULK BULK REGISTER POA ######

print_balances_ether()

print_balances_appcoins()


