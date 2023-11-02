from typing_extensions import Self
from conductor.client.orkes.models.access_key_status import AccessKeyStatus

class AccessKeyResponse:
    def __init__(self, id: str, status: AccessKeyStatus) -> Self:
        self._id = id
        self._status = status
        self._created_at = None
