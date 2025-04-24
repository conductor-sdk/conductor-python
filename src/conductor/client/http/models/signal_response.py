import pprint
import six

class SignalResponse(object):
    """Base class for workflow signal responses"""

    swagger_types = {
        'response_type': 'str',
        'target_workflow_id': 'str',
        'target_workflow_status': 'str',
        'request_id': 'str',
        'workflow_id': 'str',
        'correlation_id': 'str',
        'input': 'dict(str, object)',
        'output': 'dict(str, object)'
    }

    attribute_map = {
        'response_type': 'responseType',
        'target_workflow_id': 'targetWorkflowId',
        'target_workflow_status': 'targetWorkflowStatus',
        'request_id': 'requestId',
        'workflow_id': 'workflowId',
        'correlation_id': 'correlationId',
        'input': 'input',
        'output': 'output'
    }

    def __init__(self, response_type=None, target_workflow_id=None, target_workflow_status=None,
                 request_id=None, workflow_id=None, correlation_id=None, input=None, output=None):
        self._response_type = None
        self._target_workflow_id = None
        self._target_workflow_status = None
        self._request_id = None
        self._workflow_id = None
        self._correlation_id = None
        self._input = None
        self._output = None
        self.discriminator = None

        if response_type is not None:
            self.response_type = response_type
        if target_workflow_id is not None:
            self.target_workflow_id = target_workflow_id
        if target_workflow_status is not None:
            self.target_workflow_status = target_workflow_status
        if request_id is not None:
            self.request_id = request_id
        if workflow_id is not None:
            self.workflow_id = workflow_id
        if correlation_id is not None:
            self.correlation_id = correlation_id
        if input is not None:
            self.input = input
        if output is not None:
            self.output = output

    @property
    def response_type(self):
        return self._response_type

    @response_type.setter
    def response_type(self, response_type):
        self._response_type = response_type

    @property
    def target_workflow_id(self):
        return self._target_workflow_id

    @target_workflow_id.setter
    def target_workflow_id(self, target_workflow_id):
        self._target_workflow_id = target_workflow_id

    @property
    def target_workflow_status(self):
        return self._target_workflow_status

    @target_workflow_status.setter
    def target_workflow_status(self, target_workflow_status):
        self._target_workflow_status = target_workflow_status

    @property
    def request_id(self):
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        self._request_id = request_id

    @property
    def workflow_id(self):
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        self._workflow_id = workflow_id

    @property
    def correlation_id(self):
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        self._correlation_id = correlation_id

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, input):
        self._input = input

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, output):
        self._output = output

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
        if issubclass(SignalResponse, dict):
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
        if not isinstance(other, SignalResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other