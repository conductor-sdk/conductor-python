from typing import Dict, List, Optional
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.models.access_key_response import AccessKeyResponse
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.rest import ApiException
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.user_resource_api import UserResourceApi
from conductor.client.http.api.group_resource_api import GroupResourceApi
from conductor.client.http.api.application_resource_api import ApplicationResourceApi
from conductor.client.http.models.group import Group
from conductor.client.http.models.subject_ref import SubjectRef
from conductor.client.http.models.conductor_user import ConductorUser
from conductor.client.http.models.conductor_application import ConductorApplication
from conductor.client.http.models.upsert_user_request import UpsertUserRequest
from conductor.client.http.models.upsert_group_request import UpsertGroupRequest
from conductor.client.http.models.authorization_request import AuthorizationRequest
from conductor.client.http.models.create_or_update_application_request import CreateOrUpdateApplicationRequest
from conductor.client.authorization_client import AuthorizationClient

class OrkesAuthorizationClient(AuthorizationClient):
    def __init__(self, configuration: Configuration):
        api_client = ApiClient(configuration)
        self.applicationResourceApi = ApplicationResourceApi(api_client)
        self.userResourceApi = UserResourceApi(api_client)
        self.groupResourceApi = GroupResourceApi(api_client)

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

    # def setApplicationTags(self, tags: List[MetadataTag], applicationId: str):
    #     pass

    # def getApplicationTags(self, applicationId: str) -> List[MetadataTag]:
    #     pass

    # def deleteApplicationTags(self, tags: List[MetadataTag], applicationId: str):
    #     pass

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
        return self.userResourceApi.upsert_user(upsertUserRequest, userId)
    
    def getUser(self, userId: str) -> ConductorUser:
        return self.userResourceApi.get_user(userId)
    
    def listUsers(self, apps: Optional[bool] = False) -> List[ConductorUser]:
        kwargs = { "apps": apps }
        return self.userResourceApi.list_users(**kwargs)

    def deleteUser(self, userId: str):
        self.userResourceApi.delete_user(userId)
    
    # def sendInviteEmail(self, userId: str, conductorUser: ConductorUser):
    #     pass
    
    # def getGrantedPermissionsForUser(self, userId: str):
    #     pass
    
    # Groups
    
    def upsertGroup(self, upsertGroupRequest: UpsertGroupRequest, groupId: str) -> Group:
        return self.groupResourceApi.upsert_group(upsertGroupRequest, groupId)
        
    def getGroup(self, groupId: str) -> Group:
        return self.groupResourceApi.get_group(groupId)
    
    def listGroups(self) -> List[Group]:
        return self.groupResourceApi.list_groups()

    def deleteGroup(self, groupId: str):
        self.groupResourceApi.delete_group(groupId)
    
    def addUserToGroup(self, groupId: str, userId: str):
        self.groupResourceApi.add_user_to_group(groupId, userId)

    def getUsersInGroup(self, groupId: str) -> List[ConductorUser]:
        return self.groupResourceApi.get_users_in_group(groupId)

    def removeUserFromGroup(self, groupId: str, userId: str):
        self.groupResourceApi.remove_user_from_group(groupId, userId)
    
    # def getGrantedPermissionsForGroup(self, groupId: str):
    #     pass
    
    # Permissions
    
    def getPermissions(self, type: str, id: str) -> Dict[str, List[SubjectRef]]:
        pass
    
    
    def grantPermissions(self, authorizationRequest: AuthorizationRequest):
        pass

    def removePermissions(self, authorizationRequest: AuthorizationRequest):
        pass