from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi


def test_async_method(api_client: ApiClient):
    metadata_client = MetadataResourceApi(api_client)
    thread = metadata_client.get_task_defs(async_req=True)
    thread.wait()
    print(thread.get())
