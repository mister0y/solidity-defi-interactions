from brownie import Contract, accounts, run
from brownie_tokens import MintableForkToken

def main():
    _dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    _cDai = "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643"
    _bat = "0x0d8775f648430679a709e98d2b0cb6250d2887ef"
    _cBat = "0x6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e"
    _comptroller = "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B"

    amount = 10000
    dai = MintableForkToken(_dai)
    cdai = MintableForkToken(_cDai)
    dai._mint_for_testing(accounts[0], amount)

    CI = run('deploy')

    print(f"dai balance accounts 0: {dai.balanceOf(accounts[0])}")

    print("transferring dai to contract")
    dai.transfer(CI.address, 10000, {'from': accounts[0]})

    print(f"dai balance accounts 0: {dai.balanceOf(accounts[0])}")
    print(f"dai balance contract: {dai.balanceOf(CI.address)}")

    print("ptting dai in Compound")
    CI.invest()

    print(f"dai balance contract: {dai.balanceOf(CI.address)}")
    print(f"cdai balance contract: {cdai.balanceOf(CI.address)}")





    