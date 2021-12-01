# The FrigginEggs NFTs

This is my own NFT Project of generative art, with full implementation of ERC-20, ERC-721 and ERC-1155 contracts, with solidity v0.8.

This repository includes all the contracts, the test implementation and generation of metadata, dummies and NFT images along with a cript to upload the metadata and images to IPFS (using Pinata).
Note that the "import" folder, containing all the base images, is not included.

## Requirements

- To run this project on your computer, be sure to complete the .env file
- You also need to have a set of images in the import folder, which follow the right tree structure (see the exemple)
- Be sure to run the scripts in the main directory (NFT_PROJECT) to keep the paths working.

## How to generate the images?

To create the images simply run the following command:

```console
PS C:\Users\USERNAME\Documents\NFT_Project> python scripts/NFT_Generation/generate_nft.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)