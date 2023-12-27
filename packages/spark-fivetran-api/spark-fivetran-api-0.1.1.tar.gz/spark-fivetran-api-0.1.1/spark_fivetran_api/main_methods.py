import requests
import base64

class FivetranAPI:
    """
    A Python wrapper for the Fivetran API.
    """
    def __init__(
        self, 
        api_base='https://api.fivetran.com/v1/',
        api_key=None,
        api_secret=None,
    ):
        if not api_key or not api_secret:
            raise ValueError('API key and secret are required')

        self.api_base = api_base.rstrip('/')
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = self._create_headers()

    def _create_headers(self):
        """
        Create headers for the API requests.
        """
        auth_string = base64.b64encode(f"{self.api_key}:{self.api_secret}".encode()).decode()
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {auth_string}'
        }

    def _verbose_print(self, verbose, msg):
        if verbose:
            print(msg)

    def _request(self, method, endpoint, verbose=False, **kwargs):
        """
        Generic method for API requests.
        """
        url = self.api_base + endpoint
        self._verbose_print(verbose, f"Request URL: {url}")
        response = requests.request(method, url, headers=self.headers, **kwargs)
        self._verbose_print(verbose, f"Response Status Code: {response.status_code}")
        return response.json() if response.ok else response.raise_for_status()

    def get(self, endpoint, verbose=False, **kwargs):
        return self._request('GET', endpoint, verbose=verbose, **kwargs)

    def post(self, endpoint, verbose=False, **kwargs):
        return self._request('POST', endpoint, verbose=verbose, **kwargs)

    def put(self, endpoint, verbose=False, **kwargs):
        return self._request('PUT', endpoint, verbose=verbose, **kwargs)

    def delete(self, endpoint, verbose=False, **kwargs):
        return self._request('DELETE', endpoint, verbose=verbose, **kwargs)

    def sync_connector_data(self, connector_id, force=False, verbose=False):
        """
        Triggers a data sync for an existing connector within your Fivetran account.
        """
        if not connector_id:
            raise ValueError("Connector ID is required.")

        endpoint = f'/connectors/{connector_id}/sync'
        return self.post(endpoint, json={"force": force}, verbose=verbose)
