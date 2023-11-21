# Access Control Management

## Authorization Client

### Initialization
```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.orkes.orkes_authorization_client import OrkesAuthorizationClient

configuration = Configuration(
    server_api_url=SERVER_API_URL,
    debug=False,
    authentication_settings=AuthenticationSettings(key_id=KEY_ID, key_secret=KEY_SECRET)
)

authorization_client = OrkesAuthorizationClient(configuration)
```

### Application Management

#### Creating Application
Creates an application and returns a ConductorApplication object.
```python
from conductor.client.http.models.create_or_update_application_request import CreateOrUpdateApplicationRequest
from conductor.client.http.models.conductor_application import ConductorApplication

request = CreateOrUpdateApplicationRequest("APPLICATION_NAME")
app = authorization_client.createApplication(request)
application_id = app.id
```

#### Get Application
```python
app = authorization_client.getApplication(application_id)
```

#### List All Applications
```python
apps = authorization_client.listApplications()
```

#### Update Application
Updates an application and returns a ConductorApplication object.

```python
request = CreateOrUpdateApplicationRequest("APPLICATION_NAME")
updated_app = authorization_client.updateApplication(request, application_id)
```

#### Delete Application
```python
authorization_client.deleteApplication(application_id)
```

#### Add a role for an Application user
Add one of the roles out of ["USER", "ADMIN", "METADATA_MANAGER", "WORKFLOW_MANAGER", "USER_READ_ONLY"]
to an application user.
```python
authorization_client.addRoleToApplicationUser(application_id, "USER")
```

#### Remove a role assigned to an Application user
```python
authorization_client.removeRoleFromApplicationUser(application_id, "USER")
```

#### Set Application tags
```python
from conductor.client.orkes.models.metadata_tag import MetadataTag

tags = [
    MetadataTag("auth_tag", "val"), MetadataTag("auth_tag_2", "val2")
]
authorization_client.getApplicationTags(tags, application_id)
```

#### Get Application tags
```python
tags = authorization_client.getApplicationTags(application_id)
```

#### Delete Application tags
```python
tags = [
    MetadataTag("auth_tag", "val"), MetadataTag("auth_tag_2", "val2")
]
authorization_client.deleteApplicationTags(tags, application_id)
```

### Access Key Management

#### Create Access Key
Creates an access key for the specified application and returns a CreatedAccessKey object.
The SECRET for this access key is available in the returned object. This is the only time
when the secret for this newly created access key can be retrieved and saved.
```python
from conductor.client.orkes.models.created_access_key import CreatedAccessKey

created_access_key = authorization_client.createAccessKey(application_id)
```

#### Get Access Key
Retrieves all access keys for the specified application as List[AccessKey].

```python
from conductor.client.orkes.models.access_key import AccessKey

access_keys = authorization_client.getAccessKeys(application_id)
```

#### Enabling / Disabling Access Key
Toggle access key status between ACTIVE and INACTIVE.
```python
 access_key = authorization_client.toggleAccessKeyStatus(application_id, created_access_key.id)
```

#### Delete Acccess Key
```python
authorization_client.deleteAccessKey(application_id, created_access_key.id)
```

### User Management

#### Create or Update User
Creates or updates a user and returns a ConductorUser object.
```python
from conductor.client.http.models.upsert_user_request import UpsertUserRequest
from conductor.client.http.models.conductor_user import ConductorUser

user_id = 'test.user@company.com'
user_name = "Test User"
roles = ["USER"]
req = UpsertUserRequest(user_name, roles)
user = authorization_client.upsertUser(req, user_id)
```

#### Get User
```python
user = authorization_client.getUser(user_id)
```

#### List All Users
```python
users = authorization_client.listUsers()
```

#### Delete User
```python
authorization_client.deleteUser(user_id)
```

### Group Management

#### Create or Update a Group
Creates or updates a user group and returns a Group object.
```python
from conductor.client.http.models.upsert_group_request import UpsertGroupRequest
from conductor.client.http.models.group import Group

group_id = 'test_group'
group_name = "Test Group"
group_user_roles = ["USER"]
req = UpsertGroupRequest("Integration Test Group", group_user_roles)
group = authorization_client.upsertGroup(req, group_id)
```

#### Get Group
```python
group = authorization_client.getGroup(group_id)
```

#### List All Groups
Retrives all groups as a List[Group]
```python
users = authorization_client.listGroups()
```

#### Delete Group
```python
authorization_client.deleteGroup(group_id)
```

#### Add users to a Group
```python
 authorization_client.addUserToGroup(group_id, user_id)
```

#### Get all users in a Group
Retrives all users in a group as List[ConductorUser]
```python
users = self.authorization_client.getUsersInGroup(group_id)
```

#### Remove users from a group
```python
authorization_client.removeUserFromGroup(group_id, user_id)
```

### Permission Management

#### Grant Permissions
Grants a set of accesses to the specified Subject for a given Target.
```python
from conductor.client.http.models.target_ref import TargetRef, TargetType
from conductor.client.http.models.subject_ref import SubjectRef, SubjectType
from conductor.client.orkes.models.access_type import AccessType

target = TargetRef(TargetType.WORKFLOW_DEF, "TEST_WORKFLOW")
subject_group = SubjectRef(SubjectType.GROUP, group_id)
access_group = [AccessType.EXECUTE]

subject_user = SubjectRef(SubjectType.USER, user_id)
access_user = [AccessType.EXECUTE, AccessType.READ]

authorization_client.grantPermissions(subject_group, target, access_group)
authorization_client.grantPermissions(subject_user, target, access_user)
```

#### Get Permissions for a Target
Given the target, returns all permissions associated with it as a Dict[str, List[SubjectRef]].
In the returned dictionary, key is AccessType and value is a list of subjects.
```python
from conductor.client.http.models.target_ref import TargetRef, TargetType

target = TargetRef(TargetType.WORKFLOW_DEF, WORKFLOW_NAME)
target_permissions = authorization_client.getPermissions(target)
```

#### Get Permissions granted to a Group
Given a group id, returns all the permissions granted to a group as List[GrantedPermission].
```python
from conductor.client.orkes.models.granted_permission import GrantedPermission

group_permissions = authorization_client.getGrantedPermissionsForGroup(group_id)
```

#### Get Permissions granted to a User
Given a user id, returns all the permissions granted to a user as List[GrantedPermission].
```python
from conductor.client.orkes.models.granted_permission import GrantedPermission

user_permissions = authorization_client.getGrantedPermissionsForUser(user_id)
```

#### Remove Permissions
Removes a set of accesses from a specified Subject for a given Target.

```python
from conductor.client.http.models.target_ref import TargetRef, TargetType
from conductor.client.http.models.subject_ref import SubjectRef, SubjectType
from conductor.client.orkes.models.access_type import AccessType

target = TargetRef(TargetType.WORKFLOW_DEF, "TEST_WORKFLOW")
subject_group = SubjectRef(SubjectType.GROUP, group_id)
access_group = [AccessType.EXECUTE]

subject_user = SubjectRef(SubjectType.USER, user_id)
access_user = [AccessType.EXECUTE, AccessType.READ]

authorization_client.removePermissions(subject_group, target, access_group)
authorization_client.removePermissions(subject_user, target, access_user)
```
