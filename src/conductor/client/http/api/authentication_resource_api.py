from conductor.client.http.api_client import ApiClient


class AuthenticationResourceApi:
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.__get_token()

    def __get_token(self):
        header_params = {
            'Content-Type': self.api_client.select_header_content_type(['*/*'])
        }
        body = {
            'keyId': self.api_client.configuration.authentication_settings.key_id,
            'keySecret': self.api_client.configuration.authentication_settings.key_secret
        }
        response = self.api_client.call_api(
            '/api/token', 'POST',
            header_params,
            body=body,
            _return_http_data_only=True,
            response_type='Token'
        )
        self.token = response.token
