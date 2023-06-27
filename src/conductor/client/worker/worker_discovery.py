from ..configuration.configuration import Configuration
from ..worker.worker import Worker
from typing import List
import ast
import astor
import inspect
import logging
import os

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


def get_annotated_workers():
    pkg = __get_client_topmost_package_filepath()
    workers = __get_annotated_workers_from_subtree(pkg)
    logger.debug(f'Found {len(workers)} workers')
    return workers


def __get_client_topmost_package_filepath():
    module = inspect.getmodule(inspect.stack()[-1][0])
    while module:
        logger.debug(f'current_module: {module}')
        if not getattr(module, '__parent__', None):
            logger.debug(f'parent module not found for {module}')
            return getattr(module, '__file__', None)
        module = getattr(module, '__parent__', None)
    return None


def __get_annotated_workers_from_subtree(pkg):
    workers = []
    if not pkg:
        return workers
    pkg_path = os.path.dirname(pkg)
    for root, _, files in os.walk(pkg_path):
        for file in files:
            if not file.endswith('.py') or file == '__init__.py':
                continue
            module_path = os.path.join(root, file)
            with open(module_path, 'r') as file:
                source_code = file.read()
            module = ast.parse(source_code, filename=module_path)
            for node in ast.walk(module):
                if not isinstance(node, ast.FunctionDef):
                    continue
                for decorator in node.decorator_list:
                    params = __extract_decorator_info(
                        decorator)
                    if params is None:
                        continue
                    try:
                        worker = __create_worker_from_ast_node(
                            node, params)
                        if worker:
                            workers.append(worker)
                    except Exception as e:
                        logger.debug(
                            f'Failed to create worker from function: {node.name}. Reason: {str(e)}')
                        continue
    return workers


def __extract_decorator_info(decorator):
    if not isinstance(decorator, ast.Call):
        return None
    decorator_type = None
    decorator_func = decorator.func
    if isinstance(decorator_func, ast.Attribute):
        decorator_type = decorator_func.attr
    elif isinstance(decorator_func, ast.Name):
        decorator_type = decorator_func.id
    if decorator_type != 'WorkerTask':
        return None
    decorator_params = {}
    if decorator.args:
        for arg in decorator.args:
            arg_value = astor.to_source(arg).strip()
            decorator_params[arg_value] = ast.literal_eval(arg)
    if decorator.keywords:
        for keyword in decorator.keywords:
            param_name = keyword.arg
            param_value = ast.literal_eval(keyword.value)
            decorator_params[param_name] = param_value
    return decorator_params


def __create_worker_from_ast_node(node, params):
    logger.debug(
        f'trying to create worker from function: {node.name}, with params: {params}')
    params['execute_function'] = __retrieve_function_from_ast(node)
    worker = Worker(**params)
    return worker


def __retrieve_function_from_ast(node, imports=None):
    if imports is None:
        imports = []
    function_name = node.name
    function_source = ast.unparse(node)
    function_imports = __extract_imports_from_ast(node)
    all_imports = function_imports + imports
    logger.debug(f'all imports: {all_imports}')
    temp_module = ast.parse(function_source, filename='<ast>', mode='exec')
    import_nodes = [ast.parse(import_str) for import_str in all_imports]
    temp_module.body = import_nodes + temp_module.body
    code = compile(temp_module, filename='<ast>', mode='exec')
    exec(code, globals())
    function = globals()[function_name]
    return function


def __extract_imports_from_ast(node: ast.AST) -> List[str]:
    import_statements = []
    for child_node in ast.iter_child_nodes(node):
        if isinstance(child_node, ast.Import):
            import_names = [alias.name for alias in child_node.names]
            import_statement = f"import {', '.join(import_names)}"
            import_statements.append(import_statement)
        elif isinstance(child_node, ast.ImportFrom):
            module = child_node.module or ''
            import_names = [alias.name for alias in child_node.names]
            import_statement = f"from {module} import {', '.join(import_names)}"
            import_statements.append(import_statement)
    return import_statements
