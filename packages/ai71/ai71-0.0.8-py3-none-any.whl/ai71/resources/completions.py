from ..clients import base_client
from . import base_resource


class Completions(base_resource.BaseResource):
    def __init__(self, client: base_client.BaseClient) -> None:
        super().__init__(client)


class AsyncCompletions(base_resource.AsyncBaseResource):
    def __init__(self, client: base_client.AsyncBaseClient) -> None:
        super().__init__(client)
