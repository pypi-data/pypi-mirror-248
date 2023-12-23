import sys as _sys
import os as _os
from typing import TypeVar as _TypeVar
_T = _TypeVar('_T')

def RequireModules(*modules: str):
    '''
    Checks if python modules are installed, otherwise tries to install them
    '''
    import subprocess
    import pkgutil

    required = set(modules)
    installed = {pkg.name for pkg in pkgutil.iter_modules()}
    missing = required - installed
    if not missing:
        return
    
    print("Please wait a moment, application is missing some modules. These will be installed automatically...")
    for moduleName in missing:
        print(f"Installing {moduleName}... ", end='')
        result = subprocess.run([_sys.executable, "-m", "pip", "install", moduleName], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if(result.returncode != 0): #something went bad
            print("FAILED!")
        else:
            print("OK!")

    installed = {pkg.name for pkg in pkgutil.iter_modules()}
    missing = required - installed
    if missing:
        print("Not all required modules could automatically be installed!")
        input(f"Please install the modules below manually: {missing}")
        raise ImportError(f"Missing dependecies for this application: {missing}")
    return

def ImportModuleDynamically(moduleName, path):
    '''
    :param moduleName: freely name the module to import
    :param path: full path to the python module
    '''
    import importlib.util

    spec = importlib.util.spec_from_file_location(moduleName, path)
    mod = importlib.util.module_from_spec(spec)
    _sys.modules[moduleName] = mod
    _sys.path.append(_os.path.dirname(_os.path.abspath(path)))
    spec.loader.exec_module(mod)
    return mod

def ChangeCWDToMainModule():
    '''Set the directory of the main script module as the current working directory'''
    _os.chdir(ModuleInfo().pathInfo.Tail)

class ModuleInfo:
    ''' A wrapper class for retrieving information about a module '''

    def __init__(self, module=_sys.modules["__main__"]):
        '''
        :param module: The module to retrieve information from. Defaults to '__main__'.
        '''

        from simpleworkspace.io.path import PathInfo

        self.rawModule = module
        self.pathInfo = PathInfo(module.__file__)
        '''
            >>> pathInfo.Absolute # '/path/to/main_script.py'
            >>> pathInfo.Head     # 'main_script.py'
            >>> pathInfo.Tail     # '/path/to'
        '''

    def GetDeclaredClasses(self, targetClass: type[_T], includeChildsOnly=False) -> dict[str, type[_T]]:
        '''
        Get the classes declared in the module that are subclasses of the specified target class and the target class itself.

        :param targetClass: The target class to search for.
        :param includeChildsOnly: If True, include only child classes of the target class, aka exclude targetClass itself
        :return: A dictionary containing the matched class names as keys and class objects as values.
        '''
        import inspect

        matchedClasses = {}
        for className, classObj in inspect.getmembers(self.rawModule, inspect.isclass):
            if(not issubclass(classObj, targetClass)):
                continue
            if(includeChildsOnly and classObj == targetClass):
                continue
            if(self.rawModule.__name__ != classObj.__module__):
                continue

            matchedClasses[className] = classObj
        
        return matchedClasses