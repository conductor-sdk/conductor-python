from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.orkes.api.tags_api import TagsApi
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.api.user_resource_api import UserResourceApi
from conductor.client.http.api.group_resource_api import GroupResourceApi
from conductor.client.http.api.secret_resource_api import SecretResourceApi
from conductor.client.http.api.application_resource_api import ApplicationResourceApi
from conductor.client.http.api.authorization_resource_api import AuthorizationResourceApi
from conductor.client.http.api.scheduler_resource_api import SchedulerResourceApi

import logging


class OrkesBaseClient(object):
    def __init__(self, configuration: Configuration):
        self.api_client = ApiClient(configuration)
        self.logger = logging.getLogger(
            Configuration.get_logging_formatted_name(__name__)
        )
        self.metadataResourceApi = MetadataResourceApi(self.api_client)
        self.taskResourceApi = TaskResourceApi(self.api_client)
        self.workflowResourceApi = WorkflowResourceApi(self.api_client)
        self.applicationResourceApi = ApplicationResourceApi(self.api_client)
        self.secretResourceApi = SecretResourceApi(self.api_client)
        self.userResourceApi = UserResourceApi(self.api_client)
        self.groupResourceApi = GroupResourceApi(self.api_client)
        self.authorizationResourceApi = AuthorizationResourceApi(self.api_client)
        self.schedulerResourceApi = SchedulerResourceApi(self.api_client)
        self.tagsApi = TagsApi(self.api_client)
