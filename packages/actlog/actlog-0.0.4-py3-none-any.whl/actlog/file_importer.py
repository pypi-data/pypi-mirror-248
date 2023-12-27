import sys
import importlib.util


def import_module_from_file(module_name, path):
    """Returns a module imported from a file.

    See https://stackoverflow.com/a/67692/345716"""
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec == None or spec.loader == None:
        raise RuntimeError(f"Couldn't find {module_name} in {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
