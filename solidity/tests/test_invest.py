from brownie import accounts, Wei


def test_investing_dai(dai, cdai, deployment, dai_tokens):
    # compund interaction deployment
    CI = deployment

    # transfer dai from accounts[0] to the CI contract
    dai.functions.transfer(str(CI.address), 10000).transact({'from': str(accounts[0])})

    # invest
    CI.invest({'from': accounts[0]})

    assert cdai.functions.balanceOf(str(accounts[0])).call() > 0 
