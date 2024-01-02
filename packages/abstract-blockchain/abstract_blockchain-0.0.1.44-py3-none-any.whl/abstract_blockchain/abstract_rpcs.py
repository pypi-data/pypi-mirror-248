import os
from abstract_utilities.json_utils import closest_dictionary, find_matching_dicts,safe_read_from_json
from abstract_utilities.type_utils import is_number, convert_to_number,make_list
from web3 import Web3
script_path = os.path.abspath(__file__)
directory_path = os.path.dirname(script_path)
class RPCBridge: 
    """
    RPCBridge class manages RPC parameters for a blockchain.
    """

    def __init__(self, rpc_js: dict = None, testnet=False, rpc_list=None, rpc_gui=False):
        """
        Initializes the RPCBridge instance with RPC parameters.
        """
        self.rpc_list = rpc_list or self.get_default_rpc_list()
        self.testnet_rpcs, self.non_testnet_rpcs = self.separate_testnet_rpcs(self.rpc_list)
        self.non_testnet_values = self.get_total_values_list(self.non_testnet_rpcs)
        self.testnet_values = self.get_total_values_list(self.testnet_rpcs)
        self.rpc_values = {"False":[self.non_testnet_values,self.non_testnet_rpcs],"True":[self.testnet_values,self.testnet_rpcs]}
        self.common_chains = self.get_common_chains()
        self.rpc_js = self.update_rpc_js(rpc_js=rpc_js, testnet=testnet,rpc_gui=rpc_gui)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc)) if self.rpc else None
    def update_rpc_js(self, rpc_js: dict = None, testnet=False,rpc_gui=False):
        """
        Updates the RPC JavaScript object.
        """
        if rpc_gui:
            rpc_js = RPCGUIManager()
        if not isinstance(rpc_js,dict):
            if rpc_js == None:
                rpc_js = self.get_default_rpc()
            else:
                closest_rpc_items = self.get_closest_values(make_list(rpc_js),self.rpc_values[str(testnet)][0])
                rpc_js = closest_dictionary(dict_objs = self.rpc_values[str(testnet)][1],values=closest_rpc_items)
        self.rpc_js = rpc_js or self.get_default_rpc()
        self.setup_rpc_attributes()
        

    def setup_rpc_attributes(self):
        """
        Sets up various RPC attributes.
        """
        self.symbol = self.rpc_js.get('chain', '')
        self.name = self.rpc_js.get('name', '')
        self.explorers = self.rpc_js.get('explorers', [])
        self.explorer = self.explorers[0] if self.explorers else None
        self.rpcs = self.rpc_js.get('rpcs',self.get_rpc_urls(self.rpc_js))
        self.rpc = self.rpcs[0] if self.rpcs else None
        self.chainId = int(self.rpc_js['chainId']) if is_number(self.rpc_js['chainId']) else None
        self.scanner = self.strip_web(self.explorer)
    @staticmethod
    def get_common_chains():
            return ['Arbitrum One', 'Avalanche C-Chain', 'Endurance Smart Chain Mainnet', 'Celo Mainnet', 'Cronos Mainnet', 'Elastos Smart Chain', 'Ethereum Mainnet', 'Fuse Mainnet', 'Gnosis', 'Huobi ECO Chain Mainnet', 'Hoo Smart Chain', 'IoTeX Network Mainnet', 'Catecoin Chain Mainnet', 'Polygon Mainnet', 'Moonriver', 'Nahmii Mainnet', 'OKXChain Mainnet', 'Harmony Mainnet Shard 0', 'PandoProject Mainnet', 'Smart Bitcoin Cash', 'Neon EVM Mainnet', 'Telos EVM Mainnet', 'Ubiq']

    @staticmethod
    def strip_web(url:str):
        if isinstance(url,dict):
            url = url.get('url',url)        
        if url:
            if url.startswith("http://"):
                url = url.replace("http://", '', 1)
            elif url.startswith("https://"):
                url = url.replace("https://", '', 1)
            url = url.split('/')[0]
            return url
    @staticmethod
    def get_total_values_list(rpc_list):
        return {convert_to_number(value) for rpc in rpc_list for value in rpc.values() if isinstance(value, (str, int))}
    @staticmethod  
    def get_default_rpc_list():
        rpc_list =safe_read_from_json(os.path.join(directory_path,'data','rpc_list.json'))
        return rpc_list['chains']

    @staticmethod
    def separate_testnet_rpcs(rpc_list):
        """
        Separates testnet and non-testnet RPCs.
        """
        testnet_rpcs = [rpc for rpc in rpc_list if 'testnet' in rpc['name'].lower()]
        non_testnet_rpcs = [rpc for rpc in rpc_list if 'testnet' not in rpc['name'].lower()]
        return testnet_rpcs, non_testnet_rpcs
    @staticmethod
    def get_closest_values(rpc_js,total_values_list):
        rpc_js_new = []
        for i,rpc_value in enumerate(rpc_js):
            value = get_closest_match_from_list(rpc_value, total_values_list,sorted_out=False,highest_out=True)
            rpc_js_new.append(convert_to_number(value))
        return rpc_js_new
    @staticmethod
    def get_testnet(testnet, rpc_list):
        return [rpc for rpc in rpc_list if ('testnet' in rpc['name'].lower().split(' ')) == testnet]
    @staticmethod
    def get_rpc_urls(rpc_js):
        urls=[]
        rpc=''
        rpcs=[]
        if 'rpc' in rpc_js:
            rpcs = find_matching_dicts(dict_objs=rpc_js['rpc'],keys=['tracking'],values=['none']) or rpc_js['rpc']
        for rpc in rpcs:
            if 'url' in rpc:
                urls.append(rpc['url'])
        return urls
    @staticmethod
    def get_explorers(rpc_js):
        urls=[]
        explorer=''
        explorers=[]
        if 'explorers' in rpc_js:
            explorers=rpc_js['explorers']
        for explorer in explorers:
            if 'url' in explorer:
                urls.append(explorer['url'])
        return urls
    def get_default_rpc(self,Network_Name:str="Ethereum", rpc_list:list=None):
        rpc_list= rpc_list or self.rpc_list
        return closest_dictionary(dict_objs=rpc_list,values=[Network_Name])
