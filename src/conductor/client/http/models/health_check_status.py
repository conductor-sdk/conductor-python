import pprint
import re  # noqa: F401

import six


class HealthCheckStatus(object):
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
    swagger_types = {
        "health_results": "list[Health]",
        "suppressed_health_results": "list[Health]",
        "healthy": "bool",
    }

    attribute_map = {
        "health_results": "healthResults",
        "suppressed_health_results": "suppressedHealthResults",
        "healthy": "healthy",
    }

    def __init__(
        self, health_results=None, suppressed_health_results=None, healthy=None
    ):  # noqa: E501
        """HealthCheckStatus - a model defined in Swagger"""  # noqa: E501
        self._health_results = None
        self._suppressed_health_results = None
        self._healthy = None
        self.discriminator = None
        if health_results is not None:
            self.health_results = health_results
        if suppressed_health_results is not None:
            self.suppressed_health_results = suppressed_health_results
        if healthy is not None:
            self.healthy = healthy

    @property
    def health_results(self):
        """Gets the health_results of this HealthCheckStatus.  # noqa: E501


        :return: The health_results of this HealthCheckStatus.  # noqa: E501
        :rtype: list[Health]
        """
        return self._health_results

    @health_results.setter
    def health_results(self, health_results):
        """Sets the health_results of this HealthCheckStatus.


        :param health_results: The health_results of this HealthCheckStatus.  # noqa: E501
        :type: list[Health]
        """

        self._health_results = health_results

    @property
    def suppressed_health_results(self):
        """Gets the suppressed_health_results of this HealthCheckStatus.  # noqa: E501


        :return: The suppressed_health_results of this HealthCheckStatus.  # noqa: E501
        :rtype: list[Health]
        """
        return self._suppressed_health_results

    @suppressed_health_results.setter
    def suppressed_health_results(self, suppressed_health_results):
        """Sets the suppressed_health_results of this HealthCheckStatus.


        :param suppressed_health_results: The suppressed_health_results of this HealthCheckStatus.  # noqa: E501
        :type: list[Health]
        """

        self._suppressed_health_results = suppressed_health_results

    @property
    def healthy(self):
        """Gets the healthy of this HealthCheckStatus.  # noqa: E501


        :return: The healthy of this HealthCheckStatus.  # noqa: E501
        :rtype: bool
        """
        return self._healthy

    @healthy.setter
    def healthy(self, healthy):
        """Sets the healthy of this HealthCheckStatus.


        :param healthy: The healthy of this HealthCheckStatus.  # noqa: E501
        :type: bool
        """

        self._healthy = healthy

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
        if issubclass(HealthCheckStatus, dict):
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
        if not isinstance(other, HealthCheckStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
