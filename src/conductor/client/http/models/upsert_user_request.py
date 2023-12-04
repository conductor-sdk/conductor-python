import pprint
import re  # noqa: F401

import six


class UpsertUserRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {"name": "str", "roles": "list[str]", "groups": "list[str]"}

    attribute_map = {"name": "name", "roles": "roles", "groups": "groups"}

    def __init__(self, name=None, roles=None, groups=None):  # noqa: E501
        """UpsertUserRequest - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._roles = None
        self._groups = None
        self.discriminator = None
        self.name = name
        if roles is not None:
            self.roles = roles
        if groups is not None:
            self.groups = groups

    @property
    def name(self):
        """Gets the name of this UpsertUserRequest.  # noqa: E501

        User's full name  # noqa: E501

        :return: The name of this UpsertUserRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpsertUserRequest.

        User's full name  # noqa: E501

        :param name: The name of this UpsertUserRequest.  # noqa: E501
        :type: str
        """
        self._name = name

    @property
    def roles(self):
        """Gets the roles of this UpsertUserRequest.  # noqa: E501


        :return: The roles of this UpsertUserRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this UpsertUserRequest.


        :param roles: The roles of this UpsertUserRequest.  # noqa: E501
        :type: list[str]
        """
        allowed_values = [
            "ADMIN",
            "USER",
            "WORKER",
            "METADATA_MANAGER",
            "WORKFLOW_MANAGER",
        ]  # noqa: E501
        if not set(roles).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `roles` [{0}], must be a subset of [{1}]".format(  # noqa: E501
                    ", ".join(map(str, set(roles) - set(allowed_values))),  # noqa: E501
                    ", ".join(map(str, allowed_values)),
                )
            )

        self._roles = roles

    @property
    def groups(self):
        """Gets the groups of this UpsertUserRequest.  # noqa: E501

        Ids of the groups this user belongs to  # noqa: E501

        :return: The groups of this UpsertUserRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """Sets the groups of this UpsertUserRequest.

        Ids of the groups this user belongs to  # noqa: E501

        :param groups: The groups of this UpsertUserRequest.  # noqa: E501
        :type: list[str]
        """

        self._groups = groups

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(UpsertUserRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpsertUserRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
