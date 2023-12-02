from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient
from conductor.client.orkes.orkes_workflow_client import OrkesWorkflowClient
from conductor.client.orkes.orkes_task_client import OrkesTaskClient
from conductor.client.orkes.orkes_scheduler_client import OrkesSchedulerClient
from conductor.client.orkes.orkes_secret_client import OrkesSecretClient
from conductor.client.orkes.orkes_authorization_client import OrkesAuthorizationClient

class OrkesClients:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        
    def get_workflow_client(self) -> OrkesWorkflowClient:
        return OrkesWorkflowClient(self.configuration)

    def get_authorization_client(self) -> OrkesAuthorizationClient:
        return OrkesAuthorizationClient(self.configuration)

    def get_metadata_client(self) -> OrkesMetadataClient:
        return OrkesMetadataClient(self.configuration)
    
    def get_scheduler_client(self) -> OrkesSchedulerClient:
        return OrkesSchedulerClient(self.configuration)
    
    def get_secret_client(self) -> OrkesSecretClient:
        return OrkesSecretClient(self.configuration)
    
    def get_task_client(self) -> OrkesTaskClient:
        return OrkesTaskClient(self.configuration)
    
    