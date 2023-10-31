# Schedule Management

## Scheduler Client

### Initialization
```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.orkes.orkes_scheduler_client import OrkesSchedulerClient

configuration = Configuration(
    server_api_url=SERVER_API_URL,
    debug=False,
    authentication_settings=AuthenticationSettings(
        key_id=KEY_ID,
        key_secret=KEY_SECRET
    ),
)

scheduler_client = OrkesSchedulerClient(configuration)
```

### Saving Schedule
```python
from conductor.client.http.models.save_schedule_request import SaveScheduleRequest
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest

startWorkflowRequest = StartWorkflowRequest(
    name="WORKFLOW_NAME", workflow_def=workflowDef
)
saveScheduleRequest = SaveScheduleRequest(
    name="SCHEDULE_NAME",
    start_workflow_request=startWorkflowRequest,
    cron_expression= "0 */5 * ? * *"
)

scheduler_client.saveSchedule(saveScheduleRequest)
```

### Get Schedule

#### Get a specific schedule
```python
scheduler_client.getSchedule("SCHEDULE_NAME")
```

#### Get all schedules
```python
scheduler_client.getAllSchedules()
```

#### Get all schedules for a workflow
```python
scheduler_client.getAllSchedules("WORKFLOW_NAME")
```

### Delete Schedule
```python
scheduler_client.deleteSchedule("SCHEDULE_NAME")
```

### Pause and Resume Schedules

#### Pause a schedule
```python
scheduler_client.pauseSchedule("SCHEDULE_NAME")
```

#### Pause all schedules
```python
scheduler_client.pauseAllSchedules()
```

#### Resume a scheduler
```python
scheduler_client.resumeSchedule("SCHEDULE_NAME")
```

#### Resume all schedules
```python
scheduler_client.resumeAllSchedules()
```

### Scheduler Tag Management

#### Set scheduler tags
```python
from conductor.client.orkes.models.metadata_tag import MetadataTag

tags = [
    MetadataTag("sch_tag", "val"), MetadataTag("sch_tag_2", "val2")
]
scheduler_client.setSchedulerTags(tags, "SCHEDULE_NAME")
```

#### Get scheduler tags
```python
tags = scheduler_client.getSchedulerTags("SCHEDULE_NAME")
```

#### Delete scheduler tags
```python
tags = [
    MetadataTag("sch_tag", "val"), MetadataTag("sch_tag_2", "val2")
]
scheduler_client.deleteSchedulerTags(tags, "SCHEDULE_NAME")
```
