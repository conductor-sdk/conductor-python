# WorkflowTask

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**task_reference_name** | **str** |  | 
**description** | **str** |  | [optional] 
**input_parameters** | **dict(str, object)** |  | [optional] 
**type** | **str** |  | [optional] 
**dynamic_task_name_param** | **str** |  | [optional] 
**case_value_param** | **str** |  | [optional] 
**case_expression** | **str** |  | [optional] 
**script_expression** | **str** |  | [optional] 
**decision_cases** | **dict(str, list[WorkflowTask])** |  | [optional] 
**dynamic_fork_join_tasks_param** | **str** |  | [optional] 
**dynamic_fork_tasks_param** | **str** |  | [optional] 
**dynamic_fork_tasks_input_param_name** | **str** |  | [optional] 
**default_case** | [**list[WorkflowTask]**](WorkflowTask.md) |  | [optional] 
**fork_tasks** | **list[list[WorkflowTask]]** |  | [optional] 
**start_delay** | **int** |  | [optional] 
**sub_workflow_param** | [**SubWorkflowParams**](SubWorkflowParams.md) |  | [optional] 
**join_on** | **list[str]** |  | [optional] 
**sink** | **str** |  | [optional] 
**optional** | **bool** |  | [optional] 
**task_definition** | [**TaskDef**](TaskDef.md) |  | [optional] 
**rate_limited** | **bool** |  | [optional] 
**default_exclusive_join_task** | **list[str]** |  | [optional] 
**async_complete** | **bool** |  | [optional] 
**loop_condition** | **str** |  | [optional] 
**loop_over** | [**list[WorkflowTask]**](WorkflowTask.md) |  | [optional] 
**retry_count** | **int** |  | [optional] 
**evaluator_type** | **str** |  | [optional] 
**expression** | **str** |  | [optional] 
**workflow_task_type** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

