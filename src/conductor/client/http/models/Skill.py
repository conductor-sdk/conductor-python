# skills.py
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from conductor.client.workflow.task.http_task import HttpTask
from urllib.parse import urlencode, unquote

class SkillType(str, Enum):
    API = "API"
    WORKER = "WORKER"

class SkillDocument:
    """Represents a single capability for RAG"""
    id: str
    skill_name: str
    capability_name: str
    description: str
    when_to_use: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    examples: List[Dict[str, Any]]


class Skill(BaseModel):
    """
    Skills represent capabilities that can be assigned to agents.
    They can be created, managed and shared across different agents.
    """
    name: str = Field(description="Unique name of the skill")
    type: SkillType = Field(description="Type of skill (API or WORKER)")
    version: str = Field(description="Version of the skill")
    description: str = Field(description="Detailed description of what the skill does")
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration parameters for the skill"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional metadata about the skill"
    )


class OpenApiSkill:
    def __init__(self, spec: Dict[str, Any], base_url: str, parameter_mappings: Dict[str, str]):
        self.spec = spec  # OpenAPI spec
        self.base_url = base_url
         # each secret will be used as e.g. '${workflow.secrets.GEO_API_KEY}'
        self.parameter_mappings = parameter_mappings # Maps parameter names to secret refs or other sources
    
    def get_capability_description(self) -> List[SkillDocument]:
        """Converts OpenAPI endpoints to SkillDocument objects"""
        skill_documents = []
        
        for path, methods in self.spec['paths'].items():
            for method, details in methods.items():
                # Create a unique ID for each endpoint
                skill_id = f"{method.lower()}_{path.replace('/', '_').strip('_')}"
                
                # Extract parameters for input schema
                input_schema = {}
                for param in details.get('parameters', []):
                    input_schema[param['name']] = param['schema'].get('type', 'string')
                
                # Create example using parameter mappings
                example = {}
                for param_name, mapped_value in self.parameter_mappings.items():
                    example[param_name] = f"Example: {mapped_value}"
                
                # Create the skill document
                skill_doc = SkillDocument()
                skill_doc.id = skill_id
                skill_doc.skill_name = f"{self.base_url}{path}"
                skill_doc.capability_name = details['summary']
                skill_doc.description = f"Can {details['summary']} using {method.upper()} {path}"
                skill_doc.when_to_use = [
                    f"When {details['summary'].lower()} is needed",
                    f"When making {method.upper()} requests to {path}"
                ]
                skill_doc.input_schema = input_schema
                skill_doc.output_schema = {"response": "HTTP response from the API"}
                skill_doc.examples = [example]
                
                skill_documents.append(skill_doc)
        
        return skill_documents
        
        def to_conductor_task(self, task_ref_name: str, inputs: Dict) -> HttpTask:
            """
            Convert an OpenAPI endpoint to an HttpTask, handling parameter mappings and HTTP methods.
            Supports building URL parameters for GET requests.
            """
            paths = self.spec.get('paths', {})
            
            tasks = []
            for path, path_spec in paths.items():
                for method, operation in path_spec.items():
                    method = method.upper()
                    full_url = f"{self.base_url.rstrip('/')}{path}"
                    
                    parameters = operation.get('parameters', [])
                    
                    query_params = {}
                    headers = {}
                    path_params = {}
                    
                    for param in parameters:
                        param_name = param['name']
                        param_in = param.get('in', '')
                        
                        if param_name in self.parameter_mappings:
                            mapped_value = self.parameter_mappings[param_name]
                            
                            if param_in == 'query':
                                query_params[param_name] = mapped_value
                            elif param_in == 'header':
                                headers[param_name] = mapped_value
                            elif param_in == 'path':
                                path_params[param_name] = mapped_value
                    
                    for param_name, value in path_params.items():
                        full_url = full_url.replace(f"{{{param_name}}}", value)
                    
                    if method == 'GET' and query_params:
                        query_string = unquote(urlencode(query_params))
                        full_url = f"{full_url}?{query_string}"
                        http_input = {
                            'uri': full_url,
                            'method': method
                        }
                    else:
                        http_input = {
                            'uri': full_url,
                            'method': method,
                            'params': query_params
                        }
                    
                    if headers:
                        http_input['headers'] = headers
                    
                    # Create a clean task name by:
                    # 1. Replace slashes with single underscore
                    # 2. Remove any path parameter brackets
                    # 3. Remove any remaining special characters
                    clean_path = path.replace('/', '_').replace('{', '').replace('}', '')
                    clean_path = clean_path.strip('_')  # Remove leading/trailing underscores
                    
                    # Create meaningful task name based on method and path
                    task_name = f"{method.lower()}_{clean_path}"
                    
                    task = HttpTask(
                        task_ref_name=f"{task_name}_ref",  # Add _ref suffix
                        http_input=http_input
                    )
                    task.name = task_name  # Set the task name
                    tasks.append(task)
            
            return tasks[0] if len(tasks) == 1 else tasks

        def _resolve_reference(self, ref: str) -> Dict:
            """Helper method to resolve $ref in OpenAPI spec"""
            if not ref.startswith('#/'):
                raise ValueError(f"Only local references are supported: {ref}")
            
            parts = ref[2:].split('/')
            current = self.spec
            for part in parts:
                current = current[part]
            return current

