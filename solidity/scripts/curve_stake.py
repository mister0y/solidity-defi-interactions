from typing_extensions import Protocol
from brownie import Contract, accounts, interface
from brownie_tokens import MintableForkToken


# Sometimes Contract is not working, in that case load it from etherscan. Use this function:
def load_contract(addr):
    try:
        cont = Contract(addr)
    except ValueError:
        cont = Contract.from_explorer(addr)
    return cont 

def main():
    dai_addr = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    usdc_addr = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    curve_addr = "0x0000000022D53366457F9d5E68Ec105046FC4383"

    amount = 100000 * 10 ** 18
    dai = MintableForkToken(dai_addr)

    dai._mint_for_testing(accounts[0], amount)

    curve = load_contract(curve_addr)
    curve_registry_addr = curve.get_registry()
    print(f"Registry address: {curve_registry_addr}")
    registry = load_contract(curve_registry_addr)
    pool_addr = registry.find_pool_for_coins(dai_addr, usdc_addr)
    pool = load_contract(pool_addr)

    dai.approve(pool_addr, amount, {'from': accounts[0]})
    pool.add_liquidity([amount, 0, 0], 0, {'from': accounts[0]})

    gauge_info = registry.get_gauges(pool_addr)
    gauge_addr = gauge_info[0][0]

    # OLD
    # gauge_contract = interface.LiquidityGauge(gauge_addr)

    # NEW
    gauge_contract = load_contract(gauge_addr)

    lp_token = MintableForkToken(gauge_contract.lp_token())
    lp_token.approve(gauge_addr, amount, {'from': accounts[0]})
    gauge_contract.deposit(lp_token.balanceOf(accounts[0]), {'from': accounts[0]})








