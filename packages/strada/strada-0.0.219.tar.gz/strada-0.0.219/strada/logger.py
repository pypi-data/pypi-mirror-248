import functools
import inspect
import json
import time

from .sdk import StradaResponseStatus
from .custom_types import HttpObjectType, LogType
from .debug_logger import DebugLogger


def debug_logger_execute(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        
        # print(self.__dict__) # Here, we can have access to the function name
        
        # Track execution time
        start_time = time.time()
        
        # Execute the function
        result = func(self, *args, **kwargs)
        
        json_response = result.model_dump_json()
        DebugLogger.log_function_call(function_name=self.function_name, app_name="openai-chatgpt", log_entry={"status": StradaResponseStatus.SUCCESS.name, "input": kwargs, "output": json_response})
        
        # Track execution time
        end_time = time.time()
        return result
    return wrapper


def debug_logger_http(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        DebugLogger.log_http_object(HttpObjectType.REQUEST.name, req_log_entry)
        
        # Execute the function
        result = func(self, *args, **kwargs)
        
        DebugLogger.log_http_object(HttpObjectType.RESPONSE.name, res_log_entry)
        return result
    return wrapper