def compare_http_tasks(task1: HttpTask, task2: HttpTask) -> bool:
    """Compare two HttpTask objects by their content"""
    if task1.task_ref_name != task2.task_ref_name:
        print(f"Task ref name mismatch: {task1.task_ref_name} != {task2.task_ref_name}")
        return False
    
    # Compare http_input dictionaries
    if type( task1.http_input ) == type ( dict() ):
        if set(task1.http_input.keys()) != set(task2.http_input.keys()):
            print(f"Http input keys mismatch: {task1.http_input.keys()} != {task2.http_input.keys()}")
            return False
        
        for key in task1.http_input:
            if task1.http_input[key] != task2.http_input[key]:
                print(f"Http input value mismatch for {key}: {task1.http_input[key]} != {task2.http_input[key]}")
                return False
    
    return True

def run_test_case(name: str, spec: Dict, base_url: str, parameter_mappings: Dict, expected_output: Dict):
    print(f"\nRunning test case: {name}")
    print("-" * 50)
    
    skill = OpenApiSkill(spec, base_url, parameter_mappings)
    result = skill.to_conductor_task("test", {})
    
    # Compare the result with expected output
    success = True
    if isinstance(result, list):
        if not isinstance(expected_output, list) or len(result) != len(expected_output):
            success = False
            print(f"List length mismatch: {len(result)} != {len(expected_output)}")
        else:
            for r, e in zip(result, expected_output):
                if not compare_http_tasks(r, e):
                    success = False
                    break
    else:
        success = compare_http_tasks(result, expected_output)
    
    print("\nResult:")
    print(f"  Task ref name: {result.task_ref_name}")
    print(f"  Http input: {result.http_input}")
    print("\nExpected:")
    print(f"  Task ref name: {expected_output.task_ref_name}")
    print(f"  Http input: {expected_output.http_input}")
    print("\nTest passed:" if success else "\nTest failed:", "✅" if success else "❌")
    return success

if __name__ == "__main__":
    # Test cases remain the same as before
    test_cases = [
        {
            "name": "Simple GET request with query parameters",
            "spec": {
                "paths": {
                    "/search": {
                        "get": {
                            "parameters": [
                                {"name": "q", "in": "query"},
                                {"name": "api_key", "in": "query"}
                            ]
                        }
                    }
                }
            },
            "base_url": "https://api.example.com",
            "parameter_mappings": {
                "q": "${workflow.input.query}",
                "api_key": "${workflow.secrets.API_KEY}"
            },
            "expected": HttpTask(
                task_ref_name="get_search_ref",
                http_input={
                    "uri": "https://api.example.com/search?q=${workflow.input.query}&api_key=${workflow.secrets.API_KEY}",
                    "method": "GET"
                }
            )
        },
        {
            "name": "POST request with path parameter",
            "spec": {
                "paths": {
                    "/users/{user_id}": {
                        "post": {
                            "parameters": [
                                {"name": "user_id", "in": "path"},
                                {"name": "auth_token", "in": "header"}
                            ]
                        }
                    }
                }
            },
            "base_url": "https://api.example.com",
            "parameter_mappings": {
                "user_id": "${workflow.input.user_id}",
                "auth_token": "${workflow.secrets.AUTH_TOKEN}"
            },
            "expected": HttpTask(
                task_ref_name="post_users_user_id_ref",
                http_input={
                    "uri": "https://api.example.com/users/${workflow.input.user_id}",
                    "method": "POST",
                    "params": {},
                    "headers": {"auth_token": "${workflow.secrets.AUTH_TOKEN}"}
                }
            )
        },
        {
            "name": "GET request with query parameters and special characters",
            "spec": {
                "paths": {
                    "/filter": {
                        "get": {
                            "parameters": [
                                {"name": "complex_query", "in": "query"}
                            ]
                        }
                    }
                }
            },
            "base_url": "https://api.example.com",
            "parameter_mappings": {
                "complex_query": "${workflow.input.complex query with spaces}"
            },
            "expected": HttpTask(
                task_ref_name="get_filter_ref",
                http_input={
                    "uri": "https://api.example.com/filter?complex_query=${workflow.input.complex query with spaces}",
                    "method": "GET"
                }
            )
        }
    ]

    # Run all test cases
    total_tests = len(test_cases)
    passed_tests = 0

    for test_case in test_cases:
        if run_test_case(
            test_case["name"],
            test_case["spec"],
            test_case["base_url"],
            test_case["parameter_mappings"],
            test_case["expected"]
        ):
            passed_tests += 1

    print("\nTest Summary")
    print("-" * 50)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.2f}%")