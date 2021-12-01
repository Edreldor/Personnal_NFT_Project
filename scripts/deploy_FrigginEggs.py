from brownie import FrigginEggs
from scripts.helpful_scripts import get_account, get_contract


def main():
    account = get_account()
    frigginEggs_contract = get_contract(
        FrigginEggs, last=False, account=account)
