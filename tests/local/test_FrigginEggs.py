from scripts.helpful_scripts import get_account, get_contract, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import FrigginEggs, network, exceptions
import pytest
from web3 import Web3


def test_cannot_mint_when_paused():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    frigginEggs = get_contract(FrigginEggs, last=False, account=account)

    # Check if the contract is paused
    assert frigginEggs.projectStage() == 0

    # Try all the function requiring the contract not to be paused
    with pytest.raises(exceptions.VirtualMachineError) as e_info_1:
        frigginEggs.getPriceToMintOne()
    with pytest.raises(exceptions.VirtualMachineError) as e_info_2:
        frigginEggs.getPriceToMintThree()
    with pytest.raises(exceptions.VirtualMachineError) as e_info_3:
        frigginEggs.getPriceToMintTen()
    with pytest.raises(exceptions.VirtualMachineError) as e_info_4:
        frigginEggs.mintEggForFree(
            {"from": account, "value": Web3.toWei(1, "ether")})
    with pytest.raises(exceptions.VirtualMachineError) as e_info_5:
        frigginEggs.mintOneEgg(
            {"from": account, "value": Web3.toWei(1, "ether")})
    with pytest.raises(exceptions.VirtualMachineError) as e_info_6:
        frigginEggs.mintThreeEggs(
            {"from": account, "value": Web3.toWei(1, "ether")})
    with pytest.raises(exceptions.VirtualMachineError) as e_info_7:
        frigginEggs.mintTenEggs(
            {"from": account, "value": Web3.toWei(1, "ether")})


def test_cannot_mint_if_wrong_price():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    frigginEggs = get_contract(FrigginEggs, last=False, account=account)

    # First, change the project stage to Presales
    frigginEggs.changeToPreSales({"from": account})
    assert frigginEggs.projectStage() == 1

    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintOneEgg(
            {"from": account, "value": frigginEggs.getPriceToMintOne() - 1000})
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintThreeEggs(
            {"from": account, "value": frigginEggs.getPriceToMintThree() - 1000})
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintTenEggs(
            {"from": account, "value": frigginEggs.getPriceToMintTen() - 1000})

    frigginEggs.changeToMainSales({"from": account})
    assert frigginEggs.projectStage() == 2

    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintOneEgg(
            {"from": account, "value": frigginEggs.getPriceToMintOne() - 1000})
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintThreeEggs(
            {"from": account, "value": frigginEggs.getPriceToMintThree() - 1000})
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintTenEggs(
            {"from": account, "value": frigginEggs.getPriceToMintTen() - 1000})


