from brownie import accounts


def test_investing_dai(dai, cdai, deployment, dai_tokens):
    # compund interaction deployment
    CI = deployment

    # transfer dai from accounts[0] to the CI contract
    dai.functions.transfer(str(CI.address), 10000).transact({'from': str(accounts[0])})

    # invest
    mint_result = CI.invest()

    assert False