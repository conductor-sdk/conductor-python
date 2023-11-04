from typing import Dict, List, Optional
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.models.access_type import AccessType
from conductor.client.orkes.models.granted_permission import GrantedPermission
from conductor.client.orkes.models.access_key_response import AccessKeyResponse
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.rest import ApiException
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.user_resource_api import UserResourceApi
from conductor.client.http.api.group_resource_api import GroupResourceApi
from conductor.client.http.api.application_resource_api import ApplicationResourceApi
from conductor.client.http.api.authorization_resource_api import AuthorizationResourceApi
from conductor.client.http.models.group import Group
from conductor.client.http.models.subject_ref import SubjectRef
from conductor.client.http.models.conductor_user import ConductorUser
from conductor.client.http.models.target_ref import TargetRef, TargetType
from conductor.client.http.models.conductor_application import ConductorApplication
from conductor.client.http.models.upsert_user_request import UpsertUserRequest
from conductor.client.http.models.upsert_group_request import UpsertGroupRequest
from conductor.client.http.models.authorization_request import AuthorizationRequest
from conductor.client.http.models.create_or_update_application_request import CreateOrUpdateApplicationRequest
from conductor.client.authorization_client import AuthorizationClient

class OrkesAuthorizationClient(AuthorizationClient):
    def __init__(self, configuration: Configuration):
        self.api_client = ApiClient(configuration)
        self.applicationResourceApi = ApplicationResourceApi(self.api_client)
        self.userResourceApi = UserResourceApi(self.api_client)
        self.groupResourceApi = GroupResourceApi(self.api_client)
        self.authorizationResourceApi = AuthorizationResourceApi(self.api_client)

    # Applications
    def createApplication(
        self,
        createOrUpdateApplicationRequest: CreateOrUpdateApplicationRequest
    ) -> ConductorApplication:
        return self.applicationResourceApi.create_application(createOrUpdateApplicationRequest)
    
    def getApplication(self, applicationId: str) -> ConductorApplication:
        return self.applicationResourceApi.get_application(applicationId)
    
    def listApplications(self) -> List[ConductorApplication]:
        return self.applicationResourceApi.list_applications()
    
    def updateApplication(
        self,
        createOrUpdateApplicationRequest: CreateOrUpdateApplicationRequest,
        applicationId: str
    ) -> ConductorApplication:
        return self.applicationResourceApi.update_application(
            createOrUpdateApplicationRequest, applicationId
        )

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

    # def createAccessKey(self, applicationId: str) -> AccessKeyResponse:
    #     return self.applicationResourceApi.create_access_key(applicationId)
    
    # def getAccessKeys(self, applicationId: str) -> List[AccessKeyResponse]:
    #     return self.applicationResourceApi.get_access_keys(applicationId)
    
    # def toggleAccessKeyStatus(self, applicationId: str, keyId: str) -> AccessKeyResponse:
    #     return self.applicationResourceApi.toggle_access_key_status(applicationId, keyId)

    # def deleteAccessKey(self, applicationId: str, keyId: str):
    #     self.applicationResourceApi.delete_access_key(applicationId, keyId)
    
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
    
    # def sendInviteEmail(self, userId: str, conductorUser: ConductorUser):
    #     pass
    
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
    
    def grantPermissions(self, subject: SubjectRef, target: TargetRef, access: List[AccessType]):
        req = AuthorizationRequest(subject, target, access)
        self.authorizationResourceApi.grant_permissions(req)

    def removePermissions(self, subject: SubjectRef, target: TargetRef, access: List[AccessType]):
        req = AuthorizationRequest(subject, target, access)
        self.authorizationResourceApi.remove_permissions(req)
        