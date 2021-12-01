import requests
from typing import Union
import time


class OpenSea:
    '''
    A simple OpenSea object to connect to the OpenSea API
    '''

    def __init__(self, network, api_key=None):
        self.network = network
        self.baseURL = self.get_baseURI()
        if api_key:
            self.headers = {"X-API-KEY": str(api_key)}
        else:
            self.headers = api_key

    def get_baseURI(self):
        if self.network.lower() == "rinkeby":
            return "https://rinkeby-api.opensea.io/api/v1/"
        elif self.network.lower() == "mainnet":
            return "https://api.opensea.io/api/v1/"

    # Function to retrieve an asset from opensea with the desired filter parameters.
    def retrieve_asset(self, owner: Union[str, None] = None,
                       token_ids: Union[list, None] = None,
                       asset_contract_address: Union[str, None] = None,
                       asset_contract_addresses: Union[list, None] = None,
                       order_by: Union[str, None] = None,
                       order_direction: str = 'desc',
                       offset: int = 0,
                       limit: int = 20,
                       collection: Union[str, None] = None):
        '''
        owner - string
        The address of the owner of the assets

        token_ids - list of int
        An array of token IDs to search for (e.g. ?token_ids=1&token_ids=209). Will return a list of assets with token_id matching any of the IDs in this array.

        asset_contract_address - string
        The NFT contract address for the assets

        asset_contract_addresses - string
        An array of contract addresses to search for (e.g. ?asset_contract_addresses=0x1...&asset_contract_addresses=0x2...). Will return a list of assets with contracts matching any of the addresses in this array. If "token_ids" is also specified, then it will only return assets that match each (address, token_id) pairing, respecting order.

        order_by - string
        How to order the assets returned. By default, the API returns the fastest ordering. Options you can set are sale_date (the last sale's transaction's timestamp), sale_count (number of sales), and sale_price (the last sale's total_price)

        order_direction - string
        Can be 'asc' for ascending or 'desc' for descending

        offset - int
        Offset

        limit - int
        Limit. Defaults to 20, capped at 50.

        collection - string
        Limit responses to members of a collection. Case sensitive and must match the collection slug exactly. Will return all assets from all contracts in a collection. For more information on collections, see our collections documentation.
        '''
        parameters = {"owner": owner,
                      "token_ids": token_ids,
                      "asset_contract_address": asset_contract_address,
                      "asset_contract_addresses": asset_contract_addresses,
                      "order_by": order_by,
                      "order_direction": order_direction,
                      "offset": offset,
                      "limit": limit,
                      "collection": collection}
        endpoint = 'assets'
        base_url = self.baseURL + endpoint
        request_url = self._get_link_with_parameters(base_url, parameters)
        return requests.get(request_url, headers=self.headers)

    def retrieve_events(self, asset_contract_address: Union[str, None] = None,
                        collection_slug: Union[str, None] = None,
                        token_id: Union[int, None] = None,
                        account_address: Union[str, None] = None,
                        event_type: Union[str, None] = None,
                        only_opensea: bool = False,
                        auction_type: Union[str, None] = None,
                        offset: int = 0,
                        limit: str = 20,
                        occurred_before: Union[int, None] = None,
                        occurred_after: Union[int, None] = None):
        '''
        asset_contract_address
        The NFT contract address for the assets for which to show events

        collection_slug - string
        Limit responses to events from a collection. Case sensitive and must match the collection slug exactly. Will return all assets from all contracts in a collection. For more information on collections, see our collections documentation.

        token_id - int
        The token's id to optionally filter by

        account_address - string
        A user account's wallet address to filter for events on an account

        event_type
        string
        The event type to filter. Can be created for new auctions, successful for sales, cancelled, bid_entered, bid_withdrawn, transfer, or approve

        only_opensea - boolean
        Restrict to events on OpenSea auctions. Can be true or false

        auction_type - string
        Filter by an auction type. Can be english for English Auctions, dutch for fixed-price and declining-price sell orders (Dutch Auctions), or min-price for CryptoPunks bidding auctions.

        offset - int
        Offset for pagination

        limit - string
        Limit for pagination

        occurred_before - date-time [epoch]
        Only show events listed before this timestamp. Seconds since the Unix epoch.

        occurred_after - date-time [epoch]
        Only show events listed after this timestamp. Seconds since the Unix epoch.
        '''
        parameters = {"asset_contract_address": asset_contract_address,
                      "collection_slug": collection_slug,
                      "token_id": token_id,
                      "account_address": account_address,
                      "event_type": event_type,
                      "only_opensea": only_opensea,
                      "auction_type": auction_type,
                      "offset": offset,
                      "limit": limit,
                      "occurred_before": occurred_before,
                      "occurred_after": occurred_after}
        endpoint = 'events'
        if self.headers != None:
            h = self.headers
        else:
            h = {}
        h["Accept"] = "application/json"
        base_url = self.baseURL + endpoint
        request_url = self._get_link_with_parameters(base_url, parameters)
        return requests.get(request_url, headers=h)

    def retrieve_collections(self, asset_owner: str = '',
                             offset: int = 0,
                             limit: int = 300):
        '''
        asset_owner - string
        A wallet address. If specified, will return collections where the owner owns at least one asset belonging to smart contracts in the collection. The number of assets the account owns is shown as owned_asset_count for each collection.

        offset - int
        For pagination. Number of contracts offset from the beginning of the result list.

        limit - int
        For pagination. Maximum number of contracts to return.
        '''
        parameters = {"asset_owner": asset_owner,
                      "offset": offset,
                      "limit": limit}
        endpoint = 'collections'
        base_url = self.baseURL + endpoint
        request_url = self._get_link_with_parameters(base_url, parameters)
        return requests.get(request_url, headers=self.headers)

    def retrieve_bundles(self, on_sale: Union[bool, None] = None,
                         owner: Union[str, None] = None,
                         asset_contract_address: Union[str, None] = None,
                         asset_contract_addresses: Union[str, None] = None,
                         token_ids: Union[list, None] = None,
                         limit: int = 20,
                         offset: int = 0):
        '''
        on_sale - boolean
        If set to true, only show bundles currently on sale. If set to false, only show bundles that have been sold or cancelled.

        owner - string
        Account address of the owner of a bundle (and all assets within)

        asset_contract_address - string
        Contract address of all the assets in a bundle. Only works for homogenous bundles, not mixed ones.

        asset_contract_addresses - string
        An array of contract addresses to search for (e.g. ?asset_contract_addresses=0x1...&asset_contract_addresses=0x2...). Will return a list of bundles with assets having contracts that match ALL of the addresses in this array. Useful for querying for mixed bundles, e.g. ones with CryptoKitties AND CK Talisman statues.

        token_ids - list of ints
        A list of token IDs for showing only bundles with at least one of the token IDs in the list

        limit - int
        For pagination: how many results to return

        offset - int
        For pagination: the index of the result to start at (beginning with 0)
        '''
        parameters = {"on_sale": on_sale,
                      "owner": owner,
                      "asset_contract_address": asset_contract_address,
                      "asset_contract_addresses": asset_contract_addresses,
                      "token_ids": token_ids,
                      "limit": limit,
                      "offset": offset}
        endpoint = 'bundles'
        base_url = self.baseURL + endpoint
        request_url = self._get_link_with_parameters(base_url, parameters)
        return requests.get(request_url, headers=self.headers)

    def retrieve_single_asset(self, asset_contract_address: str,
                              token_id: int,
                              account_address: Union[str, None] = None):
        '''
        asset_contract_address - string - REQUIRED
        Address of the contract for this NFT

        token_id - string - REQUIRED
        Token ID for this item

        account_address - string
        Address of an owner of the token. If you include this, the response will include an ownership object that includes the number of tokens owned by the address provided instead of the top_ownerships object included in the standard response, which provides the number of tokens owned by each of the 10 addresses with the greatest supply of the token..
        '''
        base_url = self.baseURL + 'asset/' + \
            asset_contract_address + '/' + str(token_id) + '/'
        parameters = {"account_address": account_address}
        request_url = self._get_link_with_parameters(base_url, parameters)
        return requests.get(request_url, headers=self.headers)

    def retrieve_single_contract(self, asset_contract_address: str):
        '''
        asset_contract_address - string - REQUIRED
        Address of the contract
        '''
        request_url = self.baseURL + 'asset_contract/' + asset_contract_address
        return requests.get(request_url, headers=self.headers)

    def retrieving_single_collection(self, collection_slug: str):
        '''
        collection_slug - string - REQUIRED
        The collection slug of this collection that is used to uniquely link to this collection on OpenSea
        '''
        request_url = self.baseURL + 'collection/' + collection_slug
        return requests.get(request_url, headers=self.headers)

    def retrieve_collection_stats(self, collection_slug: str):
        '''
        collection_slug - string - REQUIRED
        The collection slug
        '''
        if self.headers != None:
            h = self.headers
        else:
            h = {}
        h["Accept"] = "application/json"
        request_url = self.baseURL + 'collection/' + collection_slug + '/stats'
        return requests.get(request_url, headers=h)

    def retrieve_orders(self, asset_contract_address: Union[str, None] = None,
                        payment_token_address: Union[str, None] = None,
                        maker: Union[str, None] = None,
                        taker: Union[str, None] = None,
                        owner: Union[str, None] = None,
                        is_english: Union[bool, None] = None,
                        bundled: bool = False,
                        include_bundled: bool = False,
                        include_invalid: bool = False,
                        listed_after: Union[int, None] = None,
                        listed_before: Union[int, None] = None,
                        token_id: Union[int, None] = None,
                        token_ids: Union[list, None] = None,
                        side: Union[int, None] = None,
                        sale_kind: Union[int, None] = None,
                        limit: int = 20,
                        offset: int = 0,
                        order_by: str = 'created_date',
                        order_direction: str = 'desc'):
        '''
        asset_contract_address - string
        Filter by smart contract address for the asset category. Needs to be defined together with token_id or token_ids.

        payment_token_address - string
        Filter by the address of the smart contract of the payment token that is accepted or offered by the order

        maker - string
        Filter by the order maker's wallet address

        taker - string
        Filter by the order taker's wallet address. Orders open for any taker have the null address as their taker.

        owner - string
        Filter by the asset owner's wallet address

        is_english - boolean
        When "true", only show English Auction sell orders, which wait for the highest bidder. When "false", exclude those.

        bundled - boolean
        Only show orders for bundles of assets

        include_bundled - boolean
        Include orders on bundles where all assets in the bundle share the address provided in asset_contract_address or where the bundle's maker is the address provided in owner

        include_invalid - boolean
        Include orders marked invalid by the orderbook, typically due to makers not owning enough of the token/asset anymore

        listed_after - date-time [int: epoch]
        Only show orders listed after this timestamp. Seconds since the Unix epoch.

        listed_before - date-time [int: epoch]
        Only show orders listed before this timestamp. Seconds since the Unix epoch.

        token_id - int
        Filter by the token ID of the order's asset. Needs to be defined together with asset_contract_address.

        token_ids - list of ints
        Filter by a list of token IDs for the order's asset. Needs to be defined together with asset_contract_address.

        side - int
        Filter by the side of the order. 0 for buy orders and 1 for sell orders.

        sale_kind - int
        Filter by the kind of sell order. 0 for fixed-price sales or min-bid auctions, and 1 for declining-price Dutch Auctions. NOTE: use only_english=true for filtering for only English Auctions

        limit - int
        Number of orders to return (capped at 50).

        offset - int
        Number of orders to offset by (for pagination)

        order_by - string
        How to sort the orders. Can be created_date for when they were made, or eth_price to see the lowest-priced orders first (converted to their ETH values). eth_price is only supported when asset_contract_address and token_id are also defined.

        order_direction - string
        Can be asc or desc for ascending or descending sort. For example, to see the cheapest orders, do order_direction asc and order_by eth_price.
        '''
        parameters = {"asset_contract_address": asset_contract_address,
                      "payment_token_address": payment_token_address,
                      "maker": maker,
                      "taker": taker,
                      "owner": owner,
                      "is_english": is_english,
                      "bundled": bundled,
                      "include_bundled": include_bundled,
                      "include_invalid": include_invalid,
                      "listed_after": listed_after,
                      "listed_before": listed_before,
                      "token_id": token_id,
                      "token_ids": token_ids,
                      "side": side,
                      "sale_kind": sale_kind,
                      "limit": limit,
                      "offset": offset,
                      "order_by": order_by,
                      "order_direction": order_direction}
        endpoint = 'orders'
        if self.headers != None:
            h = self.headers
        else:
            h = {}
        h["Accept"] = "application/json"
        base_url = self.baseURL + endpoint
        request_url = self._get_link_with_parameters(base_url, parameters)
        return requests.get(request_url, headers=h)

    # Function that helps building the url for the different requests
    def _get_link_with_parameters(self, base_url, parameters):
        request_url = base_url + '?'
        first = True
        for p in parameters:
            if parameters[p] != None:
                if type(parameters[p]) == list:
                    for i in range(len(parameters[p])):
                        if not first:
                            request_url = request_url + '&'
                        else:
                            first = False
                        request_url = request_url + p + \
                            '=' + str(parameters[p][i])
                elif str(parameters[p]) != '':
                    if not first:
                        request_url = request_url + '&'
                    else:
                        first = False
                    request_url = request_url + p + '=' + str(parameters[p])
        return request_url
