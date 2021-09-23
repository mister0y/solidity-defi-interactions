from brownie import CompoundInteraction, accounts, network

def main():
    _dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    _cDai = "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643"
    _bat = "0x0d8775f648430679a709e98d2b0cb6250d2887ef"
    _cBat = "0x6c8c6b02e7b2be14d4fa6022dfd6d75921d90e4e"
    _comptroller = "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B"
    # requires brownie account to have been created
    if network.show_active() == 'development' or network.show_active() == 'mainnet-fork':
        CI = CompoundInteraction.deploy(
            _dai,
            _cDai,
            _bat,
            _cBat,
            _comptroller, 
            {'from': accounts[0]}
        )
    else: # ropsten
        acct = accounts.load('deploy')
        CI = CompoundInteraction.deploy(
            _dai,
            _cDai,
            _bat,
            _cBat,
            _comptroller, 
            {'from': acct}
        )
    return CI
