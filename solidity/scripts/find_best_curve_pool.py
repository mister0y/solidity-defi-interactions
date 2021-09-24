from brownie import accounts, chain, Contract, ZERO_ADDRESS
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

def run_operations(_pool, _pool_index, tripool_lp):
    # Take a chain snapshot
    chain.snapshot()

    # Ape into pool
    ape(_pool, _pool_index, tripool_lp)

    # Skip forward one day
    chain.mine(timedelta=60*60*24)

    # Check Curve balance
    _val = calc_curve_value()
    _name = registry.get_pool_name(_pool)

    # Revert
    chain.revert()
    return _name, _val
        
def ape(pool, pool_index, tripool_lp):
    # Approve deposit from Tripool into Metapool
    tripool_bal = tripool_lp.balanceOf(whale)
    tripool_lp.approve(pool, tripool_bal, {'from': whale})

    # Add Liquidity
    amounts = [0] * registry.get_n_coins(pool)[0]
    amounts[pool_index] = tripool_bal
    pool.add_liquidity(amounts, 0, {'from': whale})

    # Check if the pool has a gauge
    gauge_addr = registry.get_gauges(pool)[0][0]
    if gauge_addr == ZERO_ADDRESS:
        return

    # Create Approval for the rewards pool
    pool_lp = load_contract(registry.get_lp_token(pool))
    pool_bal = pool_lp.balanceOf(whale)
    if pool_lp.allowance(whale, gauge_addr) < pool_bal:
        pool_lp.approve(gauge_addr, pool_bal, {'from': whale})

    # Make a Deposit
    gauge = load_contract(gauge_addr)
    gauge.deposit(pool_bal, {'from': whale})

def calc_curve_value():
    # Get initial value
    init_val = calc_balance()

    # Set CRV claim array
    crv_pools = [ZERO_ADDRESS] * 8
    j = 0
    for i in range(registry.pool_count()):
        # Check if gauge exists
        _addr = registry.get_gauges(registry.pool_list(i))[0][0]
        if _addr == ZERO_ADDRESS:
            continue

        # Add guage to claim if balance
        _gauge = load_contract(_addr)
        if _gauge.balanceOf(whale) > 0 and j < 8:
            crv_pools[j] = _addr
            j += 1

    # Mint many
    minter.mint_many(crv_pools, {'from': whale})
        
    # Calculate our Balance
    final_val = calc_balance()

    # Undo Mint Many
    chain.undo()
    return final_val - init_val

def calc_balance():
    return crv.balanceOf(whale) / 10 ** crv.decimals()

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

