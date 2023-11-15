from typing import Dict, List, Optional
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.models.access_type import AccessType
from conductor.client.orkes.models.granted_permission import GrantedPermission
from conductor.client.orkes.models.access_key import AccessKey
from conductor.client.orkes.models.created_access_key import CreatedAccessKey
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.group import Group
from conductor.client.http.models.subject_ref import SubjectRef
from conductor.client.http.models.conductor_user import ConductorUser
from conductor.client.http.models.target_ref import TargetRef
from conductor.client.http.models.conductor_application import ConductorApplication
from conductor.client.http.models.upsert_user_request import UpsertUserRequest
from conductor.client.http.models.upsert_group_request import UpsertGroupRequest
from conductor.client.http.models.authorization_request import AuthorizationRequest
from conductor.client.http.models.create_or_update_application_request import CreateOrUpdateApplicationRequest
from conductor.client.authorization_client import AuthorizationClient
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.exceptions.api_exception_handler import api_exception_handler, for_all_methods

@for_all_methods(api_exception_handler, ["__init__"])
class OrkesAuthorizationClient(OrkesBaseClient, AuthorizationClient):
    def __init__(self, configuration: Configuration):
        super(OrkesAuthorizationClient, self).__init__(configuration)

    # Applications
    def createApplication(
        self,
        createOrUpdateApplicationRequest: CreateOrUpdateApplicationRequest
    ) -> ConductorApplication:
        app_obj = self.applicationResourceApi.create_application(createOrUpdateApplicationRequest)
        return self.api_client.deserialize_class(app_obj, "ConductorApplication")
    
    def getApplication(self, applicationId: str) -> ConductorApplication:
        app_obj = self.applicationResourceApi.get_application(applicationId)
        return self.api_client.deserialize_class(app_obj, "ConductorApplication")
    
    def listApplications(self) -> List[ConductorApplication]:
        return self.applicationResourceApi.list_applications()
    
    def updateApplication(
        self,
        createOrUpdateApplicationRequest: CreateOrUpdateApplicationRequest,
        applicationId: str
    ) -> ConductorApplication:
        app_obj = self.applicationResourceApi.update_application(
            createOrUpdateApplicationRequest, applicationId
        )
        return self.api_client.deserialize_class(app_obj, "ConductorApplication")

    def deleteApplication(self, applicationId: str):
        self.applicationResourceApi.delete_application(applicationId)
        
    def addRoleToApplicationUser(self, applicationId: str, role: str):
        self.applicationResourceApi.add_role_to_application_user(applicationId, role)
    
    def removeRoleFromApplicationUser(self, applicationId: str, role: str):
        self.applicationResourceApi.remove_role_from_application_user(applicationId, role)

    def setApplicationTags(self, tags: List[MetadataTag], applicationId: str):
        self.applicationResourceApi.put_tags_for_application(tags, applicationId)

    def getApplicationTags(self, applicationId: str) -> List[MetadataTag]:
        return self.applicationResourceApi.get_tags_for_application(applicationId)

    def deleteApplicationTags(self, tags: List[MetadataTag], applicationId: str):
        self.applicationResourceApi.delete_tags_for_application(tags, applicationId)

    def createAccessKey(self, applicationId: str) -> CreatedAccessKey:
        key_obj = self.applicationResourceApi.create_access_key(applicationId)
        created_access_key = CreatedAccessKey(key_obj["id"], key_obj["secret"])
        return created_access_key
    
    def getAccessKeys(self, applicationId: str) -> List[AccessKey]:
        access_keys_obj = self.applicationResourceApi.get_access_keys(applicationId)
        
        access_keys = []
        for key_obj in access_keys_obj:
            access_key = AccessKey(key_obj["id"], key_obj["status"], key_obj["createdAt"])
            access_keys.append(access_key)
    
        return access_keys
    
    def toggleAccessKeyStatus(self, applicationId: str, keyId: str) -> AccessKey:
        key_obj = self.applicationResourceApi.toggle_access_key_status(applicationId, keyId)
        return AccessKey(key_obj["id"], key_obj["status"], key_obj["createdAt"])

    def deleteAccessKey(self, applicationId: str, keyId: str):
        self.applicationResourceApi.delete_access_key(applicationId, keyId)
    
    # Users
    
    def upsertUser(self, upsertUserRequest: UpsertUserRequest, userId: str) -> ConductorUser:
        user_obj = self.userResourceApi.upsert_user(upsertUserRequest, userId)
        return self.api_client.deserialize_class(user_obj, "ConductorUser")
    
    def getUser(self, userId: str) -> ConductorUser:
        user_obj = self.userResourceApi.get_user(userId)
        return self.api_client.deserialize_class(user_obj, "ConductorUser")
    
    def listUsers(self, apps: Optional[bool] = False) -> List[ConductorUser]:
        kwargs = { "apps": apps }
        return self.userResourceApi.list_users(**kwargs)

    def deleteUser(self, userId: str):
        self.userResourceApi.delete_user(userId)
    
    # Groups
    
    def upsertGroup(self, upsertGroupRequest: UpsertGroupRequest, groupId: str) -> Group:
        group_obj = self.groupResourceApi.upsert_group(upsertGroupRequest, groupId)
        return self.api_client.deserialize_class(group_obj, "Group")
        
    def getGroup(self, groupId: str) -> Group:
        group_obj = self.groupResourceApi.get_group(groupId)
        return self.api_client.deserialize_class(group_obj, "Group")

    def listGroups(self) -> List[Group]:
        return self.groupResourceApi.list_groups()

    def deleteGroup(self, groupId: str):
        self.groupResourceApi.delete_group(groupId)
    
    def addUserToGroup(self, groupId: str, userId: str):
        self.groupResourceApi.add_user_to_group(groupId, userId)

    def getUsersInGroup(self, groupId: str) -> List[ConductorUser]:
        user_objs = self.groupResourceApi.get_users_in_group(groupId)
        group_users = []
        for u in user_objs:
            c_user = self.api_client.deserialize_class(u, "ConductorUser")
            group_users.append(c_user)
        
        return group_users

    def removeUserFromGroup(self, groupId: str, userId: str):
        self.groupResourceApi.remove_user_from_group(groupId, userId)
    
    # Permissions
    
    def grantPermissions(self, subject: SubjectRef, target: TargetRef, access: List[AccessType]):
        req = AuthorizationRequest(subject, target, access)
        self.authorizationResourceApi.grant_permissions(req)
        
    def getPermissions(self, target: TargetRef) -> Dict[str, List[SubjectRef]]:
        resp_obj = self.authorizationResourceApi.get_permissions(target.type.name, target.id)
        permissions = {}
        for access_type, subjects in resp_obj.items():
            subject_list = []
            for sub in subjects:
                subject_list.append(
                    SubjectRef(sub["type"], sub["id"])
                )
            permissions[access_type] = subject_list
        return permissions

    def getGrantedPermissionsForGroup(self, groupId: str) -> List[GrantedPermission]:
        granted_access_obj = self.groupResourceApi.get_granted_permissions1(groupId)
        granted_permissions = []
        for ga in granted_access_obj['grantedAccess']:
            target = TargetRef(ga["target"] ["type"], ga["target"] ["id"])
            access = ga["access"]
            granted_permissions.append(GrantedPermission(target, access))
        return granted_permissions
    
    def getGrantedPermissionsForUser(self, userId: str) -> List[GrantedPermission]:
        granted_access_obj = self.userResourceApi.get_granted_permissions(userId)
        granted_permissions = []
        for ga in granted_access_obj['grantedAccess']:
            target = TargetRef(ga["target"] ["type"], ga["target"] ["id"])
            access = ga["access"]
            granted_permissions.append(GrantedPermission(target, access))
        return granted_permissions

    def removePermissions(self, subject: SubjectRef, target: TargetRef, access: List[AccessType]):
        req = AuthorizationRequest(subject, target, access)
        self.authorizationResourceApi.remove_permissions(req)
        