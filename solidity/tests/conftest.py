import pytest
from brownie import accounts, Contract, ZERO_ADDRESS
from brownie_tokens import MintableForkToken


def load_contract(addr):
    if addr == ZERO_ADDRESS:
        return None
    try:
        cont = Contract(addr)
    except ValueError:
        cont = Contract.from_explorer(addr)
    return cont 

@pytest.fixture(autouse=True)
def setup(fn_isolation):
    """
    Isolation setup fixture.
    This ensures that each test runs against the same base environment.
    """
    pass

@pytest.fixture(scope="module")
def alice():
    return accounts[0]

@pytest.fixture(scope="module")
def bob():
    return accounts[1]

@pytest.fixture(scope="module")
def registry():
    return load_contract("0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5")

@pytest.fixture(scope="module")
def tripool(registry):
    return load_contract(registry.pool_list(0))

@pytest.fixture(scope="module")
def tripool_lp_token(registry, tripool):
    return registry.get_lp_token(tripool)

@pytest.fixture(scope="module")
def tripool_funded(registry, tripool, alice):
    dai_addr = registry.get_coins(tripool)[0]
    dai = MintableForkToken(dai_addr)
    amount = 1000 * 10 ** 18
    dai._mint_for_testing(alice, amount)
    dai.approve(tripool, amount, {'from': alice})
    tripool.add_liquidity([amount, 0, 0], 0, {'from': alice})
    return tripool

