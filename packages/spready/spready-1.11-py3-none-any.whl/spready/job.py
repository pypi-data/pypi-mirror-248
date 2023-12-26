import importlib
from typing import Any, Dict
from .parser import SpreadyDecoratorParser
import os, sys
from loguru import logger

 
parser = SpreadyDecoratorParser(os.environ["SPREADY_MODULES"])
spreadyModules = parser.spreadyRouts

logger.info(f"Spready moduels found: {spreadyModules}")

from .dto import SPRequest



def runjob(routePath: str, params: Dict[str, Any], requestType: str, headers: Dict[str, Any] = {}):
    logger.info(f"Running function with {routePath} and {params}")
    if routePath in spreadyModules:
        function_string = spreadyModules[routePath]
    else:
        logger.error(f"Route not found {routePath}")
        return {"error": "Route not found"}
    try:
        mod_name, func_name = function_string.rsplit('.',1)
        logger.debug(f"Module name: {mod_name}")
        logger.debug(f"Function name: {func_name}")
        sys.path.append(os.getcwd())
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        req = SPRequest(json=params, requestType=requestType, headers=headers)
        result = func(req)
        logger.debug(f"Output: {result}")
        return result
    except Exception as _e:
        return {"error": str(_e)}
