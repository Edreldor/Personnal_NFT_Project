// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract FrigginEggs is ERC721Enumerable, Ownable {
    using Strings for uint256;

    // Optional mapping for token URIs
    mapping(uint256 => string) private _tokenURIs;
    string baseURI;
    string public extensionURI;

    enum STAGES {
        PAUSED,
        PRESALES,
        MAIN
    }

    // Define names and description for each Token: People can edit them and it will be implemented in the metadata
    mapping(uint256 => string) public FrigNames;
    mapping(uint256 => string) public FrigDescriptions;

    // Define the different prices for the different stages
    uint256 private constant FrigPrice_PreSale = 0.04 ether; // PreSale Price : 0.04 ETH
    uint256 private constant ThreeFrigPrice_PreSale = 0.108 ether; // PreSale Price : 0.108 ETH for 3
    uint256 private constant TenFrigPrice_PreSale = 0.32 ether; // PreSale Price : 0.32 ETH for 10

    uint256 private constant FrigPrice_MainSale = 0.05 ether; // PreSale Price : 0.05 ETH
    uint256 private constant ThreeFrigPrice_MainSale = 0.135 ether; // PreSale Price : 0.135 ETH for 3
    uint256 private constant TenFrigPrice_MainSale = 0.4 ether; // PreSale Price : 0.40 ETH for 10

    uint256 constant MaxEggPerAccount = 15; // Maximum number of Eggs to mint per account
    uint256 private FrigReserve = 5; // Number of Eggs for giveaways and contests
    uint256 private FrigFreeMint = 5; // Number of Eggs available to mint for free

    uint256 private MAX_Frig = 36;

    STAGES public projectStage;

    // addresses of the Team Member
    address constant T = 0x1f2A9EC7f7b2dC4491E0206c65E8aB8F4B4c3c3f;
    address constant K = 0x8f2EB78F0895bc4f93B6e65462Cb2458035ee817;
    address constant M = 0x4C11FA301e246A32C4276B38be2bB689c0BA4bac;
    address constant F = 0xdcE642cC913d21A2eE3c67CBd63c22A00A20Cd5f;
    //community wallet
    address constant C = 0x2e70F672A7F9D9f45Cf622965303EAb428B6Df04;

    constructor() ERC721("FrigginEggs", "EGGS") {
        projectStage = STAGES.PAUSED;
    }

    /**
     * SET THE DIFFERENT REQUIREMENTS FOR OUR TOKEN METADATA HANDLING
     */
    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }

    function setBaseURI(string memory baseURI_) public onlyOwner {
        baseURI = baseURI_;
    }

    function _extensionURI() internal view virtual returns (string memory) {
        return extensionURI;
    }

    function setExtensionURI(string memory extensionURI_) public onlyOwner {
        extensionURI = extensionURI_;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(
            _exists(tokenId),
            "ERC721URIStorage: URI query for nonexistent token"
        );

        string memory _tokenURI = _tokenURIs[tokenId];

        if (bytes(_tokenURI).length == 0) {
            _tokenURI = tokenId.toString();
        }

        string memory base = _baseURI();
        string memory extension = _extensionURI();

        // If there is no base nor extension URI, return the token URI.
        if (bytes(base).length == 0 && bytes(extension).length == 0) {
            return _tokenURI;
        }
        // If only extension is set, concatenate the tokenURI and extensionURI (via abi.encodePacked).
        if (bytes(base).length == 0 && bytes(extension).length > 0) {
            return string(abi.encodePacked(_tokenURI, extension));
        }
        // If only base is set, concatenate the tokenURI and baseURI (via abi.encodePacked).
        if (bytes(base).length > 0 && bytes(extension).length == 0) {
            return string(abi.encodePacked(base, _tokenURI));
        }
        // If all are set, concatenate the baseURI, tokenURI and extensionURI (via abi.encodePacked).
        if (bytes(_tokenURI).length > 0) {
            return
                string(
                    abi.encodePacked(
                        string(abi.encodePacked(base, _tokenURI)),
                        extension
                    )
                );
        }
        return super.tokenURI(tokenId);
    }

    /**
     * @dev Sets `_tokenURI` as the tokenURI of `tokenId`.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     */
    function setTokenURI(uint256 tokenId, string memory _tokenURI)
        public
        onlyOwner
    {
        require(
            _exists(tokenId),
            "ERC721URIStorage: URI set of nonexistent token"
        );
        _tokenURIs[tokenId] = _tokenURI;
    }

    /**
     * @dev Destroys `tokenId`.
     * The approval is cleared when the token is burned.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     *
     * Emits a {Transfer} event.
     */
    function _burn(uint256 tokenId) internal virtual override {
        super._burn(tokenId);

        if (bytes(_tokenURIs[tokenId]).length != 0) {
            delete _tokenURIs[tokenId];
        }
    }

    //** END OF METADATA HANDLING */

    // Function for the team to send The FrigginEggs to winners of Giveaway
    function reserveFrig(address _to, uint256 _reserveAmount) public onlyOwner {
        uint256 supply = totalSupply();
        require(
            _reserveAmount > 0 && _reserveAmount <= FrigReserve,
            "Not enough eggs left in the reserve"
        );
        for (uint256 i = 0; i < _reserveAmount; i++) {
            _safeMint(_to, supply + i);
        }
        FrigReserve = FrigReserve - 1;
    }

    // Functions to change state of contract
    function pauseProject() public onlyOwner {
        projectStage = STAGES.PAUSED;
    }

    function changeToPreSales() public onlyOwner {
        projectStage = STAGES.PRESALES;
    }

    function changeToMainSales() public onlyOwner {
        projectStage = STAGES.MAIN;
    }

    // Function to get all tokens of a wallet (array uint256[])
    function tokensOfOwner(address _owner)
        external
        view
        returns (uint256[] memory)
    {
        uint256 tokenCount = balanceOf(_owner);
        if (tokenCount != 0) {
            uint256[] memory result = new uint256[](tokenCount);
            uint256 index;
            for (index = 0; index < tokenCount; index++) {
                result[index] = tokenOfOwnerByIndex(_owner, index);
            }
            return result;
        } else {
            // Return an empty array
            return new uint256[](0);
        }
    }

    // Function to edit the name of your Friggin Egg (Free)
    function changeName(uint256 _id, string memory FrigginName) public {
        require(ownerOf(_id) == msg.sender, "You do not own this FrigginEgg");
        FrigNames[_id] = FrigginName;
    }

    // Function to edit the description of your Friggin Egg (Free)
    function changeDescription(uint256 _id, string memory FrigginDescription)
        public
    {
        require(ownerOf(_id) == msg.sender, "You do not own this FrigginEgg");
        FrigDescriptions[_id] = FrigginDescription;
    }

    // Function to get the prices
    function getPriceToMintOne() public view returns (uint256) {
        require(
            projectStage != STAGES.PAUSED,
            "Sale must be active to get the price"
        );
        if (projectStage == STAGES.PRESALES) {
            return (FrigPrice_PreSale);
        }
        if (projectStage == STAGES.MAIN) {
            return (FrigPrice_MainSale);
        }
        return (ThreeFrigPrice_MainSale);
    }

    function getPriceToMintThree() public view returns (uint256) {
        require(
            projectStage != STAGES.PAUSED,
            "Sale must be active to get the price"
        );
        if (projectStage == STAGES.PRESALES) {
            return (ThreeFrigPrice_PreSale);
        }
        if (projectStage == STAGES.MAIN) {
            return (ThreeFrigPrice_MainSale);
        }
        return (ThreeFrigPrice_MainSale);
    }

    function getPriceToMintTen() public view returns (uint256) {
        require(
            projectStage != STAGES.PAUSED,
            "Sale must be active to get the price"
        );
        if (projectStage == STAGES.PRESALES) {
            return (TenFrigPrice_PreSale);
        }
        if (projectStage == STAGES.MAIN) {
            return (TenFrigPrice_MainSale);
        }
        return (ThreeFrigPrice_MainSale);
    }

    // MINT FUNCTIONS
    function _mintFrig(uint256 numberOfTokens, address sender) internal {
        uint256 initialIndex = totalSupply();
        for (uint256 i = 0; i < numberOfTokens; i++) {
            _safeMint(sender, initialIndex + i);
        }
    }

    function mintOneEgg() public payable {
        require(
            projectStage != STAGES.PAUSED,
            "Sale must be active to mint eggs"
        );
        require(
            totalSupply() + 1 <= MAX_Frig - FrigReserve,
            "Not enough Friggin Eggs for this amount mate"
        );
        require(
            balanceOf(msg.sender) < MaxEggPerAccount,
            "You reached the maximum amount for minting"
        );
        require(getPriceToMintOne() <= msg.value, "Incorrect amount of Ether");

        _mintFrig(1, msg.sender);
    }

    // Function to Mint a Free EGG -> NEED TO HAVE A TOTAL OF 0 EGGS TO CLAIM (only 1000 free eggs)
    function mintEggForFree() public {
        require(
            projectStage != STAGES.PAUSED,
            "Sale must be active to mint Free eggs"
        );
        require(FrigFreeMint >= 1, "No more Free Eggs available");
        require(totalSupply() + 1 <= MAX_Frig - FrigReserve);
        require(balanceOf(msg.sender) == 0, "You already have a Friggin Egg");

        _safeMint(msg.sender, totalSupply());
        FrigFreeMint = FrigFreeMint - 1;
    }

    function mintThreeEggs() public payable {
        require(
            projectStage != STAGES.PAUSED,
            "Sale must be active to mint eggs"
        );
        require(
            totalSupply() + 3 <= MAX_Frig - FrigReserve,
            "Not enough Friggin Eggs for this amount mate"
        );
        require(
            balanceOf(msg.sender) < MaxEggPerAccount - 2,
            "You reached the maximum amount for minting"
        );
        require(
            getPriceToMintThree() <= msg.value,
            "Incorrect amount of Ether"
        );

        _mintFrig(3, msg.sender);
    }

    function mintTenEggs() public payable {
        require(
            projectStage != STAGES.PAUSED,
            "Sale must be active to mint eggs"
        );
        require(
            totalSupply() + 10 <= MAX_Frig - FrigReserve,
            "Not enough Friggin Eggs for this amount mate"
        );
        require(
            balanceOf(msg.sender) < MaxEggPerAccount - 9,
            "You reached the maximum amount for minting"
        );
        require(getPriceToMintTen() <= msg.value, "Incorrect amount of Ether");

        _mintFrig(10, msg.sender);
    }

    // 4% will go to the community wallet, withdraw function
    function withdrawAll() public payable onlyOwner {
        uint256 _each = (address(this).balance * 29) / 100;
        uint256 _toF = (address(this).balance * 9) / 100;
        require(payable(T).send(_each));
        require(payable(K).send(_each));
        require(payable(M).send(_each));
        require(payable(F).send(_toF));
        uint256 balance = address(this).balance;
        require(payable(C).send(balance));
    }
}
