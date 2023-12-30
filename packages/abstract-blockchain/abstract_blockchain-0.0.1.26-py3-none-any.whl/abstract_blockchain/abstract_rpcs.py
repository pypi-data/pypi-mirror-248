import os
from abstract_utilities.json_utils import safe_read_from_json,closest_dictionary,find_matching_dicts
from abstract_utilities.type_utils import convert_to_number,is_number,make_list
from abstract_utilities.compare_utils import get_closest_match_from_list,get_shared_characters_count,get_common_portions
from abstract_gui import create_row_of_buttons,sg,AbstractWindowManager
from web3 import Web3
script_path = os.path.abspath(__file__)
directory_path = os.path.dirname(script_path)
def if_list_itterate(obj,itteration=0):
    if obj and isinstance(obj,list):
        obj = obj[itteration]
    return obj
class RPCBridge: 
    """
    RPCBridge class manages RPC parameters for a blockchain.
    """
    def __init__(self, rpc_js:dict=None,testnet=False,rpc_list=None):
        """
        Initializes the RPCBridge instance with RPC parameters.

        :param rpc_js: Dictionary containing RPC parameters.
        """
        self.rpc_list= rpc_list or self.get_default_rpc_list()
        self.update_rpc_js(rpc_js=rpc_js,testnet=testnet)

    def update_rpc_list(self,rpc_list):
        self.rpc_list = rpc_list
    def update_rpc_js(self,rpc_js:dict=None,testnet=False):
        self.rpc_js = rpc_js
        if not isinstance(self.rpc_js,dict):
            if self.rpc_js == None:
                self.rpc_js = self.get_default_rpc()
            else:
                self.valid_rpcs = self.get_testnet(testnet,self.rpc_list)
                self.total_values_list = self.get_total_values_list(self.valid_rpcs)
                self.rpc_js = self.get_closest_values(make_list(self.rpc_js),self.total_values_list)
                self.rpc_js = closest_dictionary(dict_objs = self.valid_rpcs,values=self.rpc_js)
        self.symbol = self.rpc_js['chain']
        self.network_name = self.rpc_js['name']
        self.block_explorers = self.get_explorers(self.rpc_js)
        print(self.block_explorers)
        self.block_explorer  = if_list_itterate(self.block_explorers)
        print(self.block_explorer)
        print(self.rpc_js)
        self.rpcs = self.get_rpc_urls(self.rpc_js)
        self.rpc  = if_list_itterate(self.rpcs)
        self.chain_id = self.rpc_js['chainId']
        self.scanner = self.strip_web(self.block_explorer)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc))
        return self.rpc_js
    def return_rpc_js(self,rpc_js:dict=None):
        return rpc_js or self.rpc_js
    def get_default_rpc(self,Network_Name:str="Ethereum", rpc_list:list=None):
        rpc_list= rpc_list or self.rpc_list
        return closest_dictionary(dict_objs=rpc_list,values=[Network_Name])
    def derive_rpc(self,new_rpc,testnet=False):
        derive_rpc_js = new_rpc
        for key in ['rpc','explorers']:
            if key in derive_rpc_js:
                del derive_rpc_js[key]
        if 'chainId' in new_rpc:
            if is_number(new_rpc['chainId']):
                new_rpc['chainId'] = int(new_rpc['chainId'])
        self.update_rpc_js(rpc_js=list(derive_rpc_js.values()),testnet=testnet)
        new_rpc['rpcs'] = new_rpc.get('rpcs',self.rpcs)
        self.rpcs=new_rpc['rpcs']
        new_rpc['rpc'] = new_rpc.get('rpc',if_list_itterate(self.rpcs))
        self.rpc=new_rpc['rpc']
        new_rpc['w3'] = Web3(Web3.HTTPProvider(self.rpc))
        self.w3 = new_rpc['w3']
        new_rpc['explorers'] = new_rpc.get('explorers',self.block_explorer)
        self.block_explorer = new_rpc['explorers']
        new_rpc['scanner'] = self.strip_web(self.block_explorer)
        self.scanner = new_rpc['explorers']
        new_rpc['chainId'] = new_rpc.get('chainId',self.chain_id)
        self.chain_id = new_rpc['chainId']
        new_rpc['name'] = new_rpc.get('name',self.network_name)
        self.network_name=new_rpc['name']
        new_rpc['chain'] = new_rpc.get('chain',self.symbol)
        self.symbol=new_rpc['chain']
        return new_rpc
    @staticmethod
    def strip_web(url:str):
        if url:
            if url.startswith("http://"):
                url = url.replace("http://", '', 1)
            elif url.startswith("https://"):
                url = url.replace("https://", '', 1)
            url = url.split('/')[0]
            return url
    @staticmethod  
    def get_default_rpc_list():
        rpc_list =safe_read_from_json(os.path.join(directory_path,'data','rpc_list.json'))
        return rpc_list['chains']
    @staticmethod
    def get_total_values_list(rpc_list):
        return {
            convert_to_number(value) 
            for rpc in rpc_list 
            for value in rpc.values() 
            if isinstance(value, (str, int))
        }
    @staticmethod
    def get_closest_values(rpc_js,total_values_list):
        rpc_js_new = []
        for i,rpc_value in enumerate(rpc_js):
            value = get_closest_match_from_list(rpc_value, total_values_list,sorted_out=False,highest_out=True)
            rpc_js_new.append(convert_to_number(value))
        return rpc_js_new
    @staticmethod
    def get_testnet(testnet, rpc_list):
        test_net_string = 'testnet'
        return [
            rpc for rpc in rpc_list
            if (test_net_string in rpc['name'].lower().split(' ')) == testnet]
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

class RPCGUIManager:
    def __init__(self, rpc_list:list=None):
        self.rpc_mgr = RPCBridge(rpc_list=rpc_list)
        self.rpc_list=self.rpc_mgr.rpc_list
        self.relevant_list = self.rpc_mgr.rpc_list
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
    def rpc_win_while(self,event,values,window):
        self.event,self.values,self.window=event,values,window
        if event == '-SEARCH-':
            query = values['-SEARCH-']
            if query == '':
                self.new_network_names=self.network_names
                value=self.new_network_names[0]
                self.relevant_list = self.rpc_mgr.rpc_list
            else:
                self.new_network_names = [name for name in self.network_names if query.lower() in name.lower()]
                values = get_closest_match_from_list(query,self.new_network_names,sorted_out=True,highest_out=False)
                value = values[0]
                self.relevant_list = [item for item in self.rpc_mgr.rpc_list if item.get('name') in values]
            self.update_network_name(values=values,value=value,relevant_list=self.relevant_list)
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

