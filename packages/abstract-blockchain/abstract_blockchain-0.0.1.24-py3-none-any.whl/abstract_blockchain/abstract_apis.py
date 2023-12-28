from abstract_webtools import DynamicRateLimiterManager
from abstract_blockchain.abstract_rpcs import Choose_RPC_Parameters_GUI,RPCBridge
from abstract_blockchain.abstract_api_gui import choose_api_gui
from abstract_utilities import safe_json_loads
from abstract_security import get_env_value
import requests
import json

class APIBridge:
    def __init__(self,api_data:str=None,api_gui:str=True,rpc_js:dict=None,rpc_gui=True,address:str=None,contract_address:str=None,start_block:str=None,end_block:str=None):
        self.re_initialize(api_data=api_data,api_gui=api_gui,rpc_js=rpc_js,rpc_gui=rpc_gui,address=address)
    def re_initialize(self,api_data:str=None,api_gui=True,rpc_js:dict=None,rpc_gui=True,address:str=None):
        if rpc_js == None and rpc_gui:
            rpc_js = Choose_RPC_Parameters_GUI()
        self.rpc_manager = RPCBridge(rpc_js=rpc_js)
        self.address = address
        self.request_manager = DynamicRateLimiterManager()
        api_manager = APIBridge(api_data=api_data,api_gui=api_gui,rpc_js=rpc_js,rpc_gui=api_gui,address=address,contract_address=contract_address,start_block=start_block,end_block=end_block)
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
        self.response = self.get_response(self.get_try(request_url=self.api_url))
    def get_api_data_string(self,api_data_type:str=None,address:str=None,contract_address:str=None,start_block:str=None,end_block:str=None,api_gui:str=True):
        self.address = self.try_check_sum(address)
        self.contract_address = self.try_check_sum(contract_address)
        self.start_block = start_block
        self.end_block = end_block
        if self.api_key:
            if self.api_data == None:
                if self. api_gui:
                    self.api_data = choose_api_gui()
            if api_data_type and self.api_key:
                if 'abi' in api_data_type.lower() and self.address:
                    return f"module=contract&action=getabi&address={self.address}"
                if ('source' in api_data_type.lower() or "code" in api_data_type.lower()) and self.address:
                    return f"module=contract&action=getabi&address={self.address}"
            if self.start_block and self.end_block and self.address:
                return f"module=account&action=tokentx&address={address}&startblock={self.start_block}&endblock={self.end_block}&sort=asc"
            elif self.contract_address and self.address:
                return f"module=account&action=tokenbalance&contractaddress={contract_address}&address={address}&tag=latest"
            elif self.contract_address:
                return f"module=module=stats&action=tokensupply&contractaddress={contract_address}"
        return api_data_type
    def api_keys(self):
        if self.rpc_manager.scanner in ['ftmscan.com','moonbeam.moonscan.io','polygonscan.com','bscscan.com']:
            return get_env_value(key=self.rpc_manager.scanner)
        return get_env_value(key='etherscan.io')        
    def get_http_variants(self,url:str):
        http_parts = url.split("://")
        http = http_parts[0]
        url_part = http_parts[-1]
        if http[-1]=="s":
            http_2 = http[:-1]
        else:
            http_2 = http+"s"
        return [url,http_2+"://"+url_part]
    def get_api_variants(self,urls:(list or str)):
        if isinstance(urls,str):
            urls= [urls]
        for i,url in enumerate(urls):
            http_parts = url.split("://")
            http = http_parts[0]
            url_part = http_parts[-1][len("api"):]
            if url_part[0]=="-":
                url_part_2 = '.'+url_part[1:]
            elif url_part[0]==".":
                url_part_2 = '-'+url_part[1:]
            urls[i]=http+"://api"+url_part_2
        return urls
    def get_try(self,request_url:str=None,service_name:str=None,low_limit:int=1,high_limit:int=5,limit_epoch:int=1,starting_tokens:int=5,epoch_cycle_adjustment:int=5):
        request_url= request_url or self.api_url
        service_name= service_name or self.rpc_manager.rpc_js['Network_Name']
        response = self.rate_manager.request(request_url=request_url)
        return response
    def get_request(self,request_url:str=None, service_name: str = None, low_limit: int = 20, high_limit: int = 30,limit_epoch: int = 60, starting_tokens: int = None,epoch_cycle_adjustment:int=None):
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
        self.request_manager.add_service(low_limit=low_limit, high_limit=high_limit, limit_epoch=limit_epoch, starting_tokens=starting_tokens)
        return self.request_manager.request(service_name=self.service_name,request_url=request_url)
    def get_response(self,response=None):
        """
        Parse the JSON response and return the ABI.

        :return: Parsed ABI response.
        """
        if response and isinstance(response,dict):
            response = safe_json_loads(response.get('result',response))
        return response
        
    def check_sum(self, address:str=None):
        """
        Convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        """
        address = address or self.address
        return self.rpc_manager.w3.to_checksum_address(address)
    def try_check_sum(self, address:str=None):
        """
        Attempt to convert the address to a checksum address.

        :param address: Ethereum address to convert.
        :return: Checksum Ethereum address.
        :raises ValueError: If the address is invalid.
        """
        address = address or self.address
        try:
            address = self.check_sum(address)
            return address
        except:
            #raise ValueError("Invalid Ethereum Address")
            pass


