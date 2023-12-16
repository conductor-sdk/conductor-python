class UserDetails:
    """
    User info data class with constructor to set properties
    """

    swagger_types = {
        '_name': 'str',
        '_user_id': 'str',
        '_addresses': 'object',
    }

    attribute_map = {
        '_name': 'name',
        '_user_id': 'user_id',
        '_addresses': 'addresses'
    }

    def __init__(self, name: str, user_id: int, addresses: list[object]) -> None:
        self._name = name
        self._user_id = user_id
        self._addresses = addresses

    @property
    def name(self) -> str:
        return self._name

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def address(self) -> list[object]:
        return self._addresses