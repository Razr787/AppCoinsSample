from json import loads

from web3 import Web3, HTTPProvider
from contract_adress import ContractAdress

web3 = Web3(HTTPProvider("http://127.0.0.1:8545", request_kwargs={"timeout": 60}))


def get_params(sender):
    return {"from": sender, "gasPrice": web3.eth.gasPrice, "gas": 6721975,
            "nonce": web3.eth.getTransactionCount(sender)}

# Read HelloWorld Contract
with open("build/contracts/AppCoinsIAB.json", "r") as f_handler:
    contract_info = loads(f_handler.read())
    f_handler.close()

# Get HelloWorld Contract
helloworld_contract = web3.eth.contract(ContractAdress.APPCOINS.value, abi=contract_info["abi"])

user = ["hello", 10]
tx_params = helloworld_contract.functions.doNothing().buildTransaction(get_params(web3.eth.accounts[0]))
txid = Web3.toHex(web3.eth.sendTransaction(tx_params))