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

# Read AppCoinsTracker Contract
with open("build/contracts/AppCoinsTracker.json", "r") as f_handler:
    contract_info = loads(f_handler.read())
    f_handler.close()

# Get AppCoinsTracker Contract
appcoins_tracker_contract = web3.eth.contract(ContractAdress.APPCOINSTRACKER.value, abi=contract_info["abi"])

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

###### BULK CANCEL CAMPAIGN ######
print("\n\n###### BULK CANCEL CAMPAIGN ######")

tx_params = appcoins_tracker_contract.functions.cancelCampaigns([txid, txid, txid])\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid_1 = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid))
print("\nTransfer (Transaction):\n{}".format(web3.eth.getTransaction(txid_1)))

receipt = web3.eth.getTransactionReceipt(txid_1)
print("\nCampaignCancelled (Event):")
for elem in appcoins_tracker_contract.events.CampaignCancelled().processReceipt(receipt):
    print(" - event: {}".format(elem))
    

print("\n###### END: BULK CANCEL CAMPAIGN ######")
###### END: BULK CANCEL CAMPAIGN ######

###### BULK CREATE MULTIPLE CAMPAIGN ######
print("\n\n###### BULK CREATE MULTIPLE CAMPAIGN ######")

campaign_lauched_information = [
    (txid, "packageName2", "endPoint1", [4,5,6], 1, 100, 1, 3),
    (txid_1, "packageName3", "endPoint2", [1,2,3], 2, 200, 2, 6),
]

tx_params = appcoins_tracker_contract.functions.createCampaigns(
    campaign_lauched_information)\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid_1 = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid_1))
print("\nTransfer (Transaction):\n{}".format(web3.eth.getTransaction(txid_1)))

receipt = web3.eth.getTransactionReceipt(txid_1)
print("\nCampaignLaunched (Event):")
for elem in appcoins_tracker_contract.events.CampaignLaunched().processReceipt(receipt):
    print(" - event: {}".format(elem))


print("\n###### END: BULK CREATE MULTIPLE CAMPAIGN ######")
###### END: BULK CREATE MULTIPLE CAMPAIGN ######

###### BULK REGISTER POA MULTIPLE CAMPAIGNS ######
print("\n\n###### BULK REGISTER POA MULTIPLE CAMPAIGNS ######")

bulks_poa_information = [
    (txid, txid, txid, 1),
    (txid_1, txid_1, txid_1, 2),
]

tx_params = appcoins_tracker_contract.functions.bulkRegisterPoaOfMultipleCampaigns(bulks_poa_information).buildTransaction(get_params(web3.eth.accounts[1]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid))
print("\nTransfer (Transaction):\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nBulkPoARegistered (Event):")
for elem in appcoins_tracker_contract.events.BulkPoARegistered().processReceipt(receipt):
    print(" - event: {}".format(elem))

print("\n###### END: BULK REGISTER POA MULTIPLE CAMPAIGNS ######")
###### END: BULK REGISTER POA MULTIPLE CAMPAIGNS ######

###### INFORM MULTIPLE OFFCHAIN BUY ######
print("\n\n###### INFORM MULTIPLE OFFCHAIN BUY ######")
print_balances_appcoins()

off_chain_buys = [(web3.eth.accounts[0],txid),(web3.eth.accounts[1],txid)]

tx_params = appcoins_tracker_contract.functions.informOffChainBuys(off_chain_buys)\
    .buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))
print("TXID: {}".format(txid))
print("\nOffChainBuy (Transaction):\n{}".format(web3.eth.getTransaction(txid)))

receipt = web3.eth.getTransactionReceipt(txid)
print("\nOffChainBuy (Event):\n{}")
for elem in appcoins_tracker_contract.events.OffChainBuy().processReceipt(receipt):
    print(" - event: {}".format(elem))

print_balances_appcoins()
print("\n###### END: INFORM MULTIPLE OFFCHAIN BUY ######")
###### END: INFORM MULTIPLE OFFCHAIN BUY ######

print_balances_ether()

print_balances_appcoins()


