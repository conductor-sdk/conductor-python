import logging

from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.application_resource_api import \
    ApplicationResourceApi
from conductor.client.http.api.authorization_resource_api import \
    AuthorizationResourceApi
from conductor.client.http.api.group_resource_api import GroupResourceApi
from conductor.client.http.api.integration_resource_api import \
    IntegrationResourceApi
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.http.api.prompt_resource_api import PromptResourceApi
from conductor.client.http.api.scheduler_resource_api import \
    SchedulerResourceApi
from conductor.client.http.api.secret_resource_api import SecretResourceApi
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.api.user_resource_api import UserResourceApi
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.http.api_client import ApiClient
from conductor.client.orkes.api.tags_api import TagsApi


class OrkesBaseClient:
    def __init__(self, configuration: Configuration):
        self.api_client = ApiClient(configuration)
        self.logger = logging.getLogger(
            Configuration.get_logging_formatted_name(__name__)
        )
        self.metadata_resource_api = MetadataResourceApi(self.api_client)
        self.task_resource_api = TaskResourceApi(self.api_client)
        self.workflow_resource_api = WorkflowResourceApi(self.api_client)
        self.application_resource_api = ApplicationResourceApi(self.api_client)
        self.secret_resource_api = SecretResourceApi(self.api_client)
        self.user_resource_api = UserResourceApi(self.api_client)
        self.group_resource_api = GroupResourceApi(self.api_client)
        self.authorization_resource_api = AuthorizationResourceApi(self.api_client)
        self.scheduler_resource_api = SchedulerResourceApi(self.api_client)
        self.tags_api = TagsApi(self.api_client)
        self.integration_api = IntegrationResourceApi(self.api_client)
        self.prompt_api = PromptResourceApi(self.api_client)
