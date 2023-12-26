import json
from .api_service import APIService
from .contracts import Contracts
from .order_signer import OrderSigner
from .onboarding_signer import OnboardingSigner
from .utilities import *
from .constants import TIME, SERVICE_URLS
from .interfaces import *
from .sockets import Sockets
from .enumerations import *
from .websocket_client import WebsocketClient

from eth_account import Account
from eth_utils import to_wei, from_wei

class FireflyClient:
    def __init__(self, are_terms_accepted, network, private_key=""):
        self.are_terms_accepted = are_terms_accepted
        self.network = network
        self.w3 = self._connect_w3(self.network["url"])
        if private_key != "":
            self.account = Account.from_key(private_key)
        self.apis = APIService(self.network["apiGateway"], default_value(self.network, "UUID", "") )
        self.dmsApi = APIService(self.network["dmsURL"], default_value(self.network, "UUID", ""))
        self.socket = Sockets(self.network["socketURL"])
        self.webSocketClient = WebsocketClient(self.network["webSocketURL"])
        self.contracts = Contracts()
        self.order_signers = {}
        self.onboarding_signer = OnboardingSigner()
        
            
    async def init(self, user_onboarding=True, api_token=""):
        """
            Initialize the client.
            Inputs:
                user_onboarding (bool, optional): If set to true onboards the user address to exchange and gets authToken. Defaults to True.
                api_token(string, optional): API token to initialize client in read-only mode 
        """
        self.contracts.contract_addresses = await self.get_contract_addresses()

        if "error" in self.contracts.contract_addresses:
            raise Exception("Error initializing client: {}".format(self.contracts.contract_addresses["error"]))

        # adding auxiliaryContracts to contracts class
        for i,j in self.contracts.get_contract_address(market="auxiliaryContractsAddresses").items():
            self.add_contract(name=i,address=j)
        
        # contracts pertaining to markets
        for k, v in self.contracts.contract_addresses.items():
            if 'PERP' in k:
                self.add_contract(name="Perpetual",address=v["Perpetual"], market=k)

        if api_token:
            self.apis.api_token = api_token
            # for socket
            self.socket.set_api_token(api_token)
            self.webSocketClient.set_api_token(api_token)
        # In case of api_token received, user onboarding is not done
        elif user_onboarding:
            self.apis.auth_token = await self.onboard_user()
            self.dmsApi.auth_token = self.apis.auth_token
            self.socket.set_token(self.apis.auth_token)
            self.webSocketClient.set_token(self.apis.auth_token)


    async def onboard_user(self, token:str=None):
        """
            On boards the user address and returns user authentication token.
            Inputs:
                token: user access token, if you possess one.
            Returns:
                str: user authorization token
        """
        user_auth_token = token
        
        # if no auth token provided create on
        if not user_auth_token:
            onboarding_signature = self.onboarding_signer.create_signature(
                self.network["onboardingUrl"], 
                self.account.key)

            response = await self.authorize_signed_hash(onboarding_signature) 
            
            if 'error' in response:
                raise SystemError("Authorization error: {}".format(response['error']['message']))

            user_auth_token = response['token']

        return user_auth_token

    def set_uuid(self, uuid):
        self.apis.set_uuid(uuid)
        self.dmsApi.set_uuid(uuid)

    async def authorize_signed_hash(self, signed_hash:str):
        """
            Registers user as an authorized user on server and returns authorization token.
            Inputs:
                signed_hash: signed onboarding hash
            Returns:
                dict: response from user authorization API Firefly
        """
        return await self.apis.post(
            SERVICE_URLS["USER"]["AUTHORIZE"],
            {
                "signature": signed_hash,
                "userAddress": self.account.address,
                "isTermAccepted": self.are_terms_accepted,
            })

    def add_market(self, symbol: MARKET_SYMBOLS, trader_contract=None):
        """
            Adds Order signer for market to instance's order_signers dict.
            Inputs:
                symbol(MARKET_SYMBOLS): Market symbol of order signer.
                trader_contract(str): Contract address of the Orders contract.
            
            Returns:
                bool: indicating whether the market was successfully added
        """
        symbol_str = symbol.value
        # if signer for market already exists return false
        if (symbol_str in self.order_signers):
            return False 
          
        # if orders contract address is not provided get 
        # from addresses retrieved from dapi
        if trader_contract == None:
            try:
                trader_contract = self.contracts.contract_addresses[symbol_str]["IsolatedTrader"]
            except:
                raise SystemError("Can't find orders contract address for market: {}".format(symbol_str))

        self.order_signers[symbol_str] = OrderSigner(
            self.network["chainId"],
            trader_contract
            )
        return True 

    def add_contract(self,name,address,market=None):
        """
            Adds contracts to the instance's contracts dictionary. 
            The contract name should match the contract's abi name in ./abi directory or a new abi should be added with the desired name.
            Inputs:
                name(str): The contract name.
                address(str): The contract address.
                market(str): The market (ETH/BTC) this contract belongs to (required for market specific contracts).
        """
        abi = self.contracts.get_contract_abi(name)
        if market:
            contract=self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)
            self.contracts.set_contracts(market=market,name=name,contract=contract)
        else:
            contract=self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)
            self.contracts.set_contracts(name=name,contract=contract)
        return 

    def create_order_to_sign(self, params:OrderSignatureRequest):
        """
            Creates order signature request for an order.
            Inputs:
                params (OrderSignatureRequest): parameters to create order with, refer OrderSignatureRequest 
            
            Returns:
                Order: order raw info
        """
        expiration = current_unix_timestamp()        
        # MARKET ORDER set expiration of 1 minute
        if (params["orderType"] == ORDER_TYPE.MARKET):
            expiration += TIME["SECONDS_IN_A_MINUTE"]
        # LIMIT ORDER set expiration of 30 days
        else:
            expiration += TIME["SECONDS_IN_A_MONTH"] 

        return Order (
            isBuy = params["side"] == ORDER_SIDE.BUY,
            price = to_wei(params["price"], "ether"),
            quantity =  to_wei(params["quantity"], "ether"),
            leverage =  to_wei(default_value(params, "leverage", 1), "ether"),
            maker =  params["maker"].lower() if "maker" in params else self.account.address.lower(),
            reduceOnly =  default_value(params, "reduceOnly", False),
            postOnly =  default_value(params, "postOnly", False),
            cancelOnRevert =  default_value(params, "cancelOnRevert", False),
            triggerPrice =  to_wei(default_value(params,"triggerPrice",0),"ether"),
            expiration =  default_value(params, "expiration", expiration),
            salt =  default_value(params, "salt", random_number(1000000)),
            )

    def create_signed_order(self, params:OrderSignatureRequest):
        """
            Create an order from provided params and signs it using the private 
            key of the account
            Inputs:
                params (OrderSignatureRequest): parameters to create order with
    
            Returns:
                OrderSignatureResponse: order raw info and generated signature
        """
        
        # from params create order to sign
        order = self.create_order_to_sign(params)

        symbol = params["symbol"].value
        order_signer = self.order_signers.get(symbol) 

        if not order_signer:
            raise SystemError("Provided Market Symbol({}) is not added to client library".format(symbol))
        
        order_signature = order_signer.sign_order(order, self.account.key.hex())
        
        return OrderSignatureResponse(
            symbol=symbol,
            price=params["price"],
            quantity=params["quantity"],
            side=params["side"],
            leverage=default_value(params, "leverage", 1),
            reduceOnly=default_value(params, "reduceOnly", False),
            postOnly=default_value(params, "postOnly", False),
            triggerPrice=default_value(params, "triggerPrice", 0),
            cancelOnRevert =  default_value(params, "cancelOnRevert", False),
            salt=order["salt"],
            expiration=order["expiration"],
            orderSignature=order_signature,
            orderType=params["orderType"],
            maker=order["maker"],
            timeInForce=default_value(params, "timeInForce", TIME_IN_FORCE.GOOD_TILL_TIME),
        )
    
    def create_signed_cancel_order(self,params:OrderSignatureRequest, parentAddress:str=""):
        """
            Creates a cancel order request from provided params and signs it using the private
            key of the account

        Inputs:
            params (OrderSignatureRequest): parameters to create cancel order with
            parentAddress (str): Only provided by a sub account
 
        Returns:
            OrderSignatureResponse: generated cancel signature 
        """
        try:
            signer:OrderSigner = self._get_order_signer(params["symbol"])
            order_to_sign = self.create_order_to_sign(params)
            hash = signer.get_order_hash(order_to_sign)
            return self.create_signed_cancel_orders(params["symbol"], hash, parentAddress)
        except Exception as e:
            return ""

    def create_signed_cancel_orders(self, symbol:MARKET_SYMBOLS, order_hash:list, parentAddress:str=""):
        """
            Creates a cancel order from provided params and sign it using the private
            key of the account

        Inputs:
            params (list): a list of order hashes
            parentAddress (str): only provided by a sub account
        Returns:
            OrderCancellationRequest: containing symbol, hashes and signature
        """
        if type(order_hash)!=list:
            order_hash = [order_hash]

        order_signer:OrderSigner = self._get_order_signer(symbol)
        cancel_hash = order_signer.sign_cancellation_hash(order_hash)
        hash_sig = order_signer.sign_hash(cancel_hash,self.account.key.hex(), "01")
        return OrderCancellationRequest(
            symbol=symbol.value,
            hashes=order_hash,
            signature=hash_sig,
            parentAddress=parentAddress
        )

    async def post_cancel_order(self,params:OrderCancellationRequest):
        """
            POST cancel order request to Firefly
            Inputs:
                params(dict): a dictionary with OrderCancellationRequest required params
            Returns:
                dict: response from orders delete API Firefly
        """

        return await self.apis.delete(
            SERVICE_URLS["ORDERS"]["ORDERS_HASH"],
            {
            "symbol": params["symbol"],
            "orderHashes":params["hashes"],
            "cancelSignature":params["signature"],
            "parentAddress": params["parentAddress"],
            },
            auth_required=True
            )
    
    async def cancel_all_orders(self, symbol:MARKET_SYMBOLS, status: List[ORDER_STATUS], parentAddress:str=""):
        """
            GETs all orders of specified status for the specified symbol, 
            and creates a cancellation request for all orders and 
            POSTs the cancel order request to Firefly
            Inputs:
                symbol (MARKET_SYMBOLS): Market for which orders are to be cancelled 
                status (List[ORDER_STATUS]): status of orders that need to be cancelled 
                parentAddress (str): address of parent account, only provided by sub account
            Returns:
                dict: response from orders delete API Firefly
        """
        orders = await self.get_orders({
            "symbol":symbol,
            "parentAddress": parentAddress,
            "statuses":status
        })

        hashes = []
        for i in orders:
            hashes.append(i["hash"])
        
        if len(hashes) > 0:
            req = self.create_signed_cancel_orders(symbol, hashes, parentAddress)
            return await self.post_cancel_order(req)

        return False
    
    async def post_signed_order(self, params:PlaceOrderRequest):
        """
            Creates an order from provided params and signs it using the private
            key of the account

            Inputs:
                params (OrderSignatureRequest): parameters to create order with

            Returns:
                OrderSignatureResponse: order raw info and generated signature
        """

        return await self.apis.post(
            SERVICE_URLS["ORDERS"]["ORDERS"],
            {
            "symbol": params["symbol"],
            "price": to_wei(params["price"], "ether"),
            "quantity": to_wei(params["quantity"], "ether"),
            "leverage": to_wei(params["leverage"], "ether"),
            "userAddress": params["maker"],
            "orderType": params["orderType"].value,
            "triggerPrice": to_wei(params["triggerPrice"],"ether"),
            "side": params["side"].value,            
            "reduceOnly": params["reduceOnly"],
            "salt": params["salt"],
            "expiration": params["expiration"],
            "orderSignature": params["orderSignature"],
            "timeInForce": default_enum_value(params, "timeInForce", TIME_IN_FORCE.GOOD_TILL_TIME),
            "postOnly": default_value(params, "postOnly", False),
            "cancelOnRevert": default_value(params, "cancelOnRevert", False),
            "clientId": "firefly-client: {}".format(default_value(params, "clientId", "firefly-client")),
            },
            auth_required=True
            )

    ## Contract calls
    async def deposit_margin_to_bank(self, amount):
        """
            Deposits given amount of USDC from user's account to margin bank

            Inputs:
                amount (number): quantity of usdc to be deposited to bank in base decimals (1,2 etc)

            Returns:
                Boolean: true if amount is successfully deposited, false otherwise
        """

        usdc_contract = self.contracts.get_contract(name="USDC") 
        mb_contract = self.contracts.get_contract(name="MarginBank") 

        amount = to_wei(amount,"mwei") 

        # approve funds on usdc
        
        construct_txn = usdc_contract.functions.approve(
            mb_contract.address, 
            amount).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
            })

        self._execute_tx(construct_txn)

        # deposit to margin bank
        construct_txn = mb_contract.functions.depositToBank(
            self.account.address, 
            amount).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                })

        self._execute_tx(construct_txn)

        return True
    
    async def close_position(self, symbol, parent=""):
        """
            closes user position when market in de-listed

            Inputs:
                symbol (MARKET_SYMBOLS): market on which position is to be closed

            Returns:
                Boolean: true if position is closed, false otherwise
        """

        perp_contract = self.contracts.get_contract(name="Perpetual", market=symbol.value) 

        # deposit to margin bank
        construct_txn = perp_contract.functions.closePosition(
            self.account.address if parent == "" else parent).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                })

        self._execute_tx(construct_txn)

        return True

    async def withdraw_margin_from_bank(self, amount):
        """
            Withdraws given amount of usdc from margin bank if possible

            Inputs:
                amount (number): quantity of usdc to be withdrawn from bank in base decimals (1,2 etc)

            Returns:
                Boolean: true if amount is successfully withdrawn, false otherwise
        """

        mb_contract = self.contracts.get_contract(name="MarginBank")
        amount = to_wei(amount,"mwei")

        # withdraw from margin bank
        construct_txn = mb_contract.functions.withdrawFromBank(
            self.account.address, 
            amount).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                })

        self._execute_tx(construct_txn)

        return True

    async def adjust_leverage(self, symbol, leverage, parentAddress:str=""):
        """
            Adjusts user leverage to the provided one for their current position on-chain and off-chain.
            If a user has no position for the provided symbol, leverage only recorded off-chain

            Inputs:
                symbol (MARKET_SYMBOLS): market for which to adjust user leverage
                leverage (number): new leverage to be set. Must be in base decimals (1,2 etc.)
                parentAddress (str): optional, if provided, the leverage of parent is 
                                    being adjusted (for sub accounts only)
            Returns:
                Boolean: true if the leverage is successfully adjusted
        """

        user_position = await self.get_user_position({"symbol":symbol, "parentAddress": parentAddress})
        
        account_address = Web3.to_checksum_address(self.account.address if parentAddress == "" else parentAddress)
            
        # implies user has an open position on-chain, perform on-chain leverage update
        if(user_position != {}):
            perp_contract = self.contracts.get_contract(name="Perpetual", market=symbol.value) 
            construct_txn = perp_contract.functions.adjustLeverage(
                account_address, 
                to_wei(leverage, "ether")).build_transaction({
                    'from': self.account.address,
                    'nonce': self.w3.eth.get_transaction_count(self.account.address),
                    })  
            signedTx = self._signed_tx_hex(construct_txn)
            response = await self.apis.post(
                SERVICE_URLS["USER"]["ADJUST_LEVERAGE"],
                {
                    "symbol": symbol.value,
                    "address": account_address,
                    "leverage": to_wei(leverage, "ether"),
                    "marginType": MARGIN_TYPE.ISOLATED.value,
                    "signedTransaction": signedTx
                },
                auth_required=True
                )

            # If API is unsuccessful make direct contract call to update the leverage
            if 'error' in response:
                self._execute_tx(construct_txn)

        else:
            await self.apis.post(
                SERVICE_URLS["USER"]["ADJUST_LEVERAGE"],
                {
                    "symbol": symbol.value,
                    "address": account_address,
                    "leverage": to_wei(leverage, "ether"),
                    "marginType": MARGIN_TYPE.ISOLATED.value,
                    },
                auth_required=True
                )
        
        return True
 
    async def adjust_margin(self, symbol, operation, amount, parentAddress:str=""):
        """
            Adjusts user's on-chain position by adding or removing the specified amount of margin.
            Performs on-chain contract call, the user must have gas tokens
            Inputs:
                symbol (MARKET_SYMBOLS): market for which to adjust user leverage
                operation (ADJUST_MARGIN): ADD/REMOVE adding or removing margin to position
                amount (number): amount of margin to be adjusted
                parentAddress (str): optional, if provided, the margin of parent is 
                                    being adjusted (for sub accounts only)
            Returns:
                Boolean: true if the margin is adjusted
        """

        user_position = await self.get_user_position({"symbol":symbol, "parentAddress": parentAddress})

        account_address = Web3.to_checksum_address(self.account.address if parentAddress == "" else parentAddress)

        if(user_position == {}):
            raise(Exception("User has no open position on market: {}".format(symbol)))
        else:
            perp_contract = self.contracts.get_contract(name="Perpetual", market=symbol.value) 
            on_chain_call = perp_contract.functions.addMargin if operation == ADJUST_MARGIN.ADD  else perp_contract.functions.removeMargin

            construct_txn = on_chain_call(
                account_address, 
                to_wei(amount, "ether")).build_transaction({
                    'from': self.account.address,
                    'nonce': self.w3.eth.get_transaction_count(self.account.address),
                    })

            self._execute_tx(construct_txn)
        
        return True
    
    async def update_sub_account(self, symbol, sub_account_address, status):
        """
            Used to whitelist and account as a sub account or revoke sub account status from an account.
            Inputs:
                symbol (MARKET_SYMBOLS): market on which sub account status is to be updated
                sub_account_address (str): address of the sub account
                status (bool): new status of the sub account

            Returns:
                Boolean: true if the sub account status is update
        """
        perp_contract = self.contracts.get_contract(name="Perpetual", market=symbol.value) 

        construct_txn = perp_contract.functions.setSubAccount(
                sub_account_address, 
                status).build_transaction({
                    'from': self.account.address,
                    'nonce': self.w3.eth.get_transaction_count(self.account.address),
                    })

        self._execute_tx(construct_txn)

        return True

    async def get_native_chain_token_balance(self, userAddress: str = None):
        """
            Returns user's native chain token (ETH/BOBA) balance
        """
        try:
            return from_wei(self.w3.eth.get_balance(self.w3.to_checksum_address(userAddress or self.account.address)), "ether")
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))

    async def get_usdc_balance(self, userAddress: str = None):
        """
            Returns user's USDC token balance on Firefly.
        """
        try:
            contract = self.contracts.get_contract(name="USDC")
            raw_bal = contract.functions.balanceOf(userAddress or self.account.address).call() 
            return from_wei(int(raw_bal), "mwei")
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))

    async def get_margin_bank_balance(self,userAddress: str = None ):
        """
            Returns user's Margin Bank balance.
        """
        try:
            contract = self.contracts.get_contract(name="MarginBank")
            return from_wei(contract.functions.getAccountBankBalance(userAddress or self.account.address).call(),"ether")
        except Exception as e:
            raise(Exception("Failed to get balance, Exception: {}".format(e)))

    ## Market endpoints
    
    async def get_orderbook(self, params:GetOrderbookRequest):
        """
            Returns a dictionary containing the orderbook snapshot.
            Inputs:
                params(GetOrderbookRequest): the order symbol and limit(orderbook depth) 
            Returns:
                dict: Orderbook snapshot
        """
        params = extract_enums(params, ["symbol"])

        return await self.apis.get(
            SERVICE_URLS["MARKET"]["ORDER_BOOK"], 
            params
            )

    async def get_exchange_status(self):
        """
            Returns a dictionary containing the exchange status.
            Returns:
                dict: exchange status
        """
        return await self.apis.get(SERVICE_URLS["MARKET"]["STATUS"], {})

    async def get_market_symbols(self):
        """
            Returns a list of active market symbols.
            Returns:
                list: active market symbols
        """
        return await self.apis.get(
            SERVICE_URLS["MARKET"]["SYMBOLS"],
            {} 
            )

    async def get_funding_rate(self,symbol:MARKET_SYMBOLS):
        """
            Returns a dictionary containing the current funding rate on market.
            Inputs:
                symbol(MARKET_SYMBOLS): symbol of market
            Returns:
                dict: Funding rate into
        """
        return await self.apis.get(
            SERVICE_URLS["MARKET"]["FUNDING_RATE"],
            {"symbol": symbol.value}
        )
    
    async def get_transfer_history(self,params:GetTransferHistoryRequest):
        """
            Returns a list of the user's transfer history records, a boolean indicating if there is/are more page(s),
                and the next page number
            Inputs:
                params(GetTransferHistoryRequest): params required to fetch transfer history  
            Returns:
                GetUserTransferHistoryResponse: 
                    isMoreDataAvailable: boolean indicating if there is/are more page(s)
                    nextCursor: the next page number
                    data: a list of the user's transfer history record
        """
        
        return await self.apis.get(
            SERVICE_URLS["USER"]["TRANSFER_HISTORY"],
            params,
            auth_required=True
        )

    async def get_funding_history(self,params:GetFundingHistoryRequest):
        """
            Returns a list of the user's funding payments, a boolean indicating if there is/are more page(s),
                and the next page number
            Inputs:
                params(GetFundingHistoryRequest): params required to fetch funding history  
            Returns:
                GetFundingHistoryResponse: 
                    isMoreDataAvailable: boolean indicating if there is/are more page(s)
                    nextCursor: the next page number
                    data: a list of the user's funding payments
        """

        params = extract_enums(params,["symbol"])
        
        return await self.apis.get(
            SERVICE_URLS["USER"]["FUNDING_HISTORY"],
            params,
            auth_required=True
        )

    async def get_market_meta_info(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing market meta info.
            Inputs:
                symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                dict: meta info
        """
        query = {"symbol": symbol.value } if symbol else {}

        return await self.apis.get(
            SERVICE_URLS["MARKET"]["META"], 
            query
            )

    async def get_market_data(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing market's current data about best ask/bid, 24 hour volume, market price etc..
            Inputs:
                symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                dict: meta info
        """
        query = {"symbol": symbol.value } if symbol else {}

        return await self.apis.get(
            SERVICE_URLS["MARKET"]["MARKET_DATA"], 
            query
            )
    
    async def get_exchange_info(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing exchange info for market(s). The min/max trade size, max allowed oi open
            min/max trade price, step size, tick size etc...
            Inputs:
                symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                dict: exchange info
        """
        query = {"symbol": symbol.value } if symbol else {}
        return await self.apis.get(
            SERVICE_URLS["MARKET"]["EXCHANGE_INFO"], 
            query
            )
    
    async def get_master_info(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing master info for market(s).
            It contains all market data, exchange info and meta data of market(s)
            Inputs:
                symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                dict: master info
        """
        query = {"symbol": symbol.value } if symbol else {}
        return await self.apis.get(
            SERVICE_URLS["MARKET"]["MASTER_INFO"], 
            query
            )
    
    async def get_ticker_data(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns a dictionary containing ticker data for market(s).
            Inputs:
                symbol(MARKET_SYMBOLS): the market symbol  
            Returns:
                dict: ticker info
        """
        query = {"symbol": symbol.value } if symbol else {}
        return await self.apis.get(
            SERVICE_URLS["MARKET"]["TICKER"], 
            query
            )

    async def get_market_candle_stick_data(self,params:GetCandleStickRequest):
        """
            Returns a list containing the candle stick data.
            Inputs:
                params(GetCandleStickRequest): params required to fetch candle stick data  
            Returns:
                list: the candle stick data
        """
        params = extract_enums(params, ["symbol","interval"])
        
        return await self.apis.get(
            SERVICE_URLS["MARKET"]["CANDLE_STICK_DATA"], 
            params
            )
    
    async def get_market_recent_trades(self,params:GetMarketRecentTradesRequest):
        """
            Returns a list containing the recent trades data.
            Inputs:
                params(GetCandleStickRequest): params required to fetch candle stick data  
            Returns:
                ist: the recent trades 
        """
        params = extract_enums(params, ["symbol", "traders"])

        return await self.apis.get(
            SERVICE_URLS["MARKET"]["RECENT_TRADE"], 
            params
            ) 

    async def get_contract_addresses(self, symbol:MARKET_SYMBOLS=None):
        """
            Returns all contract addresses for the provided market.
            Inputs:
                symbol(MARKET_SYMBOLS): the market symbol
            Returns:
                dict: all the contract addresses
        """
        query = {"symbol": symbol.value } if symbol else {}

        return await self.apis.get(
            SERVICE_URLS["MARKET"]["CONTRACT_ADDRESSES"], 
            query
            )   

    ## User endpoints
    
    def get_account(self):
        """
            Returns the user account object 
        """
        return self.account

    def get_public_address(self):
        """
            Returns the user account public address
        """
        return self.account.address

    async def generate_readonly_token(self):
        """
            Returns a read-only token generated for authenticated user.
        """
        return await self.apis.post(
            SERVICE_URLS["USER"]["GENERATE_READONLY_TOKEN"],
            {},
            True
        )
    
    async def get_orders(self,params:GetOrderRequest):
        """
            Returns a list of orders.
            Inputs:
                params(GetOrderRequest): params required to query orders (e.g. symbol,statuses) 
            Returns:
                list: a list of orders 
        """
        params = extract_enums(params,["symbol","statuses", "orderType"])

        return await self.apis.get(
            SERVICE_URLS["USER"]["ORDERS"],
            params,
            True
        )
    
    async def get_orders_by_type(self,params:GetOrderByTypeRequest):
        """
            Returns a list of orders by type.
            Inputs:
                params(GetOrderByTypeRequest): params required to query orders (e.g. symbol,statuses) 
            Returns:
                list: a list of orders by order type
        """
        params = extract_enums(params,["symbol","limitStatuses","marketStatuses"])

        return await self.apis.get(
            SERVICE_URLS["USER"]["ORDERS_BY_TYPE"],
            params,
            True
        )
        
    async def get_transaction_history(self,params:GetTransactionHistoryRequest):
        """
            Returns a list of transaction.
            Inputs:
                params(GetTransactionHistoryRequest): params to query transactions (e.g. symbol) 
            Returns:
                list: a list of transactions
        """
        params = extract_enums(params,["symbol"])
        return await self.apis.get(
            SERVICE_URLS["USER"]["USER_TRANSACTION_HISTORY"],
            params,
            True
        )
    
    async def get_user_position(self,params:GetPositionRequest):
        """
            Returns a list of positions.
            Inputs:
                params(GetPositionRequest): params required to query positions (e.g. symbol) 
            Returns:
                list: a list of positions
        """
        params = extract_enums(params,["symbol"])
        return await self.apis.get(
            SERVICE_URLS["USER"]["USER_POSITIONS"],
            params,
            True
        )

    async def get_user_trades(self,params:GetUserTradesRequest):
        """
            Returns a list of user trades.
            Inputs:
                params(GetUserTradesRequest): params to query trades (e.g. symbol) 
            Returns:
                list: a list of positions
        """
        params = extract_enums(params,["symbol","type"])
        return await self.apis.get(
            SERVICE_URLS["USER"]["USER_TRADES"],
            params,
            True
        )
    
    async def get_user_trades_history(self,params:GetUserTradesHistoryRequest):
        """
            Returns a list of user trades history.
            Inputs:
                params(GetUserTradesHistoryRequest): params to query trades (e.g. symbol) 
            Returns:
                list: a list of positions
        """
        params = extract_enums(params,["symbol","type"])
        return await self.apis.get(
            SERVICE_URLS["USER"]["USER_TRADES_HISTORY"],
            params,
            True
        )

    async def get_user_account_data(self, parentAddress:str = ""):
        """
            Returns user account data.
            Inputs:
                parentAddress: an optional field, used by sub accounts to fetch parent account state 
        """
        return await self.apis.get(
            service_url = SERVICE_URLS["USER"]["ACCOUNT"],
            query = { "parentAddress": parentAddress },
            auth_required = True
        )
        
    async def get_user_leverage(self, symbol:MARKET_SYMBOLS, parentAddress:str=""):
        """
            Returns user market default leverage.
            Inputs:
                symbol(MARKET_SYMBOLS): market symbol to get user market default leverage for. 
                parentAddress(str): an optional field, used by sub accounts to fetch parent account state
            Returns:
                str: user default leverage 
        """
        account_data_by_market = (await self.get_user_account_data(parentAddress))["accountDataByMarket"]
        
        for i in account_data_by_market:
            if symbol.value==i["symbol"]:
                return int(from_wei(int(i["selectedLeverage"]), "ether"))    

        # default leverage on system is 3
        # todo fetch from exchange info route
        return 3

    async def get_cancel_on_disconnect_timer(self, params:GetCancelOnDisconnectTimerRequest=None):
        """
            Returns a list of the user's countDowns for provided market symbol,
            Inputs:
                - symbol(MARKET_SYMBOLS): (Optional) market symbol to get user market cancel_on_disconnect timer for, not providing it would return all the active countDown timers for each market.  
                - parentAddress (str):(Optional) Only provided by a sub account
            Returns:
                - GetCountDownsResponse:
                    - countDowns: object with provided market symbol and respective countDown timer
                    - timestamp
        """
        
        params = extract_enums(params, ["symbol"])
        response = await self.dmsApi.get(
            SERVICE_URLS["USER"]["CANCEL_ON_DISCONNECT"],
            params,
            auth_required=True
        )
        # check for service unavailibility
        if hasattr(response, 'status') and response.status == 503:
            raise Exception("Cancel on Disconnect (dead-mans-switch) feature is currently unavailable")
            
        return response
    
    async def reset_cancel_on_disconnect_timer(self, params:PostTimerAttributes):
        """
            Returns PostTimerResponse containing accepted and failed countdowns, and the next page number
            Inputs:
                - params(PostTimerAttributes): params required to fetch funding history  
            Returns:
                - PostTimerResponse: 
                    - acceptedToReset: array with symbols for which timer was reset successfully
                    - failedReset: aray with symbols for whcih timer failed to reset 
        """
        response = await self.dmsApi.post(
            SERVICE_URLS["USER"]["CANCEL_ON_DISCONNECT"],
            json.dumps(params),
            auth_required=True,
            contentType = 'application/json'
        )
        # check for service unavailibility
        if hasattr(response, 'status') and response.status == 503:
             raise Exception("Cancel on Disconnect (dead-mans-switch) feature is currently unavailable")
        return response
       
    ## Growth endpoints
    async def generate_referral_code(self,params:GenerateReferralCodeRequest):
        """
            Inputs:
                params(GenerateReferralCodeRequest): params required to generate referral code
            Returns:
                - GenerateReferralCodeResponse
                    - referralAddress
                    - referralCode
                    - message?
        """
        return await self.apis.post(
            SERVICE_URLS["GROWTH"]["GENERATE_CODE"],
            params,
            True
        )
    
    async def affiliate_link_referred_user(self,params:LinkReferredUserRequest):
        """
            Inputs:
                params(LinkReferredUserRequest): params required to link referred user
            Returns:
                - LinkReferredUserResponse
                    - referralCode
                    - refereeAddress
                    - campaignId
                    - message
        """
        return await self.apis.post(
            SERVICE_URLS["GROWTH"]["AFFILIATE_LINK_REFERRED_USER"],
            params,
            True
        )
    
    async def get_referrer_info(self,parentAddress:str=""):
        """
            Inputs:
                parentAddress (Optional)
            Returns:
                - GetReferrerInfoResponse
                    - isReferee
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["REFERRER_INFO"],
            {"parentAddress":parentAddress},
            True
        )
    
    async def get_campaign_details(self):
        """
            Returns:
                - list of GetCampaignDetailsResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["CAMPAIGN_DETAILS"]
        )
    
    async def get_campaign_rewards(self,campaignId:int, parentAddress: str):
        """
            Inputs:
                campaignId: represents campaign id for which user wants to fetch rewards of
                parentAddress (Optional)
            Returns:
                - GetCampaignRewardsResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["CAMPAIGN_REWARDS"],
            {"campaignId": campaignId, "parentAddress":parentAddress },
            True
        )
    
    async def get_affiliate_payouts(self,campaignId:int,parentAddress:str="" ):
        """
            Inputs:
                campaignId: represents campaign id for which user wants to fetch payouts of
                parentAddress (Optional)
            Returns:
                - List of GetAffiliatePayoutsResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["AFFILIATE_PAYOUTS"],
            {"campaignId": campaignId,"parentAddress":parentAddress},
            True
        )
    
    async def get_affiliate_referee_details(self,params:GetAffiliateRefereeDetailsRequest):
        """
            Inputs:
                params: GetAffiliateRefereeDetailsRequest
            Returns:
                - GetAffiliateRefereeDetailsRequestGetAffiliatePayoutsResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["AFFILIATE_REFEREE_DETAILS"],
            params,
            True
        )
    
    async def get_affiliate_referee_count(self,campaignId:int, parentAddress:str=""):
        """
            Inputs:
                campaignId: represents campaign id for which user wants to fetch referee count of
                parentAddress (Optional)
            Returns:
                - GetAffiliateRefereeCountResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["AFFILIATE_REFEREES_COUNT"],
            {"campaignId": campaignId, "parentAddress":parentAddress},
            True
        )
    
    async def get_user_rewards_history(self,params:GetUserRewardsHistoryRequest):
        """
            Inputs:
                params: GetUserRewardsHistoryRequest
            Returns:
                - GetUserRewardsHistoryResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["USER_REWARDS_HISTORY"],
            params,
            True
        )
    
    async def get_user_rewards_summary(self,parentAddress:str=""):
        """
            Returns:
                - List of GetUserRewardsSummaryResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["USER_REWARDS_SUMMARY"],
            { "parentAddress":parentAddress},
            True
        )
    
    async def get_trade_and_earn_rewards_overview(self,campaignId:int, parentAddress:str=""):
        """
            Inputs:
                campaignId: represents campaign id for which user wants to fetch rewards overview of
                parentAddress (Optional)
            Returns:
                - GetTradeAndEarnRewardsOverviewResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["REWARDS_OVERVIEW"],
            {"campaignId": campaignId, "parentAddress": parentAddress},
            True
        )
    
    async def get_trade_and_earn_rewards_detail(self,params:GetTradeAndEarnRewardsDetailRequest):
        """
            Inputs:
                params: GetTradeAndEarnRewardsDetailRequest
            Returns:
                - GetTradeAndEarnRewardsDetailResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["REWARDS_DETAILS"],
            params,
            True
        )
    
    async def get_total_historical_trading_rewards(self, parentAddress:str=""):
        """
            Returns:
                - GetTotalHistoricalTradingRewardsResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["TOTAL_HISTORICAL_TRADING_REWARDS"],
            {"parentAddress":parentAddress},
            True
        )
    
    async def get_maker_rewards_summary(self, parentAddress: str):
        """
            Returns:
                - GetMakerRewardsSummaryResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["MAKER_REWARDS_SUMMARY"],
            {"parentAddress":parentAddress},
            True
        )
    
    async def get_maker_reward_details(self,params:GetMakerRewardDetailsRequest):
        """
            Inputs:
                params: GetMakerRewardDetailsRequest
            Returns:
                - GetMakerRewardDetailsResponse
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["MAKER_REWARDS_DETAILS"],
            params,
            True
        )

    async def get_user_white_list_status_for_market_maker(self):
        """
            Returns:
                - GetUserWhiteListStatusForMarkeMaker
        """
        return await self.apis.get(
            SERVICE_URLS["GROWTH"]["MAKER_WHITELIST_STATUS"],
            {},
            True
        )
    
    #open referral program

    async def get_open_referral_referee_details(self, params: CursorPaginationPayload):
        """
        Get open referral referee details.

        Args:
            params (CursorPaginationPayload): Parameters for pagination.

        Returns:
            dict: Response containing referee details.
        """
        url = SERVICE_URLS["GROWTH"]["OPEN_REFERRAL_REFEREE_DETAILS"]
        response = self.apis.get(url, params, True)
        return response  # Returns a dictionary containing referee details.

    async def get_open_referral_details(self, campaignId, parentAddress: str=""):
        """
        Get open referral details.

        Args:
            campaignId: The campaign ID.
            parentAddress (Optional)

        Returns:
            dict: Response containing open referral details.
        """
        params = {"campaignId": campaignId, "parentAddress": parentAddress}
        url = SERVICE_URLS["GROWTH"]["OPEN_REFERRAL_REFEREES_COUNT"]
        response = self.apis.get(url, params, True)
        return response  # Returns a dictionary containing open referral details.

    async def get_open_referral_payouts(self, params: CursorPaginationPayload):
        """
        Get open referral payouts.

        Args:
            params (CursorPaginationPayload): Parameters for pagination.

        Returns:
            dict: Response containing open referral payouts.
        """
        url = SERVICE_URLS["GROWTH"]["OPEN_REFERRAL_PAYOUTS"]
        response = self.apis.get(url, params, True)
        return response  # Returns a dictionary containing open referral payouts.

    async def generate_open_referral_referral_code(self, campaignId):
        """
        Generate open referral referral code.

        Args:
            campaignId: The campaign ID.

        Returns:
            dict: Response containing the generated referral code.
        """
        data = {"campaignId": campaignId}
        url = SERVICE_URLS["GROWTH"]["OPEN_REFERRAL_GENERATE_CODE"]
        response = self.apis.post(url, data, True)
        return response  # Returns a dictionary containing the generated referral code.

    async def get_open_referral_overview(self, parentAddress:str="" ):
        """
        Get open referral overview.

        Returns:
        dict: Response containing an overview of open referrals.
        """
        url = SERVICE_URLS["GROWTH"]["OPEN_REFERRAL_OVERVIEW"]
        response = self.apis.get(url, {"parentAddress":parentAddress}, True)
        return response  # Returns a dictionary containing an overview of open referrals.

    async def open_referral_link_referred_user(self, referralCode):
        """
        Link an open referral to a referred user.

        Args:
            referralCode: The referral code.

        Returns:
            bool: True if the linking was successful, False otherwise.
        """
        data = {"referralCode": referralCode}
        url = SERVICE_URLS["GROWTH"]["OPEN_REFERRAL_LINK_REFERRED_USER"]
        response = self.apis.post(url, data, True)
        return response  # Returns a boolean indicating success or failure.



    #open referral program

    ## Internal methods
    def _get_order_signer(self,symbol:MARKET_SYMBOLS=None):
        """
            Returns the order signer for the specified symbol, else returns a dictionary of symbol -> order signer
            Inputs:
                symbol(MARKET_SYMBOLS): the symbol to get order signer for, optional
            Returns:
                dict/order signer object
        """
        if symbol:
            if symbol.value in self.order_signers.keys():
                return self.order_signers[symbol.value]
            else:
                raise(Exception("Signer does not exist. Make sure to add market"))
        else:
            return self.order_signers

    def _signed_tx_hex(self, transaction):
        """
            An internal function to create signed tx
        Args:
            transaction: A constructed txn using self.account address

        Returns:
            signedTransaction: a string representation of signed transaction
        """
        tx_create = self.w3.eth.account.sign_transaction(transaction, self.account.key)
        return tx_create.rawTransaction.hex()

    def _execute_tx(self, transaction):
        """
            An internal function to create signed tx and wait for its receipt
        Args:
            transaction: A constructed txn using self.account address

        Returns:
            tx_receipt: a receipt of txn mined on-chain
        """
        tx_create = self.w3.eth.account.sign_transaction(transaction, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(tx_create.rawTransaction)
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def _connect_w3(self,url):
        """
            Creates a connection to Web3 RPC given the RPC url.
        """
        try:
            return Web3(Web3.HTTPProvider(url))
        except:
            raise(Exception("Failed to connect to Host: {}".format(url)))
           


    async def close_connections(self):
         # close aio http connection
        await self.apis.close_session()
        await self.dmsApi.close_session()
           