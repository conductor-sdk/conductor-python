import logging
import unittest
import json

from unittest.mock import patch, MagicMock
from conductor.client.http.rest import ApiException
from conductor.client.orkes.orkes_scheduler_client import OrkesSchedulerClient
from conductor.client.http.api.scheduler_resource_api import SchedulerResourceApi
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.workflow_schedule import WorkflowSchedule
from conductor.client.http.models.save_schedule_request import SaveScheduleRequest
from conductor.client.http.models.search_result_workflow_schedule_execution_model import SearchResultWorkflowScheduleExecutionModel
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.exceptions.api_error import APIError

SCHEDULE_NAME = 'ut_schedule'
WORKFLOW_NAME = 'ut_wf'
ERROR_BODY= '{"message":"No such schedule found by name"}'

class TestOrkesSchedulerClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.scheduler_client = OrkesSchedulerClient(configuration)
        
    def setUp(self):
        self.workflowSchedule = WorkflowSchedule(name=SCHEDULE_NAME)
        self.saveScheduleRequest = SaveScheduleRequest(name=SCHEDULE_NAME)
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "schedulerResourceApi is not of type SchedulerResourceApi"
        self.assertIsInstance(self.scheduler_client.schedulerResourceApi, SchedulerResourceApi, message)

    @patch.object(SchedulerResourceApi, 'save_schedule')
    def test_saveSchedule(self, mock):
        self.scheduler_client.saveSchedule(self.saveScheduleRequest)
        self.assertTrue(mock.called)
        mock.assert_called_with(self.saveScheduleRequest)

    @patch.object(SchedulerResourceApi, 'get_schedule')
    def test_getSchedule(self, mock):
        mock.return_value = self.workflowSchedule
        schedule = self.scheduler_client.getSchedule(SCHEDULE_NAME)
        self.assertEqual(schedule, self.workflowSchedule)
        self.assertTrue(mock.called)
        mock.assert_called_with(SCHEDULE_NAME)

    @patch.object(SchedulerResourceApi, 'get_schedule')
    def test_getSchedule_non_existing(self, mock):
        error_body = { 'status': 404, 'message': 'Schedule not found' }
        mock.side_effect = MagicMock(side_effect=ApiException(body=json.dumps(error_body)))
        with self.assertRaises(APIError):
            self.scheduler_client.getSchedule("WRONG_SCHEDULE")
            mock.assert_called_with("WRONG_SCHEDULE")
        
    @patch.object(SchedulerResourceApi, 'get_all_schedules')
    def test_getAllSchedules(self, mock):
        mock.return_value = [self.workflowSchedule]
        schedules = self.scheduler_client.getAllSchedules()
        self.assertEqual(schedules, [self.workflowSchedule])
        self.assertTrue(mock.called)
    
    @patch.object(SchedulerResourceApi, 'get_all_schedules')
    def test_getAllSchedules_with_workflow_name(self, mock):
        mock.return_value = [self.workflowSchedule]
        schedules = self.scheduler_client.getAllSchedules(WORKFLOW_NAME)
        self.assertEqual(schedules, [self.workflowSchedule])
        mock.assert_called_with(workflow_name=WORKFLOW_NAME)
    
    @patch.object(SchedulerResourceApi, 'get_next_few_schedules')
    def test_getNextFewScheduleExecutionTimes(self, mock):
        cronExpression = "0 */5 * ? * *"
        mock.return_value = [1698093000000, 1698093300000, 1698093600000]
        times = self.scheduler_client.getNextFewScheduleExecutionTimes(cronExpression)
        self.assertEqual(len(times), 3)
        mock.assert_called_with(cronExpression)
    
    @patch.object(SchedulerResourceApi, 'get_next_few_schedules')
    def test_getNextFewScheduleExecutionTimes_with_optional_params(self, mock):
        cronExpression = "0 */5 * ? * *"
        mock.return_value = [1698093300000, 1698093600000]
        times = self.scheduler_client.getNextFewScheduleExecutionTimes(
            cronExpression, 1698093300000, 1698093600000, 2
        )
        self.assertEqual(len(times), 2)
        mock.assert_called_with(
            cronExpression,
            schedule_start_time=1698093300000,
            schedule_end_time=1698093600000,
            limit=2
        )
    
    @patch.object(SchedulerResourceApi, 'delete_schedule')
    def test_deleteSchedule(self, mock):
        self.scheduler_client.deleteSchedule(SCHEDULE_NAME)
        mock.assert_called_with(SCHEDULE_NAME)
        
    @patch.object(SchedulerResourceApi, 'pause_schedule')
    def test_pauseSchedule(self, mock):
        self.scheduler_client.pauseSchedule(SCHEDULE_NAME)
        mock.assert_called_with(SCHEDULE_NAME)
        
    @patch.object(SchedulerResourceApi, 'pause_all_schedules')
    def test_pauseAllSchedules(self, mock):
        self.scheduler_client.pauseAllSchedules()
        self.assertTrue(mock.called)
        
    @patch.object(SchedulerResourceApi, 'resume_schedule')
    def test_resumeSchedule(self, mock):
        self.scheduler_client.resumeSchedule(SCHEDULE_NAME)
        mock.assert_called_with(SCHEDULE_NAME)
        
    @patch.object(SchedulerResourceApi, 'resume_all_schedules')
    def test_resumeAllSchedules(self, mock):
        self.scheduler_client.resumeAllSchedules()
        self.assertTrue(mock.called)
        
    @patch.object(SchedulerResourceApi, 'requeue_all_execution_records')
    def test_requeueAllExecutionRecords(self, mock):
        self.scheduler_client.requeueAllExecutionRecords()
        self.assertTrue(mock.called)

    @patch.object(SchedulerResourceApi, 'search_v21')
    def test_searchScheduleExecutions(self, mock):
        srw = SearchResultWorkflowScheduleExecutionModel(total_hits=2)
        mock.return_value = srw
        start = 1698093300000
        sort = "name&sort=workflowId:DESC"
        freeText = "abc"
        query="workflowId=abc"
        searchResult = self.scheduler_client.searchScheduleExecutions(
            start, 2, sort, freeText, query
        )
        mock.assert_called_with(
            start=start,
            size=2,
            sort=sort,
            freeText=freeText,
            query=query
        )
        self.assertEqual(searchResult, srw)
    
    @patch.object(SchedulerResourceApi, 'put_tag_for_schedule')
    def test_setSchedulerTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag2 = MetadataTag("tag2", "val2")
        tags = [tag1, tag2]
        self.scheduler_client.setSchedulerTags(tags, SCHEDULE_NAME)
        mock.assert_called_with(tags, SCHEDULE_NAME)
        
    @patch.object(SchedulerResourceApi, 'get_tags_for_schedule')
    def test_getSchedulerTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag1 = MetadataTag("tag2", "val2")
        mock.return_value = [tag1, tag1]
        tags = self.scheduler_client.getSchedulerTags(SCHEDULE_NAME)
        mock.assert_called_with(SCHEDULE_NAME)
        self.assertEqual(len(tags), 2)
    
    @patch.object(SchedulerResourceApi, 'delete_tag_for_schedule')
    def test_deleteSchedulerTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag2 = MetadataTag("tag2", "val2")
        tags = [tag1, tag2]
        self.scheduler_client.deleteSchedulerTags(tags, SCHEDULE_NAME)
        mock.assert_called_with(tags, SCHEDULE_NAME)