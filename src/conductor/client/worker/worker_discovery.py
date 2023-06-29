from ..configuration.configuration import Configuration
from ..worker.worker import Worker
from typing import List
import ast
import astor
import types
import dis
import inspect
import logging
import os
import re

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
            import_statements = None
            for node in ast.walk(module):
                if not isinstance(node, ast.FunctionDef):
                    continue
                for decorator in node.decorator_list:
                    params = __extract_decorator_info(
                        decorator)
                    if params is None:
                        continue
                    try:
                        if import_statements is None:
                            import_statements = __extract_imports_from_ast(
                                source_code)
                        worker = __create_worker_from_ast_node(
                            node, params, imports=import_statements)
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
    logger.debug(f'Decorator: {decorator}')
    logger.debug(f'Decorator Params: {decorator_params}')
    return decorator_params


def __create_worker_from_ast_node(node, params, imports=None):
    logger.debug(
        f'trying to create worker from function: {node.name}, with params: {params}')
    params['execute_function'] = __retrieve_function_from_ast(node, imports)
    worker = Worker(**params)
    return worker


def __retrieve_function_from_ast(node, imports=None):
    if imports is None:
        imports = []
    function_name = node.name
    function_source = ast.unparse(node)
    function_source_with_imports = '\n'.join(
        imports) + '\n\n' + function_source
    logger.debug(f'function: {function_source_with_imports}')
    temp_module = ast.parse(
        function_source_with_imports,
        filename='<ast>', mode='exec')
    nodes = []
    traverse_ast(temp_module, nodes)
    code = compile(temp_module, filename='<ast>', mode='exec')
    logger.debug(f'code: {code}')
    dis.dis(code)
    function = None
    for instr in code.co_consts:
        if isinstance(instr, types.CodeType) and instr.co_name == function_name:
            function = types.FunctionType(instr, globals())
            break
    logger.debug(
        f'got function: {function} from function_name: {function_name}')
    return function


def __extract_imports_from_ast(source_code: str) -> List[str]:
    import_statements = re.findall(
        r'^\s*(?:import|from)\s+.+', source_code, re.MULTILINE)
    return import_statements


def traverse_ast(node, nodes):
    if not hasattr(node, 'lineno'):
        node.lineno = len(nodes) + 1
    nodes.append(0)
    for child in ast.iter_child_nodes(node):
        traverse_ast(child, nodes)
