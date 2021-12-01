// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// Create interface to use the functions of the Main Contract
interface iFrigginEggs {
    function tokensOfOwner(address owner)
        external
        view
        returns (uint256[] memory);
}

contract Yolk is ERC20, Ownable {
    iFrigginEggs public FrigginEggs; // Create the interface

    uint256 public constant BASE_RATE = 1 ether; // 10 $YOLK per day per Friggin Egg
    uint256 public START; // time of launch (used to calculate reward)
    bool public rewardPaused = true; // By default, stop the reward when deploying

    mapping(address => uint256) public rewards;
    mapping(address => uint256) public lastUpdate;

    mapping(address => bool) public allowedAddresses;

    // Link the address o the main contract when deploying
    constructor(address FrigginEggsAddress) ERC20("Yolk", "YOLK") {
        FrigginEggs = iFrigginEggs(FrigginEggsAddress); // initialize the interface when deploying
        START = 0; // initialize the time of START
    }

    // Function for the FrigginEggs and allowed addresses to use to update rewards
    function updateReward(address from, address to) external {
        require(
            allowedAddresses[msg.sender] || msg.sender == address(FrigginEggs),
            "You do not have permission to call this function"
        );
        if (from != address(0)) {
            rewards[from] += getPendingReward(from);
            lastUpdate[from] = block.timestamp;
        }
        if (to != address(0)) {
            rewards[to] += getPendingReward(to);
            lastUpdate[to] = block.timestamp;
        }
    }

    // Function to call to claim your reward
    function claimReward() external {
        require(!rewardPaused, "Claiming reward has been paused");
        require(
            FrigginEggs.tokensOfOwner(msg.sender).length > 0,
            "You need to own a Friggin Egg to claim $YOLK"
        );
        // First Claim: number of NFT * BASE_RATE
        if (lastUpdate[msg.sender] != 0) {
            _mint(
                msg.sender,
                rewards[msg.sender] + getPendingReward(msg.sender)
            );
        } else {
            _mint(
                msg.sender,
                FrigginEggs.tokensOfOwner(msg.sender).length * BASE_RATE
            );
        }
        rewards[msg.sender] = 0;
        lastUpdate[msg.sender] = block.timestamp;
    }

    // Allowed addresses can send tokens to a specified address
    function claimLaboratoryExperimentRewards(address _address, uint256 _amount)
        external
    {
        require(!rewardPaused, "Claiming reward has been paused");
        require(
            allowedAddresses[msg.sender],
            "Address does not have permission to distrubute tokens"
        );
        _mint(_address, _amount);
    }

    // Burn function for allowed addresses
    function burn(address user, uint256 amount) external {
        require(
            allowedAddresses[msg.sender] || msg.sender == address(FrigginEggs),
            "Address does not have permission to burn"
        );
        _burn(user, amount);
    }

    // View claimable amount
    function viewtTotalClaimable(address user) external view returns (uint256) {
        return rewards[user] + getPendingReward(user);
    }

    // function used by claimReward() to get the amount of token based on BASE_RATE and last time the user claimed a reward
    function getPendingReward(address user) internal view returns (uint256) {
        return
            (FrigginEggs.tokensOfOwner(user).length *
                BASE_RATE *
                (block.timestamp -
                    (lastUpdate[user] >= START ? lastUpdate[user] : START))) /
            86400;
        // return FrigginEggs.tokensOfOwner(user).length * BASE_RATE * (block.timestamp - lastUpdate[user]) / 86400;
    }

    // Define allowed addresses
    function setAllowedAddresses(address _address, bool _access)
        public
        onlyOwner
    {
        allowedAddresses[_address] = _access;
    }

    // Pause or Unpause The claimability
    function toggleReward() public onlyOwner {
        require(START != 0, "Use start Project to start the generation");
        rewardPaused = !rewardPaused;
    }

    // Function to start project and initialize starting time
    function startProject() public onlyOwner {
        require(rewardPaused != false, "Project has already started");
        rewardPaused = false;
        START = block.timestamp;
    }
}
