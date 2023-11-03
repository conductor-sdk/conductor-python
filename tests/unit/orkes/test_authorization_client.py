import logging
import unittest

from unittest.mock import Mock, patch, MagicMock
from conductor.client.http.rest import ApiException
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.user_resource_api import UserResourceApi
from conductor.client.http.api.group_resource_api import GroupResourceApi
from conductor.client.http.api.application_resource_api import ApplicationResourceApi
from conductor.client.http.api.authorization_resource_api import AuthorizationResourceApi
from conductor.client.http.models.upsert_user_request import UpsertUserRequest
from conductor.client.http.models.upsert_group_request import UpsertGroupRequest
from conductor.client.http.models.authorization_request import AuthorizationRequest
from conductor.client.http.models.role import Role
from conductor.client.http.models.group import Group
from conductor.client.http.models.permission import Permission
from conductor.client.http.models.subject_ref import SubjectRef, SubjectType
from conductor.client.http.models.target_ref import TargetRef, TargetType
from conductor.client.http.models.conductor_user import ConductorUser
from conductor.client.http.models.conductor_application import ConductorApplication
from conductor.client.http.models.create_or_update_application_request import CreateOrUpdateApplicationRequest
from conductor.client.orkes.models.access_type import AccessType
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.orkes_authorization_client import OrkesAuthorizationClient

APP_ID = 'c6e75472'
APP_NAME = 'ut_application_name'
USER_ID = 'us_user@orkes.io'
USER_UUID = 'ac8b5803-c391-4237-8d3d-90f74b07d5ad'
USER_NAME = 'UT USER'
GROUP_ID = 'ut_group'
GROUP_NAME = 'Test Group'
ERROR_BODY= '{"message":"No such application found by id"}'

class TestOrkesAuthorizationClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.authorization_client = OrkesAuthorizationClient(configuration)
        cls.conductor_application = ConductorApplication(APP_ID, APP_NAME)
        cls.roles = [
            Role(
                "USER", [
                    Permission(name="METADATA_MANAGEMENT"),
                    Permission(name="WORKFLOW_MANAGEMENT"),
                    Permission(name="METADATA_VIEW")
                ]
            )
        ]
        cls.conductor_user = ConductorUser(
            id=USER_ID,
            name=USER_NAME,
            uuid=USER_UUID,
            roles=cls.roles,
            application_user=False,
            encrypted_id=False,
            encrypted_id_display_value=USER_ID
        )
        cls.group_roles =  [
            Role(
                "USER", [
                    Permission(name="CREATE_TASK_DEF"),
                    Permission(name="CREATE_WORKFLOW_DEF"),
                    Permission(name="WORKFLOW_SEARCH")
                ]
            )
        ]
        cls.conductor_group = Group(GROUP_ID, GROUP_NAME, cls.group_roles)
        
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_init(self):
        message = "applicationResourceApi is not of type ApplicationResourceApi"
        self.assertIsInstance(self.authorization_client.applicationResourceApi, ApplicationResourceApi, message)
        message = "userResourceApi is not of type UserResourceApi"
        self.assertIsInstance(self.authorization_client.userResourceApi, UserResourceApi, message)
        message = "groupResourceApi is not of type GroupResourceApi"
        self.assertIsInstance(self.authorization_client.groupResourceApi, GroupResourceApi, message)
        message = "authorizationResourceApi is not of type AuthorizationResourceApi"
        self.assertIsInstance(self.authorization_client.authorizationResourceApi, AuthorizationResourceApi, message)

    @patch.object(ApplicationResourceApi, 'create_application')
    def test_createApplication(self, mock):
        createReq = CreateOrUpdateApplicationRequest()
        mock.return_value = self.conductor_application
        app = self.authorization_client.createApplication(createReq)
        self.assertEqual(app, self.conductor_application)
        mock.assert_called_with(createReq)

    @patch.object(ApplicationResourceApi, 'get_application')
    def test_getApplication(self, mock):
        mock.return_value = self.conductor_application
        app = self.authorization_client.getApplication(APP_ID)
        mock.assert_called_with(APP_ID)
        self.assertEqual(app, self.conductor_application)

    @patch.object(ApplicationResourceApi, 'list_applications')
    def test_listApplications(self, mock):
        mock.return_value = [self.conductor_application]
        app_names = self.authorization_client.listApplications()
        self.assertTrue(mock.called)
        self.assertListEqual(app_names, [self.conductor_application])
    
    @patch.object(ApplicationResourceApi, 'delete_application')
    def test_deleteApplication(self, mock):
        self.authorization_client.deleteApplication(APP_ID)
        mock.assert_called_with(APP_ID)

    @patch.object(ApplicationResourceApi, 'update_application')
    def test_updateApplication(self, mock):
        updateReq = CreateOrUpdateApplicationRequest(APP_NAME)
        mock.return_value = self.conductor_application
        app = self.authorization_client.updateApplication(updateReq, APP_ID)
        self.assertEqual(app, self.conductor_application)
        mock.assert_called_with(updateReq, APP_ID)

    @patch.object(ApplicationResourceApi, 'add_role_to_application_user')
    def test_addRoleToApplicationUser(self, mock):
        self.authorization_client.addRoleToApplicationUser(APP_ID, "USER")
        mock.assert_called_with(APP_ID, "USER")

    @patch.object(ApplicationResourceApi, 'remove_role_from_application_user')
    def test_removeRoleFromApplicationUser(self, mock):
        self.authorization_client.removeRoleFromApplicationUser(APP_ID, "USER")
        mock.assert_called_with(APP_ID, "USER")

    @patch.object(ApplicationResourceApi, 'put_tags_for_application')
    def test_setApplicationTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag2 = MetadataTag("tag2", "val2")
        tags = [tag1, tag2]
        self.authorization_client.setApplicationTags(tags, APP_ID)
        mock.assert_called_with(tags, APP_ID)
        
    @patch.object(ApplicationResourceApi, 'get_tags_for_application')
    def test_getApplicationTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag1 = MetadataTag("tag2", "val2")
        mock.return_value = [tag1, tag1]
        tags = self.authorization_client.getApplicationTags(APP_ID)
        mock.assert_called_with(APP_ID)
        self.assertEqual(len(tags), 2)
    
    @patch.object(ApplicationResourceApi, 'delete_tags_for_application')
    def test_deleteApplicationTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag2 = MetadataTag("tag2", "val2")
        tags = [tag1, tag2]
        self.authorization_client.deleteApplicationTags(tags, APP_ID)
        mock.assert_called_with(tags, APP_ID)
    
    @patch.object(UserResourceApi, 'upsert_user')
    def test_upsertUser(self, mock):
        upsertReq = UpsertUserRequest(USER_NAME, ["ADMIN"])
        mock.return_value = self.conductor_user.to_dict()
        user = self.authorization_client.upsertUser(upsertReq, USER_ID)
        mock.assert_called_with(upsertReq, USER_ID)
        self.assertEqual(user.name, USER_NAME)
        self.assertEqual(user.id, USER_ID)
        self.assertEqual(user.uuid, USER_UUID)
        self.assertEqual(user.roles, self.roles)

    @patch.object(UserResourceApi, 'get_user')
    def test_getUser(self, mock):
        mock.return_value = self.conductor_user.to_dict()
        user = self.authorization_client.getUser(USER_ID)
        mock.assert_called_with(USER_ID)
        self.assertEqual(user.name, USER_NAME)
        self.assertEqual(user.id, USER_ID)
        self.assertEqual(user.uuid, USER_UUID)
        self.assertEqual(user.roles, self.roles)

    @patch.object(UserResourceApi, 'list_users')
    def test_listUsers_with_apps(self, mock):
        mock.return_value = [self.conductor_user]
        users = self.authorization_client.listUsers(apps=True)
        mock.assert_called_with(apps=True)
        self.assertListEqual(users, [self.conductor_user])

    @patch.object(UserResourceApi, 'list_users')
    def test_listUsers(self, mock):
        mock.return_value = [self.conductor_user]
        users = self.authorization_client.listUsers()
        mock.assert_called_with(apps=False)
        self.assertListEqual(users, [self.conductor_user])

    @patch.object(UserResourceApi, 'delete_user')
    def test_deleteUser(self, mock):
        self.authorization_client.deleteUser(USER_ID)
        mock.assert_called_with(USER_ID)

    @patch.object(GroupResourceApi, 'upsert_group')
    def test_upsertGroup(self, mock):
        upsertReq = UpsertGroupRequest(GROUP_NAME, ["USER"])
        mock.return_value = self.conductor_group.to_dict()
        group = self.authorization_client.upsertGroup(upsertReq, GROUP_ID)
        mock.assert_called_with(upsertReq, GROUP_ID)
        self.assertEqual(group, self.conductor_group)
        self.assertEqual(group.description, GROUP_NAME)
        self.assertEqual(group.id, GROUP_ID)
        self.assertEqual(group.roles, self.group_roles)

    @patch.object(GroupResourceApi, 'get_group')
    def test_getGroup(self, mock):
        mock.return_value = self.conductor_group.to_dict()
        group = self.authorization_client.getGroup(GROUP_ID)
        mock.assert_called_with(GROUP_ID)
        self.assertEqual(group, self.conductor_group)
        self.assertEqual(group.description, GROUP_NAME)
        self.assertEqual(group.id, GROUP_ID)
        self.assertEqual(group.roles, self.group_roles)

    @patch.object(GroupResourceApi, 'list_groups')
    def test_listGroups(self, mock):
        mock.return_value = [self.conductor_group]
        groups = self.authorization_client.listGroups()
        self.assertTrue(mock.called)
        self.assertListEqual(groups, [self.conductor_group])

    @patch.object(GroupResourceApi, 'delete_group')
    def test_deleteGroup(self, mock):
        self.authorization_client.deleteGroup(GROUP_ID)
        mock.assert_called_with(GROUP_ID)
    
    @patch.object(GroupResourceApi, 'add_user_to_group')
    def test_addUserToGroup(self, mock):
        mock.return_value = self.conductor_group
        self.authorization_client.addUserToGroup(GROUP_ID, USER_ID)
        mock.assert_called_with(GROUP_ID, USER_ID)

    @patch.object(GroupResourceApi, 'get_users_in_group')
    def test_getUsersInGroup(self, mock):
        mock.return_value = [self.conductor_user.to_dict()]
        users = self.authorization_client.getUsersInGroup(GROUP_ID)
        mock.assert_called_with(GROUP_ID)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, USER_NAME)
        self.assertEqual(users[0].id, USER_ID)
        self.assertEqual(users[0].uuid, USER_UUID)
        self.assertEqual(users[0].roles, self.roles)

    @patch.object(GroupResourceApi, 'remove_user_from_group')
    def test_removeUserFromGroup(self, mock):
        self.authorization_client.removeUserFromGroup(GROUP_ID, USER_ID)
        mock.assert_called_with(GROUP_ID, USER_ID)
        
    # @patch.object(GroupResourceApi, 'get_granted_permissions1')
    # def test_getGrantedPermissionsForGroup(self, mock):
    #     self.authorization_client.getGrantedPermissionsForGroup(GROUP_ID)
    #     mock.assert_called_with(GROUP_ID)
    
    @patch.object(AuthorizationResourceApi, 'get_permissions')
    def test_getPermissions(self, mock):
        mock.return_value = {
            "EXECUTE": [
                { "type": "USER", "id": USER_ID },
            ],
            "READ": [
                { "type": "USER", "id": USER_ID },
                { "type": "GROUP", "id": GROUP_ID }
            ]
        }
        permissions = self.authorization_client.getPermissions(
            TargetRef(TargetType.WORKFLOW_DEF, "workflow_name")
        )
        mock.assert_called_with(TargetType.WORKFLOW_DEF.name, "workflow_name")
        expected_permissions_dict = {
            AccessType.EXECUTE.name: [
                SubjectRef(SubjectType.USER, USER_ID),
            ],
            AccessType.READ.name: [
                SubjectRef(SubjectType.USER, USER_ID),
                SubjectRef(SubjectType.GROUP, GROUP_ID)
            ]
        }
        self.assertDictEqual(permissions, expected_permissions_dict)

    @patch.object(AuthorizationResourceApi, 'grant_permissions')
    def test_grantPermissions(self, mock):
        subject = SubjectRef(SubjectType.USER, USER_ID)
        target = TargetRef(TargetType.WORKFLOW_DEF, "workflow_name")
        access = [AccessType.READ, AccessType.EXECUTE]
        self.authorization_client.grantPermissions(subject, target, access)
        mock.assert_called_with(AuthorizationRequest(subject, target, access))

    @patch.object(AuthorizationResourceApi, 'remove_permissions')
    def test_removePermissions(self, mock):
        subject = SubjectRef(SubjectType.USER, USER_ID)
        target = TargetRef(TargetType.WORKFLOW_DEF, "workflow_name")
        access = [AccessType.READ, AccessType.EXECUTE]
        self.authorization_client.removePermissions(subject, target, access)
        mock.assert_called_with(AuthorizationRequest(subject, target, access))
