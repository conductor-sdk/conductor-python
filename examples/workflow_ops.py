from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import StartWorkflowRequest
from conductor.client.orkes_clients import OrkesClients


def main():
    api_config = Configuration()
    clients = OrkesClients(configuration=api_config)
    workflow_client = clients.get_workflow_client()

    request = StartWorkflowRequest()
    request.name = 'hello'
    request.version = 1
    request.input = {'name': 'Orkes'}
    workflow_run = workflow_client.execute_workflow(
        start_workflow_request=request,
        wait_for_seconds=12)




if __name__ == '__main__':
    main()
