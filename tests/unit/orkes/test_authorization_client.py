import logging
import unittest
import json

from unittest.mock import patch
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
from conductor.client.orkes.models.access_key import AccessKey
from conductor.client.orkes.models.access_key_status import AccessKeyStatus
from conductor.client.orkes.models.created_access_key import CreatedAccessKey
from conductor.client.orkes.models.granted_permission import GrantedPermission
from conductor.client.orkes.orkes_authorization_client import OrkesAuthorizationClient

APP_ID = '5d860b70-a429-4b20-8d28-6b5198155882'
APP_NAME = 'ut_application_name'
ACCESS_KEY_ID = '9c32f5b2-128d-42bd-988f-083857f4c541'
ACCESS_KEY_ID_2 = 'be41f18c-be18-4c68-9847-8fd91f3c21bc'
ACCESS_KEY_SECRET = 'iSEONALN8Lz91uXraPBcyEau28luuOtMGnGA7mUSbJTZ76fb'
USER_ID = 'us_user@orkes.io'
USER_UUID = 'ac8b5803-c391-4237-8d3d-90f74b07d5ad'
USER_NAME = 'UT USER'
GROUP_ID = 'ut_group'
GROUP_NAME = 'Test Group'
WF_NAME = 'workflow_name'
ERROR_BODY= '{"message":"No such application found by id"}'

class TestOrkesAuthorizationClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        configuration = Configuration("http://localhost:8080/api")
        cls.authorization_client = OrkesAuthorizationClient(configuration)
        cls.conductor_application = ConductorApplication(APP_ID, APP_NAME, USER_ID)
        cls.access_key = CreatedAccessKey(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        cls.app_keys = [
            AccessKey(ACCESS_KEY_ID, AccessKeyStatus.ACTIVE, 1698926045112),
            AccessKey(ACCESS_KEY_ID_2, AccessKeyStatus.ACTIVE, 1699100552620)
        ]
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
        message = "application_resource_api is not of type ApplicationResourceApi"
        self.assertIsInstance(self.authorization_client.application_resource_api, ApplicationResourceApi, message)
        message = "user_resource_api  is not of type UserResourceApi"
        self.assertIsInstance(self.authorization_client.user_resource_api, UserResourceApi, message)
        message = "group_resource_api  is not of type GroupResourceApi"
        self.assertIsInstance(self.authorization_client.group_resource_api, GroupResourceApi, message)
        message = "authorization_resource_api  is not of type AuthorizationResourceApi"
        self.assertIsInstance(self.authorization_client.authorization_resource_api, AuthorizationResourceApi, message)

    @patch.object(ApplicationResourceApi, 'create_application')
    def test_createApplication(self, mock):
        createReq = CreateOrUpdateApplicationRequest()
        mock.return_value = {
            "id": APP_ID,
            "name": APP_NAME,
            "createdBy": USER_ID,
            "updatedBy": USER_ID,
            "createTime": 1699236095031,
            "updateTime": 1699236095031
        }
        app = self.authorization_client.create_application(createReq)
        mock.assert_called_with(createReq)
        self.assertEqual(app, self.conductor_application)

    @patch.object(ApplicationResourceApi, 'get_application')
    def test_getApplication(self, mock):
        mock.return_value = {
            "id": APP_ID,
            "name": APP_NAME,
            "createdBy": USER_ID,
        }
        app = self.authorization_client.get_application(APP_ID)
        mock.assert_called_with(APP_ID)
        self.assertEqual(app, self.conductor_application)

    @patch.object(ApplicationResourceApi, 'list_applications')
    def test_listApplications(self, mock):
        mock.return_value = [self.conductor_application]
        app_names = self.authorization_client.list_applications()
        self.assertTrue(mock.called)
        self.assertListEqual(app_names, [self.conductor_application])
    
    @patch.object(ApplicationResourceApi, 'delete_application')
    def test_deleteApplication(self, mock):
        self.authorization_client.delete_application(APP_ID)
        mock.assert_called_with(APP_ID)

    @patch.object(ApplicationResourceApi, 'update_application')
    def test_updateApplication(self, mock):
        updateReq = CreateOrUpdateApplicationRequest(APP_NAME)
        mock.return_value = {
            "id": APP_ID,
            "name": APP_NAME,
            "createdBy": USER_ID,
            "updatedBy": USER_ID,
            "createTime": 1699236095031,
            "updateTime": 1699236095031
        }
        app = self.authorization_client.update_application(updateReq, APP_ID)
        self.assertEqual(app, self.conductor_application)
        mock.assert_called_with(updateReq, APP_ID)

    @patch.object(ApplicationResourceApi, 'add_role_to_application_user')
    def test_addRoleToApplicationUser(self, mock):
        self.authorization_client.add_role_to_application_user(APP_ID, "USER")
        mock.assert_called_with(APP_ID, "USER")

    @patch.object(ApplicationResourceApi, 'remove_role_from_application_user')
    def test_removeRoleFromApplicationUser(self, mock):
        self.authorization_client.remove_role_from_application_user(APP_ID, "USER")
        mock.assert_called_with(APP_ID, "USER")

    @patch.object(ApplicationResourceApi, 'put_tags_for_application')
    def test_setApplicationTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag2 = MetadataTag("tag2", "val2")
        tags = [tag1, tag2]
        self.authorization_client.set_application_tags(tags, APP_ID)
        mock.assert_called_with(tags, APP_ID)
        
    @patch.object(ApplicationResourceApi, 'get_tags_for_application')
    def test_getApplicationTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag1 = MetadataTag("tag2", "val2")
        mock.return_value = [tag1, tag1]
        tags = self.authorization_client.get_application_tags(APP_ID)
        mock.assert_called_with(APP_ID)
        self.assertEqual(len(tags), 2)
    
    @patch.object(ApplicationResourceApi, 'delete_tags_for_application')
    def test_deleteApplicationTags(self, mock):
        tag1 = MetadataTag("tag1", "val1")
        tag2 = MetadataTag("tag2", "val2")
        tags = [tag1, tag2]
        self.authorization_client.delete_application_tags(tags, APP_ID)
        mock.assert_called_with(tags, APP_ID)

    @patch.object(ApplicationResourceApi, 'create_access_key')
    def test_createAccessKey(self, mock):
        mock.return_value = {
            "id": ACCESS_KEY_ID,
            "secret": ACCESS_KEY_SECRET
        }
        created_key = self.authorization_client.create_access_key(APP_ID)
        mock.assert_called_with(APP_ID)
        self.assertEqual(created_key, self.access_key)

    @patch.object(ApplicationResourceApi, 'get_access_keys')
    def test_getAccessKeys(self, mock):
        mock.return_value = [
            {
                "id": ACCESS_KEY_ID,
                "createdAt": 1698926045112,
                "status": "ACTIVE"
            },
            {
                "id": ACCESS_KEY_ID_2,
                "createdAt": 1699100552620,
                "status": "ACTIVE"
            }
        ]
        access_keys = self.authorization_client.get_access_keys(APP_ID)
        mock.assert_called_with(APP_ID)
        self.assertListEqual(access_keys, self.app_keys)
    
    @patch.object(ApplicationResourceApi, 'toggle_access_key_status')
    def test_toggleAccessKeyStatus(self, mock):
        mock.return_value = {
            "id": ACCESS_KEY_ID,
            "createdAt": 1698926045112,
            "status": "INACTIVE"
        }
        access_key = self.authorization_client.toggle_access_key_status(APP_ID, ACCESS_KEY_ID)
        mock.assert_called_with(APP_ID, ACCESS_KEY_ID)
        self.assertEqual(access_key.status, AccessKeyStatus.INACTIVE)
        
    @patch.object(ApplicationResourceApi, 'delete_access_key')
    def test_deleteAccessKey(self, mock):
        self.authorization_client.delete_access_key(APP_ID, ACCESS_KEY_ID)
        mock.assert_called_with(APP_ID, ACCESS_KEY_ID)

    @patch.object(UserResourceApi, 'upsert_user')
    def test_upsertUser(self, mock):
        upsertReq = UpsertUserRequest(USER_NAME, ["ADMIN"])
        mock.return_value = self.conductor_user.to_dict()
        user = self.authorization_client.upsert_user(upsertReq, USER_ID)
        mock.assert_called_with(upsertReq, USER_ID)
        self.assertEqual(user.name, USER_NAME)
        self.assertEqual(user.id, USER_ID)
        self.assertEqual(user.uuid, USER_UUID)
        self.assertEqual(user.roles, self.roles)

    @patch.object(UserResourceApi, 'get_user')
    def test_getUser(self, mock):
        mock.return_value = self.conductor_user.to_dict()
        user = self.authorization_client.get_user(USER_ID)
        mock.assert_called_with(USER_ID)
        self.assertEqual(user.name, USER_NAME)
        self.assertEqual(user.id, USER_ID)
        self.assertEqual(user.uuid, USER_UUID)
        self.assertEqual(user.roles, self.roles)

    @patch.object(UserResourceApi, 'list_users')
    def test_listUsers_with_apps(self, mock):
        mock.return_value = [self.conductor_user]
        users = self.authorization_client.list_users(apps=True)
        mock.assert_called_with(apps=True)
        self.assertListEqual(users, [self.conductor_user])

    @patch.object(UserResourceApi, 'list_users')
    def test_listUsers(self, mock):
        mock.return_value = [self.conductor_user]
        users = self.authorization_client.list_users()
        mock.assert_called_with(apps=False)
        self.assertListEqual(users, [self.conductor_user])

    @patch.object(UserResourceApi, 'delete_user')
    def test_deleteUser(self, mock):
        self.authorization_client.delete_user(USER_ID)
        mock.assert_called_with(USER_ID)

    @patch.object(GroupResourceApi, 'upsert_group')
    def test_upsertGroup(self, mock):
        upsertReq = UpsertGroupRequest(GROUP_NAME, ["USER"])
        mock.return_value = self.conductor_group.to_dict()
        group = self.authorization_client.upsert_group(upsertReq, GROUP_ID)
        mock.assert_called_with(upsertReq, GROUP_ID)
        self.assertEqual(group, self.conductor_group)
        self.assertEqual(group.description, GROUP_NAME)
        self.assertEqual(group.id, GROUP_ID)
        self.assertEqual(group.roles, self.group_roles)

    @patch.object(GroupResourceApi, 'get_group')
    def test_getGroup(self, mock):
        mock.return_value = self.conductor_group.to_dict()
        group = self.authorization_client.get_group(GROUP_ID)
        mock.assert_called_with(GROUP_ID)
        self.assertEqual(group, self.conductor_group)
        self.assertEqual(group.description, GROUP_NAME)
        self.assertEqual(group.id, GROUP_ID)
        self.assertEqual(group.roles, self.group_roles)

    @patch.object(GroupResourceApi, 'list_groups')
    def test_listGroups(self, mock):
        mock.return_value = [self.conductor_group]
        groups = self.authorization_client.list_groups()
        self.assertTrue(mock.called)
        self.assertListEqual(groups, [self.conductor_group])

    @patch.object(GroupResourceApi, 'delete_group')
    def test_deleteGroup(self, mock):
        self.authorization_client.delete_group(GROUP_ID)
        mock.assert_called_with(GROUP_ID)
    
    @patch.object(GroupResourceApi, 'add_user_to_group')
    def test_addUserToGroup(self, mock):
        mock.return_value = self.conductor_group
        self.authorization_client.add_user_to_group(GROUP_ID, USER_ID)
        mock.assert_called_with(GROUP_ID, USER_ID)

    @patch.object(GroupResourceApi, 'get_users_in_group')
    def test_getUsersInGroup(self, mock):
        mock.return_value = [self.conductor_user.to_dict()]
        users = self.authorization_client.get_users_in_group(GROUP_ID)
        mock.assert_called_with(GROUP_ID)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, USER_NAME)
        self.assertEqual(users[0].id, USER_ID)
        self.assertEqual(users[0].uuid, USER_UUID)
        self.assertEqual(users[0].roles, self.roles)

    @patch.object(GroupResourceApi, 'remove_user_from_group')
    def test_removeUserFromGroup(self, mock):
        self.authorization_client.remove_user_from_group(GROUP_ID, USER_ID)
        mock.assert_called_with(GROUP_ID, USER_ID)
        
    @patch.object(GroupResourceApi, 'get_granted_permissions1')
    def test_getGrantedPermissionsForGroup(self, mock):
        mock.return_value = {
            "grantedAccess": [
                {
                    "target": {
                        "type": "WORKFLOW_DEF",
                        "id": WF_NAME
                    },
                    "access": [
                        "EXECUTE",
                        "UPDATE",
                        "READ"
                    ]
                }
            ]
        }
        perms = self.authorization_client.get_granted_permissions_for_group(GROUP_ID)
        mock.assert_called_with(GROUP_ID)
        expected_perm = GrantedPermission(
            target=TargetRef(TargetType.WORKFLOW_DEF, WF_NAME),
            access = ["EXECUTE", "UPDATE", "READ"]
        )
        self.assertEqual(perms, [expected_perm])

    @patch.object(UserResourceApi, 'get_granted_permissions')
    def test_getGrantedPermissionsForUser(self, mock):
        mock.return_value = {
            "grantedAccess": [
                {
                    "target": {
                        "type": "WORKFLOW_DEF",
                        "id": WF_NAME
                    },
                    "access": [
                        "EXECUTE",
                        "UPDATE",
                        "READ"
                    ]
                }
            ]
        }
        perms = self.authorization_client.get_granted_permissions_for_user(USER_ID)
        mock.assert_called_with(USER_ID)
        expected_perm = GrantedPermission(
            target=TargetRef(TargetType.WORKFLOW_DEF, WF_NAME),
            access = ["EXECUTE", "UPDATE", "READ"]
        )
        self.assertEqual(perms, [expected_perm])

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
        permissions = self.authorization_client.get_permissions(
            TargetRef(TargetType.WORKFLOW_DEF, WF_NAME)
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
        target = TargetRef(TargetType.WORKFLOW_DEF, WF_NAME)
        access = [AccessType.READ, AccessType.EXECUTE]
        self.authorization_client.grant_permissions(subject, target, access)
        mock.assert_called_with(AuthorizationRequest(subject, target, access))

    @patch.object(AuthorizationResourceApi, 'remove_permissions')
    def test_removePermissions(self, mock):
        subject = SubjectRef(SubjectType.USER, USER_ID)
        target = TargetRef(TargetType.WORKFLOW_DEF, WF_NAME)
        access = [AccessType.READ, AccessType.EXECUTE]
        self.authorization_client.remove_permissions(subject, target, access)
        mock.assert_called_with(AuthorizationRequest(subject, target, access))
