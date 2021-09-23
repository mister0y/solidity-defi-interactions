import pytest


def test_alice_not_bob(alice, bob):
    assert alice is not bob

def test_zero_balance(alice, tripool_lp_token):
    assert tripool_lp_token.balanceOf(alice) == 0

def test_non_zero_balance_after_staking(alice, tripool_lp_token, tripool_funded):
    assert tripool_lp_token.balanceOf(alice) > 0
