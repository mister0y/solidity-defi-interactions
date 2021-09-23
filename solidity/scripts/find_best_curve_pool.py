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

whale = accounts[0]
registry = load_contract("0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5")
minter = load_contract("0xd061D61a4d941c39E5453435B6345Dc261C2fcE0")
crv = load_contract(minter.token())

def main():
    # Check initial value
    strategy = {}
    init_value = calc_curve_value()
    strategy['init'] = init_value
    print(f"initally {init_value}")

    # Assign DAI to Tripool
    tripool = add_tripool_liquidity()
    tripool_lp = registry.get_lp_token(tripool)

    # Loop through all pools that accept Tripool
    for i in range(registry.pool_count()):
        _pool_addr = registry.pool_list(i)
        _pool = load_contract(_pool_addr)
        for _pool_index in range(registry.get_n_coins(_pool)[0]):
            if _pool.coins(_pool_index) == tripool_lp:
                _name, _val = run_operations(
                    _pool,
                    _pool_index,
                    load_contract(tripool_lp),
                )
                strategy[_name] = _val
                print(f"{_name}: {_val}")
    
    # Print strategy summary
    for key, value in sorted(
        strategy.items(),
        key=lambda item: -item[1]
    ):
        print(key, value)
        

def add_tripool_liquidity():
    dai_addr = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    usdc_addr = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    curve_addr = "0x0000000022D53366457F9d5E68Ec105046FC4383"

    amount = 100000 * 10 ** 18
    dai = MintableForkToken(dai_addr)

    dai._mint_for_testing(whale, amount)

    pool_addr = registry.find_pool_for_coins(dai_addr, usdc_addr)
    pool = load_contract(pool_addr)

    dai.approve(pool_addr, amount, {'from': whale})
    pool.add_liquidity([amount, 0, 0], 0, {'from': whale})

    return pool

