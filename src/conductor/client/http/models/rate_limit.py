import pprint
import re  # noqa: F401

import six


class RateLimit(object):
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
    swagger_types = {"tag": "str", "concurrent_execution_limit": "int"}

    attribute_map = {
        "tag": "tag",
        "concurrent_execution_limit": "concurrentExecutionLimit",
    }

    def __init__(self, tag=None, concurrent_execution_limit=None):  # noqa: E501
        """RateLimit - a model defined in Swagger"""  # noqa: E501
        self._tag = None
        self._concurrent_execution_limit = None
        self.discriminator = None
        if tag is not None:
            self.tag = tag
        if concurrent_execution_limit is not None:
            self.concurrent_execution_limit = concurrent_execution_limit

    @property
    def tag(self):
        """Gets the tag of this RateLimit.  # noqa: E501


        :return: The tag of this RateLimit.  # noqa: E501
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this RateLimit.


        :param tag: The tag of this RateLimit.  # noqa: E501
        :type: str
        """

        self._tag = tag

    @property
    def concurrent_execution_limit(self):
        """Gets the concurrent_execution_limit of this RateLimit.  # noqa: E501


        :return: The concurrent_execution_limit of this RateLimit.  # noqa: E501
        :rtype: int
        """
        return self._concurrent_execution_limit

    @concurrent_execution_limit.setter
    def concurrent_execution_limit(self, concurrent_execution_limit):
        """Sets the concurrent_execution_limit of this RateLimit.


        :param concurrent_execution_limit: The concurrent_execution_limit of this RateLimit.  # noqa: E501
        :type: int
        """

        self._concurrent_execution_limit = concurrent_execution_limit

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
        if issubclass(RateLimit, dict):
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
        if not isinstance(other, RateLimit):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
