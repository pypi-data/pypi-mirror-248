import io
import urllib
import urllib3

import pandas as pd

from marcuslion.config import base_url, api_key, api_version
from marcuslion.restcontroller import _RestController


class Documents(_RestController):
    """
    MarcusLion Documents class
    """

    def __init__(self):
        super().__init__(api_version + "/documents")

    def list(self) -> pd.DataFrame:
        """
        Documents.list()
        """
        return super().verify_get("list", {})

    def query(self, ref):
        """
        Documents.query(ref)
        """
        pass

    def search(self, search) -> pd.DataFrame:
        """
        Documents.search(search)
        """
        pass

    def download(self, ref) -> pd.DataFrame:
        """
        Providers.download(ref)
        """
        pass
