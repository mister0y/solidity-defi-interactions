# Don't use this! Use MintableForkToken instead.

from brownie import accounts, interface
from web3 import Web3, HTTPProvider

# first run ganache-cli with a public dai address with a large balance to unlock
# ganache-cli -f https://mainnet.infura.io/v3/b8b129de56014e2dbeeb06546f9b0ce1 -u 0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549


def transfer_dai_to_own_account():
    w3 = Web3(HTTPProvider('http://127.0.0.1:8545'))

    contract_address_dai = '0x6B175474E89094C44Da98b954EedeAC495271d0F' # DAI contract address
    # DAI ABI
    contract_instance_dai = interface.dai(contract_address_dai)
    unlocked_account = '0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549' # Unlocked account with DAI and ETH

    print(f"balance big user before is: {contract_instance_dai.balanceOf(unlocked_account)}")

    contract_instance_dai.transfer(accounts[0], 10000, {'from': unlocked_account})

    print(f"balance big user after is: {contract_instance_dai.balanceOf(unlocked_account)}")
    print(f"balance accounts[0]: {contract_instance_dai.balanceOf(accounts[0])}")

def main():
    transfer_dai_to_own_account()


