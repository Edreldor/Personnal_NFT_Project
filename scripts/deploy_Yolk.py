from brownie import Yolk, FrigginEggs
from scripts.helpful_scripts import get_account, get_contract


def main():
    account = get_account()
    frigginEggs_contract = Yolk.deploy(get_contract(
        FrigginEggs, last=True, account=account), {"from": account})
