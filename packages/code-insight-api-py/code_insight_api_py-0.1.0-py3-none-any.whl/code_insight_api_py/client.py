import requests

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

    def get_inventory(self,
                      project_id: int,
                      skip_vulnerabilities: bool = False
                      ):
        url = f"{self.api_url}/inventory/{project_id}"
        response = requests.get(url, headers=self.api_headers)
        return response.json()
