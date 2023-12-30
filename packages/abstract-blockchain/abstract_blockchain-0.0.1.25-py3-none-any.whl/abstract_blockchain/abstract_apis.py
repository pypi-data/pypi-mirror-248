from abstract_webtools import DynamicRateLimiterManager
from abstract_blockchain.abstract_rpcs import Choose_RPC_Parameters_GUI,RPCBridge
from abstract_blockchain.abstract_api_gui import choose_api_gui
from abstract_utilities import safe_json_loads
from abstract_security import get_env_value
class APIBridge:
    def __init__(self,api_data:str=None,api_gui:str=True,rpc_js:dict=None,rpc_gui=True,address:str=None,contract_address:str=None,start_block:str=None,end_block:str=None):
        self.re_initialize(api_data=api_data,api_gui=api_gui,rpc_js=rpc_js,rpc_gui=rpc_gui,address=address,contract_address=contract_address,start_block=start_block,end_block=end_block)
    def re_initialize(self,api_data:str=None,api_gui=True,rpc_js:dict=None,rpc_gui=True,address:str=None,contract_address:str=None,start_block:str=None,end_block:str=None):
        if rpc_js == None and rpc_gui:
            rpc_js = Choose_RPC_Parameters_GUI()
        self.rpc_manager = RPCBridge(rpc=rpc_js)
        
        self.address = address
        self.address=self.try_check_sum(address=self.address)
        self.rate_manager = DynamicRateLimiterManager(service_name=self.rpc_manager.rpc_js['Network_Name'])
        self.api_gui = api_gui
        self.api_data = api_data
        self.get_api_call(api_data,api_gui)
    def get_api_key(self):
        for network in ['bscscan','polygonscan','ftmscan','moonbeam.moonscan','etherscan']:
            if network in self.rpc_manager.rpc_js['Block_Explorer']:
                return get_env_value(key = f"{network}_api",deep_scan=True)
    def get_api_call(self,api_data_type:str=None,address:str=None,contract_address:str=None,start_block:str=None,end_block:str=None,api_gui=None):
        self.api_key = self.get_api_key()
        self.api_data = self.get_api_data_string(api_data_type=api_data_type,address=address,contract_address=contract_address,start_block=start_block,end_block=end_block,api_gui=api_gui)
        self.api_url = f"https://{('api.' if 'api' != self.rpc_manager.scanner[:len('api')] else '')}{self.rpc_manager.scanner}/api?{self.api_data}&apikey={self.api_key}"
        self.response = self.get_try(request_url=self.api_url)
    def get_api_data_string(self, api_data_type: str = None, address: str = None, 
                            contract_address: str = None, start_block: str = None, 
                            end_block: str = None, api_gui: bool = True) -> str:
        self.address = self.try_check_sum(address)
        self.contract_address = self.try_check_sum(contract_address)
        self.start_block, self.end_block = start_block, end_block
        self.api_data_type = api_data_type if api_data_type is not None else (choose_api_gui() if api_gui else None)
        self.api_gui = api_gui
        if not self.api_key:
            return api_data_type
        api_type_lower = self.api_data_type.lower() if self.api_data_type else ""
        if self.address:
            if any(obj in api_type_lower or obj in ['source', 'code', 'abi']):
                return f"module=contract&action=getabi&address={self.address}"
            if self.start_block and self.end_block:
                return f"module=account&action=tokentx&address={address}&startblock={self.start_block}&endblock={self.end_block}&sort=asc"
            if self.contract_address:
                return f"module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest"
        if self.contract_address:
            return f"module=module=stats&action=tokensupply&contractaddress={contract_address}"
        return api_data_type
    def get_http_variants(self, url: str) -> list:
        http, _, url_part = url.partition("://")
        alt_http = http[:-1] if http[-1] == "s" else http + "s"
        return [url, f"{alt_http}://{url_part}"]
    def get_api_variants(self, urls) -> list:
        if isinstance(urls, str):
            urls = [urls]
        return [
            f"{http}://api{('-' if url_part.startswith('.') else '.') + url_part[1:]}"
            for url in urls
            for http, _, url_part in [url.split("://")[0], '', url.split("://")[-1][len("api"):]]
        ]
    def get_try(self,request_url:str=None,service_name:str=None,low_limit:int=1,high_limit:int=5,limit_epoch:int=1,starting_tokens:int=5,epoch_cycle_adjustment:int=5):
        """
        Make a limited request to the ABI URL using rate-limiting.

        :param request_type: Type of the request (default is None).
        :param request_min: Minimum requests allowed in a rate-limited epoch (default is 10).
        :param request_max: Maximum requests allowed in a rate-limited epoch (default is 30).
        :param limit_epoch: Length of the rate-limited epoch in seconds (default is 60).
        :param request_start: Start of the rate-limited epoch (default is None).
        :param json_data: JSON data for the request (default is None).
        :return: Limited response from the ABI URL.
        """
        request_url= request_url or self.api_url
        self.service_name=service_name or self.rpc_manager.rpc_js['Network_Name']
        self.rate_manager.add_service(low_limit=low_limit, high_limit=high_limit, limit_epoch=limit_epoch, starting_tokens=starting_tokens)
        input(request_url)
        response = self.rate_manager.request(service_name=self.service_name,request_url=request_url)
        input(response)
        if response and isinstance(response,dict):
            response = safe_json_loads(response.get('result',response))
        return response
    def try_check_sum(self, address:str=None):
        """
        Attempt to convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        :raises ValueError: If the address is invalid.
        """
        address = address or self.address
        try:
            address = self.rpc_manager.w3.to_checksum_address(address)
            return address
        except:
            #raise ValueError("Invalid Ethereum Address")
            pass


APIBridge(api_data='abi',api_gui=False,rpc_js='avalanche',rpc_gui=False,address='0xCf5DA7C09A115c2800249557aA8aa7963B8658B1')
