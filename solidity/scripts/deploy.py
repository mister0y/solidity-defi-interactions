from brownie import CompoundInteraction, accounts, network


dai = "0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa"
cDai = "0xF0d0EB522cfa50B716B3b1604C4F0fA6f04376AD"
bat = "0x482dC9bB08111CB875109B075A40881E48aE02Cd"
cBat = "0x4a77fAeE9650b09849Ff459eA1476eaB01606C7a"
comptroller = "0x5eAe89DC1C671724A672ff0630122ee834098657"

def main():
    # requires brownie account to have been created
    if network.show_active()=='development':
        CI = CompoundInteraction.deploy(
            dai,
            cDai,
            bat,
            cBat,
            comptroller, 
            {'from': accounts[0]}
        )


