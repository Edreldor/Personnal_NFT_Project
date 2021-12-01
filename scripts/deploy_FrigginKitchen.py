from brownie import FrigginKitchen
from scripts.helpful_scripts import get_account, get_contract


def main():
    account = get_account()
    frigginEggs_contract = get_contract(
        FrigginKitchen, last=False, account=account)
