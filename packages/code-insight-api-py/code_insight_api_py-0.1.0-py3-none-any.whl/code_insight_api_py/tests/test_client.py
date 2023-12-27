import pytest
import logging


from code_insight_api_py import CodeInsightApiClient

logger = logging.getLogger(__name__)

## CHANGE ME ##
TEST_URL = "https://api.revenera.com"
TEST_API_TOKEN = "your_api_token"

class TestCodeInsightApiClient:
    @pytest.fixture
    def client(self):
        return CodeInsightApiClient(TEST_URL, TEST_API_TOKEN)
    
    def test_client(self, client):
        assert client.base_url == TEST_URL
    
    def get_inventory(self, client):
        return client.get_inventory(1)