def test_can_mint_if_right_price_presales():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    other_account = get_account(index=1)
    frigginEggs = get_contract(FrigginEggs, last=False, account=account)

    # First, change the project stage to Presales
    frigginEggs.changeToPreSales({"from": account})
    assert frigginEggs.projectStage() == 1

    frigginEggs.mintOneEgg(
        {"from": account, "value": frigginEggs.getPriceToMintOne()})
    assert frigginEggs.tokensOfOwner(account.address) == [0]

    frigginEggs.mintThreeEggs(
        {"from": account, "value": frigginEggs.getPriceToMintThree()})
    assert frigginEggs.tokensOfOwner(account.address) == [0, 1, 2, 3]

    frigginEggs.mintTenEggs(
        {"from": account, "value": frigginEggs.getPriceToMintTen()})
    assert frigginEggs.tokensOfOwner(account.address) == [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def test_can_mint_if_right_price_mainsales():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    other_account = get_account(index=1)
    frigginEggs = get_contract(FrigginEggs, last=False, account=account)

    # Change to MainSales
    frigginEggs.changeToMainSales({"from": account})
    assert frigginEggs.projectStage() == 2

    frigginEggs.mintOneEgg(
        {"from": other_account, "value": frigginEggs.getPriceToMintOne()})
    assert frigginEggs.tokensOfOwner(other_account.address) == [0]

    frigginEggs.mintThreeEggs(
        {"from": other_account, "value": frigginEggs.getPriceToMintThree()})
    assert frigginEggs.tokensOfOwner(other_account.address) == [0, 1, 2, 3]

    frigginEggs.mintTenEggs(
        {"from": other_account, "value": frigginEggs.getPriceToMintTen()})
    assert frigginEggs.tokensOfOwner(other_account.address) == [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def test_cannot_mint_more_than_account_limit():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    frigginEggs = get_contract(FrigginEggs, last=False, account=account)

    # First, change the project stage to Presales
    frigginEggs.changeToPreSales({"from": account})
    assert frigginEggs.projectStage() == 1

    frigginEggs.mintThreeEggs(
        {"from": account, "value": frigginEggs.getPriceToMintThree()})
    frigginEggs.mintThreeEggs(
        {"from": account, "value": frigginEggs.getPriceToMintThree()})
    assert frigginEggs.tokensOfOwner(account.address) == [0, 1, 2, 3, 4, 5]
    assert len(frigginEggs.tokensOfOwner(account.address)) == 6

    # Should not be able to mint another 10 (would result in more than 15 eggs in account)
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintTenEggs(
            {"from": account, "value": frigginEggs.getPriceToMintTen()})

    frigginEggs.mintThreeEggs(
        {"from": account, "value": frigginEggs.getPriceToMintThree()})
    frigginEggs.mintThreeEggs(
        {"from": account, "value": frigginEggs.getPriceToMintThree()})
    frigginEggs.mintOneEgg(
        {"from": account, "value": frigginEggs.getPriceToMintOne()})
    assert frigginEggs.tokensOfOwner(account.address) == [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert len(frigginEggs.tokensOfOwner(account.address)) == 13

    # Should not be able to mint another 3 (would result in more than 15 eggs in account)
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintThreeEggs(
            {"from": account, "value": frigginEggs.getPriceToMintThree()})

    frigginEggs.mintOneEgg(
        {"from": account, "value": frigginEggs.getPriceToMintOne()})
    frigginEggs.mintOneEgg(
        {"from": account, "value": frigginEggs.getPriceToMintOne()})
    assert frigginEggs.tokensOfOwner(account.address) == [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    assert len(frigginEggs.tokensOfOwner(account.address)) == 15

    # Should not be able to mint another 1 (would result in more than 15 eggs in account)
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintOneEgg(
            {"from": account, "value": frigginEggs.getPriceToMintOne()})


def test_cannot_mint_more_than_max_amount():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # MAX AMOUNT = 36 - 5 (reserve) = 31
    account = get_account()
    account_1 = get_account(index=1)
    account_2 = get_account(index=2)
    account_3 = get_account(index=3)
    frigginEggs = get_contract(FrigginEggs, last=False, account=account)

    frigginEggs.changeToPreSales({"from": account})
    assert frigginEggs.projectStage() == 1
    # Get 15 Eggs for first account
    frigginEggs.mintEggForFree(
        {"from": account})
    frigginEggs.mintOneEgg(
        {"from": account, "value": frigginEggs.getPriceToMintOne()})
    frigginEggs.mintThreeEggs(
        {"from": account, "value": frigginEggs.getPriceToMintThree()})
    frigginEggs.mintTenEggs(
        {"from": account, "value": frigginEggs.getPriceToMintTen()})
    assert len(frigginEggs.tokensOfOwner(account.address)) == 15

    # Get 15 Eggs for second account
    frigginEggs.mintEggForFree(
        {"from": account_1})
    frigginEggs.mintOneEgg(
        {"from": account_1, "value": frigginEggs.getPriceToMintOne()})
    frigginEggs.mintThreeEggs(
        {"from": account_1, "value": frigginEggs.getPriceToMintThree()})
    frigginEggs.mintTenEggs(
        {"from": account_1, "value": frigginEggs.getPriceToMintTen()})
    assert len(frigginEggs.tokensOfOwner(account.address)) == 15

    # Get 1 Egg for next account
    frigginEggs.mintEggForFree(
        {"from": account_2})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.mintOneEgg(
            {"from": account_2, "value": frigginEggs.getPriceToMintOne()})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.mintThreeEggs(
            {"from": account_2, "value": frigginEggs.getPriceToMintThree()})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.mintTenEggs(
            {"from": account_2, "value": frigginEggs.getPriceToMintTen()})

    # Test limit with free egg too:
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.mintEggForFree({"from": account_3})


def test_cannot_get_free_egg_if_already_own_one():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    account_1 = get_account(index=1)
    account_2 = get_account(index=2)
    frigginEggs = get_contract(FrigginEggs, last=False, account=account)

    # First, change the project stage to Presales
    frigginEggs.changeToPreSales({"from": account})
    assert frigginEggs.projectStage() == 1

    frigginEggs.mintEggForFree({"from": account})
    assert frigginEggs.tokensOfOwner(account.address) == [0]
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintEggForFree({"from": account})

    frigginEggs.mintOneEgg(
        {"from": account_1, "value": frigginEggs.getPriceToMintOne()})
    assert frigginEggs.tokensOfOwner(account_1.address) == [1]
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintEggForFree({"from": account_1})

    # Change the project stage to mainSales
    frigginEggs.changeToMainSales({"from": account})
    assert frigginEggs.projectStage() == 2

    frigginEggs.mintEggForFree({"from": account_2})
    assert frigginEggs.tokensOfOwner(account_2.address) == [2]
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.mintEggForFree({"from": account_2})


def test_onlyOwner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    owner = get_account()
    other_account = get_account(index=1)
    random_account = get_account(index=2)
    frigginEggs = get_contract(FrigginEggs, last=False, account=owner)

    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.setBaseURI("weogjb", {"from": other_account})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.setExtensionURI("wpegn", {"from": other_account})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.reserveFrig(random_account.address,
                                2, {"from": other_account})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.pauseProject({"from": other_account})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.changeToPreSales({"from": other_account})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.changeToMainSales({"from": other_account})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.withdrawAll({"from": other_account})

    # Change to presale, to mint one and try to change its URI with other_account
    frigginEggs.changeToPreSales({"from": owner})
    assert frigginEggs.projectStage() == 1
    frigginEggs.mintEggForFree({"from": other_account})
    assert frigginEggs.tokensOfOwner(other_account.address) == [0]
    with pytest.raises(exceptions.VirtualMachineError) as e_info:
        frigginEggs.setTokenURI(0, "woejgbwljegb", {"from": other_account})


def test_can_modify_name_and_description():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    owner = get_account()
    other_account = get_account(index=1)
    frigginEggs = get_contract(FrigginEggs, last=False, account=owner)

    frigginEggs.changeToPreSales({"from": owner})
    assert frigginEggs.projectStage() == 1

    frigginEggs.mintEggForFree({"from": other_account})
    assert frigginEggs.tokensOfOwner(other_account.address) == [0]

    # check that other accounts cannot edit names or description
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.changeName(0, "NEW NAME", {"from": owner})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.changeDescription(0, "NEW DESCRIPTION", {"from": owner})

    # Now change the name and description
    frigginEggs.changeName(0, "NEW NAME", {"from": other_account})
    frigginEggs.changeDescription(
        0, "NEW DESCRIPTION", {"from": other_account})
    assert frigginEggs.FrigNames(0) == "NEW NAME"
    assert frigginEggs.FrigDescriptions(0) == "NEW DESCRIPTION"


def test_edit_tokenURI():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    owner = get_account()
    other_account = get_account(index=1)
    frigginEggs = get_contract(FrigginEggs, last=False, account=owner)

    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.setExtensionURI("_EXTENSION", {"from": other_account})
    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.setBaseURI("BASE_URI_", {"from": other_account})

    # Should not be able to get token URI is no eggs have been minted
    with pytest.raises(exceptions.VirtualMachineError):
        token_uri_0 = frigginEggs.tokenURI(0)

    # Mint some Eggs:
    frigginEggs.changeToMainSales({"from": owner})
    frigginEggs.mintEggForFree({"from": owner})
    frigginEggs.mintEggForFree({"from": other_account})

    # Since no base_URI nor extension are set, return token_uri if it is set, or the id otherwise (here it's empty)
    assert frigginEggs.tokenURI(0) == "0"
    assert frigginEggs.tokenURI(1) == "1"

    frigginEggs.setTokenURI(1, "TOKEN_URI", {"from": owner})
    assert frigginEggs.tokenURI(0) == "0"
    assert frigginEggs.tokenURI(1) == "TOKEN_URI"

    # Now set a base_URI, should result in baseURI + tokenURI
    frigginEggs.setBaseURI("BASE_URI_", {"from": owner})
    assert frigginEggs.tokenURI(0) == "BASE_URI_0"
    assert frigginEggs.tokenURI(1) == "BASE_URI_TOKEN_URI"

    # Now set an extension and  base_URI, should result in baseURI + tokenURI + extension
    frigginEggs.setExtensionURI("_EXTENSION", {"from": owner})
    assert frigginEggs.tokenURI(0) == "BASE_URI_0_EXTENSION"
    assert frigginEggs.tokenURI(1) == "BASE_URI_TOKEN_URI_EXTENSION"

    # Now reset the baseURI, should result in tokenURIs + extension
    frigginEggs.setBaseURI("", {"from": owner})
    assert frigginEggs.tokenURI(0) == "0_EXTENSION"
    assert frigginEggs.tokenURI(1) == "TOKEN_URI_EXTENSION"

    # Now reset the tokenURI, should result in id + extension
    frigginEggs.setTokenURI(1, "", {"from": owner})
    assert frigginEggs.tokenURI(0) == "0_EXTENSION"
    assert frigginEggs.tokenURI(1) == "1_EXTENSION"

    # Now reset the extension, should result in just the id
    frigginEggs.setExtensionURI("", {"from": owner})
    assert frigginEggs.tokenURI(0) == "0"
    assert frigginEggs.tokenURI(1) == "1"


def test_free_eggs_limit():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    free_eggs_amount = 5
    accounts = [get_account(index=i) for i in range(free_eggs_amount + 1)]
    frigginEggs = get_contract(FrigginEggs, last=False, account=accounts[0])
    frigginEggs.changeToMainSales({"from": accounts[0]})

    for i in range(free_eggs_amount):
        frigginEggs.mintEggForFree({"from": accounts[i]})
        assert frigginEggs.tokensOfOwner(accounts[i].address) == [i]

    with pytest.raises(exceptions.VirtualMachineError):
        frigginEggs.mintEggForFree({"from": accounts[-1]})
