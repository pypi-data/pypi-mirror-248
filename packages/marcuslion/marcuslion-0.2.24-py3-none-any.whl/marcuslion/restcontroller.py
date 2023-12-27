import json
import urllib
import pandas as pd
import urllib3
import io

from marcuslion.config import base_url, api_key
from marcuslion.apiUtils import get_filename_from_api


class _RestController:
    """
    MarcusLion RestController class
    """
    __http = urllib3.PoolManager()

    def __init__(self, url):
        self.url = base_url + url

    def _prepare_params(self, action, params):
        s = self.url
        if action:
            s = s + '/' + action

        if params:
            s = s + '?' + urllib.parse.urlencode(params)

        return s

    def _api_request(self, action, params, method="GET", preload_content=True, **kwargs):
        full_url = self._prepare_params(action, params)

        resp = self.__http.request(method, full_url, headers={
            'X-MARCUSLION-API-KEY': api_key,
        }, preload_content=preload_content, **kwargs)

        if resp.status == 401:
            raise ValueError("401: Unauthorized User. URL:" + full_url)
        if resp.status != 200:
            raise ValueError("status: " + full_url + " -> " + (
                str(resp.status) + (" data: " + resp.data.decode()) if resp.data else ""))
        return resp

    def download_file(self, action, params, output_path=None):
        if output_path is None:
            output_path = "."
        resp = self._api_request(action, params, preload_content=False)
        file_name = f"{output_path}/{get_filename_from_api(resp)}"
        with open(file_name, 'wb') as out_file:
            for chunk in resp.stream(1024):
                out_file.write(chunk)

    def verify_get_frame(self, action, params) -> pd.DataFrame:
        response = self.verify_get(action, params)
        return pd.DataFrame.from_records(response)

    def verify_get(self, action, params=None) -> any:
        full_url = self._prepare_params(action, params)

        # Sending a GET request and getting back response as HTTPResponse object.
        resp = self._api_request(action, params)

        data_str = resp.data.decode()
        if len(data_str) == 0:
            return None
        return json.loads(data_str)

    def verify_get_data(self, action, params) -> pd.DataFrame:
        data = self.verify_get(action, params)
        if data is None:
            return pd.DataFrame()
        df = pd.DataFrame(data['data'])
        return df
