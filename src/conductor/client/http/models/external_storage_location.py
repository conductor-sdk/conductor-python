import pprint
import six
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExternalStorageLocation:
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
    _uri: Optional[str] = field(default=None, repr=False)
    _path: Optional[str] = field(default=None, repr=False)
    
    swagger_types = {
        'uri': 'str',
        'path': 'str'
    }

    attribute_map = {
        'uri': 'uri',
        'path': 'path'
    }

    def __init__(self, uri=None, path=None):  # noqa: E501
        """ExternalStorageLocation - a model defined in Swagger"""  # noqa: E501
        self._uri = None
        self._path = None
        self.discriminator = None
        if uri is not None:
            self.uri = uri
        if path is not None:
            self.path = path

    def __post_init__(self):
        """Initialize after dataclass initialization"""
        self.discriminator = None

    @property
    def uri(self):
        """Gets the uri of this ExternalStorageLocation.  # noqa: E501


        :return: The uri of this ExternalStorageLocation.  # noqa: E501
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this ExternalStorageLocation.


        :param uri: The uri of this ExternalStorageLocation.  # noqa: E501
        :type: str
        """

        self._uri = uri

    @property
    def path(self):
        """Gets the path of this ExternalStorageLocation.  # noqa: E501


        :return: The path of this ExternalStorageLocation.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this ExternalStorageLocation.


        :param path: The path of this ExternalStorageLocation.  # noqa: E501
        :type: str
        """

        self._path = path

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ExternalStorageLocation, dict):
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
        if not isinstance(other, ExternalStorageLocation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other