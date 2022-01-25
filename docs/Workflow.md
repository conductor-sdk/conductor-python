# Workflow

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**owner_app** | **str** |  | [optional] 
**create_time** | **int** |  | [optional] 
**update_time** | **int** |  | [optional] 
**created_by** | **str** |  | [optional] 
**updated_by** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**end_time** | **int** |  | [optional] 
**workflow_id** | **str** |  | [optional] 
**parent_workflow_id** | **str** |  | [optional] 
**parent_workflow_task_id** | **str** |  | [optional] 
**tasks** | [**list[Task]**](Task.md) |  | [optional] 
**input** | **dict(str, object)** |  | [optional] 
**output** | **dict(str, object)** |  | [optional] 
**correlation_id** | **str** |  | [optional] 
**re_run_from_workflow_id** | **str** |  | [optional] 
**reason_for_incompletion** | **str** |  | [optional] 
**event** | **str** |  | [optional] 
**task_to_domain** | **dict(str, str)** |  | [optional] 
**failed_reference_task_names** | **list[str]** |  | [optional] 
**workflow_definition** | [**WorkflowDef**](WorkflowDef.md) |  | [optional] 
**external_input_payload_storage_path** | **str** |  | [optional] 
**external_output_payload_storage_path** | **str** |  | [optional] 
**priority** | **int** |  | [optional] 
**variables** | **dict(str, object)** |  | [optional] 
**last_retried_time** | **int** |  | [optional] 
**start_time** | **int** |  | [optional] 
**workflow_name** | **str** |  | [optional] 
**workflow_version** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

