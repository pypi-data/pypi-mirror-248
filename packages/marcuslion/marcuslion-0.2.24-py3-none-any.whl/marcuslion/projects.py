import pandas as pd

from marcuslion.config import api_version
from marcuslion.restcontroller import _RestController


class Projects(_RestController):
    """
    MarcusLion Projects class
        # $ curl 'https://qa1.marcuslion.com/core/projects'
    """

    def __init__(self):
        super().__init__(api_version + "/projects")

    def list(self) -> pd.DataFrame:
        """
        Projects.list()
        """
        return super().verify_get_frame("", {})

    def get_project_metadata(self, project_id) -> any:
        """
        Projects.get_project_metadata(id)
        """

        return super().verify_get(project_id)
