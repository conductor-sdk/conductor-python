import pprint
import re  # noqa: F401

import six

class SearchResultWorkflow(object):
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
        'results': 'list[Workflow]',
        'total_hits': 'int'
    }

    attribute_map = {
        'results': 'results',
        'total_hits': 'totalHits'
    }

    def __init__(self, results=None, total_hits=None):  # noqa: E501
        """SearchResultWorkflow - a model defined in Swagger"""  # noqa: E501
        self._results = None
        self._total_hits = None
        self.discriminator = None
        if results is not None:
            self.results = results
        if total_hits is not None:
            self.total_hits = total_hits

    @property
    def results(self):
        """Gets the results of this SearchResultWorkflow.  # noqa: E501


        :return: The results of this SearchResultWorkflow.  # noqa: E501
        :rtype: list[Workflow]
        """
        return self._results

    @results.setter
    def results(self, results):
        """Sets the results of this SearchResultWorkflow.


        :param results: The results of this SearchResultWorkflow.  # noqa: E501
        :type: list[Workflow]
        """

        self._results = results

    @property
    def total_hits(self):
        """Gets the total_hits of this SearchResultWorkflow.  # noqa: E501


        :return: The total_hits of this SearchResultWorkflow.  # noqa: E501
        :rtype: int
        """
        return self._total_hits

    @total_hits.setter
    def total_hits(self, total_hits):
        """Sets the total_hits of this SearchResultWorkflow.


        :param total_hits: The total_hits of this SearchResultWorkflow.  # noqa: E501
        :type: int
        """

        self._total_hits = total_hits

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
        if issubclass(SearchResultWorkflow, dict):
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
        if not isinstance(other, SearchResultWorkflow):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
