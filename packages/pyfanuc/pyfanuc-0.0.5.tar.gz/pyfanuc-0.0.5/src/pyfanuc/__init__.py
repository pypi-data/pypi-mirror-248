# __init__.py

from importlib import resources

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from .main import FocasException, UnableToReadMacro, UnableToReadAxis, FocasController

# Version of the realpython-reader package
__version__ = "0.0.2"
