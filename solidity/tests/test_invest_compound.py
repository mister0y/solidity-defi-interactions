from brownie import accounts, Contract, run
from brownie_tokens import MintableForkToken


def load_contract(addr):
    try:
        cont = Contract(addr)
    except ValueError:
        cont = Contract.from_explorer(addr)
    return cont 


def test_investing_dai(deployment):
    _dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    _cDai = "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643"

    # compund interaction deployment
    CI = run('deploy')

    # transfer dai from accounts[0] to the CI contract
    dai = MintableForkToken(_dai)
    dai._mint_for_testing(accounts[0], 10000)

    cdai = Contract(_cDai)

    # invest
    CI.invest({'from': accounts[0]})

    assert cdai.balanceOf(accounts[0]).call() > 0 