class RPCGUIManager:
    def __init__(self, rpc_mgr=None,rpc_list:list=None):
        self.rpc_list = rpc_list
        self.rpc_mgr = rpc_mgr
        if self.rpc_mgr == None:
            self.rpc_mgr = RPCBridge(rpc_list=rpc_list)
        self.original_query=''
        self.rpc_list = self.rpc_mgr.rpc_list
        self.relevant_list = self.rpc_list
        self.network_names = list({item.get('name') for item in self.rpc_list})
        self.rpc_key_value_js = {"name":"-NETWORK_NAME-",'Network':"-NETWORK-",'chain':"-SYMBOL-",'chainId':"-CHAINID-",'rpc':"-RPC-",'explorers':"-BLOCK_EXPLORER-"}
        self.network_names.sort()
        self.new_network_names=self.network_names
        self.window_mgr = AbstractWindowManager()
        self.window_name = self.window_mgr.add_window(title='RPC Selector',layout=self.get_rpc_layout(),close_events=["-OK_RPC-","-EXIT_RPC-"],event_handlers=[self.rpc_win_while],suppress_raise_key_errors=False, suppress_error_popups=False, suppress_key_guessing=False,finalize=True)
        self.window=self.window_mgr.get_window()
        self.window_mgr.while_window(window_name=self.window_name)
        self.values = self.window_mgr.search_closed_windows(window_name=self.window_name,window=self.window)['values']
        self.rpc_values = self.get_rpc_values(self.values)
    def get_rpc_layout(self):
        layout = [
            [sg.Text('SEARCH'), sg.Input('', key='-SEARCH-',size=(20,1), enable_events=True)],
            [sg.Text('Network Name:'), sg.Combo(self.network_names, key='-NETWORK_NAME-', enable_events=True)],
            [sg.Text('Network:'), sg.Combo([], key='-NETWORK-',size=(20,1), enable_events=True)],
            [sg.Text('RPC:'), sg.Combo([], key='-RPC-',size=(20,1), enable_events=True)],
            [sg.Text('ChainID:'), sg.InputText(key='-CHAINID-',size=(20,1), disabled=True)],  # Make this an InputText to display ChainID
            [sg.Text('Block Explorer:'), sg.Combo([], key='-BLOCK_EXPLORER-',size=(20,1), enable_events=True)],
            [sg.Text('Symbol:'), sg.InputText(key='-SYMBOL-',size=(20,1), disabled=True)]  # Make this an InputText to display Symbol
        ]
        layout.append(create_row_of_buttons({"button_text":"OK","enable_event":True,"key":"-OK_RPC-"},
                                            {"button_text":"Show","enable_event":True,"key":"-SHOW_RPC-"},
                                            {"button_text":"Reset","enable_event":True,"key":"-RESET_RPC-"},
                                            {"button_text":"Exit","enable_event":True,"key":"-EXIT_RPC-"}))
        return layout
    def get_testnet_or_mainnet(self,string):
        return 'Testnet' if 'Testnet'.lower() in str(string).lower() else 'Mainnet'
    def get_key_from_value(self,value):
            """
            Fetches the key for a given value from the `get_rpc_js()` mapping.
            
            Parameters:
            - value: The value for which the key needs to be found.
            
            Returns:
            - The key corresponding to the value.
            """
            for key,key_value in self.rpc_key_value_js.items():
                if key_value == value:
                    return key
    def update_network_name(self,values,value,relevant_list):
        self.window['-NETWORK_NAME-'].update(values=values,value=value)
        relevant_data = [item for item in relevant_list if item.get('name') == value]
        self.window['-NETWORK-'].update(values=list({self.get_testnet_or_mainnet(item.get('name')) for item in relevant_data}), set_to_index=0)
        self.update_static_variables(relevant_data)
    def update_static_variables(self,relevant_data):
        rpc_values = next((self.rpc_mgr.get_rpc_urls(item) for item in relevant_data), '')#list(self.rpc_mgr.get_rpc_urls(item) for item in relevant_data)
        rpc_value=None
        if rpc_values and isinstance(rpc_values,list):
            rpc_value = rpc_values[0]
        self.window['-RPC-'].update(values=rpc_values,value=rpc_value)
        self.window['-CHAINID-'].update(value=next((item.get('chainId') for item in relevant_data), ''))
        explorer_values = next((self.rpc_mgr.get_explorers(item) for item in relevant_data), '')
        explorer_value=None
        if explorer_values and isinstance(explorer_values,list):
            explorer_value = explorer_values[0]
        self.window['-BLOCK_EXPLORER-'].update(values=explorer_values,value=explorer_value)
        self.window['-SYMBOL-'].update(value=next((item.get('chain') for item in relevant_data), ''))

    def get_back_values(self,num_list,values):
        rpc_values = []
        for num in num_list:
            rpc_values.append(values[num])
        return rpc_values
    def rpc_win_while(self,event,values,window):
        self.event,self.values,self.window=event,values,window
        value = None
        if event == '-SEARCH-':
            query = values['-SEARCH-']
            if query == '' or len(query) < len(self.original_query):
                self.new_network_names=self.network_names
                value=self.new_network_names[0]
                self.relevant_list = self.rpc_mgr.rpc_list
            else:
                self.relevant_list = [name for name in self.relevant_list if query.lower() in name['name'].lower()]
                names = [item['name'] for item in self.relevant_list]
                value = get_closest_match_from_list(query,names,highest_out=True)
      
                
                self.update_network_name(values=names,value=value,relevant_list=self.relevant_list)     
                self.index = [item for item in self.rpc_mgr.rpc_list if item['name'].lower() == value]
            if self.index:
                chain_ids = self.index[0]['chainId']
                rpcs = self.rpc_mgr.get_rpc_urls(self.index[0])
                explorers = self.rpc_mgr.get_explorers(self.index[0])
                symbol = chain_ids = self.index[0]['chain']
                network='testnet' if 'testnet' in self.index[0]['name'].lower() else 'Mainnet'
                self.window['-NETWORK_NAME-'].update(values=names,value=names[0])
                self.window['-NETWORK-'].update(value=network)
                self.window['-RPC-'].update(values=rpcs,value=rpcs[0])
                self.window['-CHAINID-'].update(value=chain_ids)
                self.window['-BLOCK_EXPLORER-'].update(values=explorers,value=rpcs[0])
                self.window['-SYMBOL-'].update(value=symbol)
                    #self.update_network_name(values=values,value=value,relevant_list=self.relevant_list)
            
        if event == '-NETWORK_NAME-':
            self.update_network_name(values=self.new_network_names,value=self.values.get('-NETWORK_NAME-'),relevant_list=self.relevant_list)
        elif event == '-NETWORK-':
            selected_name = self.values['-NETWORK_NAME-']
            selected_network = self.values['-NETWORK-']
            relevant_data = [item for item in self.relevant_list if item.get('name') == selected_name and self.get_testnet_or_mainnet(item.get('name')) == selected_network]
            self.update_static_variables(relevant_data)
    def get_rpc_values(self,values) -> dict or None:
        rpc=[]
        if values:
            for each in values.keys():
                key = self.get_key_from_value(each)
                if key in list(self.rpc_key_value_js.keys()):
                    rpc.append(values[each])
        new_rpc={}
        testnet=False
        need = []
        for key in ['-NETWORK_NAME-','-SYMBOL-','-CHAINID-','-NETWORK-','-BLOCK_EXPLORER-','-RPC-']:
            value = values.get(key)
            if value:
                if key == '-NETWORK-':
                    if 'testnet'.lower() in str(value).lower():
                        testnet=True
                else:
                    new_rpc[self.get_key_from_value(value=key)] = value
            else:
                need.append(key)
        return self.rpc_mgr.derive_rpc(new_rpc=new_rpc,testnet=testnet)

