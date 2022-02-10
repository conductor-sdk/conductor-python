function create_task_definition ()
{
    echo "create task definition"
    return $(curl -X 'POST' \
        'http://localhost:8080/api/metadata/taskdefs' \
        -H 'accept: */*' \
        -H 'Content-Type: application/json' \
        -s \
        -d '[{
            "name": "simple_python_worker",
            "description": "Simple Python Worker",
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
            "name": "simple_workflow_with_python_worker",
            "description": "Simple Workflow with Python Worker",
            "version": 1,
            "tasks": [
            {
                "name": "simple_python_worker",
                "taskReferenceName": "simple_python_worker_ref_1",
                "inputParameters": {},
                "type": "SIMPLE"
            }
            ],
            "inputParameters": [],
            "outputParameters": {
            "workerOutput": "${simple_python_worker_ref_1.output}"
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
        'http://localhost:8080/api/workflow/simple_workflow_with_python_worker' \
        -H 'accept: text/plain' \
        -H 'Content-Type: application/json' \
        -s \
        -d '{}'
    )
}

create_task_definition;
create_workflow_definition;

workflow_id='none'

for idx in {1..100}; do
    generate_workflow;
    echo "workflow_id=$?";
done
