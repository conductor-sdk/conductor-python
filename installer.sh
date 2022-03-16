function create_task_definition ()
{
    echo "create task definition"
    return $(curl -X 'POST' \
        'http://localhost:8080/api/metadata/taskdefs' \
        -H 'accept: */*' \
        -H 'Content-Type: application/json' \
        -s \
        -d '[{
            "name": "python_task_example",
            "description": "Python Task Example",
            "retryCount": 3,
            "retryLogic": "FIXED",
            "retryDelaySeconds": 10,
            "timeoutSeconds": 300,
            "timeoutPolicy": "TIME_OUT_WF",
            "responseTimeoutSeconds": 180,
            "ownerEmail": "example@example.com"
        }]'
    )
}

function create_workflow_definition ()
{
    echo "create workflow definition"
    return $(curl -X 'POST' \
        'http://localhost:8080/api/metadata/workflow' \
        -H 'accept: */*' \
        -H 'Content-Type: application/json' \
        -s \
        -d '{
            "createTime": 1634021619147,
            "updateTime": 1630694890267,
            "name": "workflow_with_python_task_example",
            "description": "Workflow with Python Task example",
            "version": 1,
            "tasks": [
            {
                "name": "python_task_example",
                "taskReferenceName": "python_task_example_ref_0",
                "inputParameters": {},
                "type": "SIMPLE"
            }
            ],
            "inputParameters": [],
            "outputParameters": {
            "workerOutput": "${python_task_example_ref_0.output}"
            },
            "schemaVersion": 2,
            "restartable": true,
            "ownerEmail": "example@example.com",
            "timeoutPolicy": "ALERT_ONLY",
            "timeoutSeconds": 0
        }'
    )
}

function generate_workflow () {
    echo "generate workflow"
    workflow_id=$(curl -X 'POST' \
        'http://localhost:8080/api/workflow/workflow_with_python_task_example' \
        -H 'accept: text/plain' \
        -H 'Content-Type: application/json' \
        -s \
        -d '{}'
    )
}

workflow_id='none';
create_task_definition;
create_workflow_definition;

for idx in {1..500}; do
    generate_workflow;
    echo "workflow_id=${workflow_id}";
done

echo "Delete metrics folder"
rm -rf $METRICS_FOLDER

echo "Create metrics folder"
mkdir -p $METRICS_FOLDER
