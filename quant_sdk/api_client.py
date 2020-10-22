from .api_config import ApiConfig
import requests
import multiprocessing
from multiprocessing.pool import ThreadPool
from typing import Union


# todo test whether api_config can be merged with api_client class
#  class ApiConfig:
#     api_key = None
#     url_base = 'https://api.blocksize.capital/v1/'
#     .
#     => if setting and changing of the key works make change

class ApiClient:

    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = ApiConfig.api_key
        self.headers = {"x-api-key": api_key}
        self.base_url = ApiConfig.url_base
        self.methods = {'GET', 'POST'}
        # self.thread_pool = ThreadPool() # todo after many instances of ApiConfig have been called no more thread.pools can be opened anymore either a __del__ will help or deepcopy need to look into the issue

    def make_api_call(self, access_route: str, method: str, params=None, data=None,
                      parallel=False) -> Union[requests.Response, multiprocessing.pool.ApplyResult]:

        if method not in self.methods:
            raise ValueError('Only GET or POST allowed as methods.')

        url = f'{self.base_url}{access_route}'

        if method == 'GET':
            if not parallel:
                return requests.get(url=url, params=params, headers=self.headers)
            # else:  # todo after many iterations thread.pools cannoit be opened anymore either a __del__ will help or deepcopy need to look into the issue
            #     thread = self.thread_pool.apply_async(requests.get, [url], {'params': params, 'headers': self.headers})
            # return thread

        if method == 'POST':
            return requests.post(url=url, data=data, headers=self.headers)
