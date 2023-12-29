import requests
import logging

from .factories import Factory
from .models import Project, ProjectInventory

logger = logging.getLogger(__name__)

class CodeInsightApiClient:
    def __init__(self,
                 base_url: str,
                 api_token: str
                 ):
        self.base_url = base_url
        self.api_url = f"{base_url}/codeinsight/api"
        self.api_token = api_token
        self.api_headers = {
            'Content-Type': 'application/json',
            "Authorization": "token %s" % self.api_token,
            "User-Agent": "code_insight_api_py",
        }

    def request(self, method, url_part: str, params: dict = None):
        url = f"{self.api_url}/{url_part}"
        response = requests.request(method, url, headers=self.api_headers, params=params)

        if not response.ok:
            logger.error(f"Error: {response.status_code} - {response.reason}")
            logger.error(response.text)
            raise response.raise_for_status()      

        return response

    @property
    def projects(self) -> Factory:
        return Factory.create(self, Project)
    
    @property
    def project_inventory(self) -> Factory:
        return Factory.create(self, ProjectInventory)
    

    # Coming soon...?
    def inventories(self):
        raise NotImplementedError("Inventories are not yet implemented")
    
    def vulnerabilites(self):
        raise NotImplementedError
    
    def users(self):
        raise NotImplementedError
    
    def licenses(self):
        raise NotImplementedError
    
    def tasks(self):
        raise NotImplementedError
    
    def rules(self):
        raise NotImplementedError
    
    def reports(self):
        raise NotImplementedError
    
    def files(self):
        raise NotImplementedError
    
    def folders(self):
        raise NotImplementedError
    
    def jobs(self):
        raise NotImplementedError
    
    def components(self):
        raise NotImplementedError

