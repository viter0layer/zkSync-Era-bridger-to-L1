import random
import time
from web3 import Web3

'''
Нужно оставить на комиссию бриджа минимум 0.000175 ЕTH при 700к газ лимите
'''

min_amount_to_withdraw = 98 # = 98/100000 = 0.00098 ETH
max_amount_to_withdraw = 101 # = 101/100000 = 0.00101 ETH

eth_rpc = 'https://rpc.ankr.com/zksync_era'
web3 = Web3(Web3.HTTPProvider(eth_rpc))

def read_file(filename):
    result = []
    with open(filename, 'r') as file:
        for tmp in file.readlines():
            result.append(tmp.replace('\n', ''))

    return result


def write_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(f'{text}\n')


def bridge_to_l1(private):
    address = web3.eth.account.privateKeyToAccount(private).address

    tx = {
        "chainId": 324,
        "data": f"0x51cff8d9000000000000000000000000{address[2:]}",
        "from": address,
        "gas": 700000,
        "gasPrice": web3.eth.gasPrice,
        "nonce": web3.eth.getTransactionCount(address),
        "to": web3.toChecksumAddress("0x000000000000000000000000000000000000800a"),
        "value": web3.toWei(random.randint(min_amount_to_withdraw, max_amount_to_withdraw)/100000, 'ether')
    }

    tx_create = web3.eth.account.sign_transaction(tx, private)
    tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
    write_to_file('hashes.txt', tx_hash.hex())
    print(f"Transaction hash: {tx_hash.hex()}")


def main():
    privates = read_file('privates.txt')

    for private in privates:
        bridge_to_l1(private)
        time.sleep(random.randint(15, 22))


if __name__ == '__main__':
    main()
