import functools
import time
import inspect
from enum import Enum
import json

from .common import original_print
from .custom_types import HttpObjectType, LogType


class DebugLogger:
    @staticmethod
    def log_http_object(http_object_type, log_entry):
        # log_entry must be a dictionary
        try:
            log_entry['log_type'] = LogType.HTTP_OBJECT.name
            log_entry['http_object_type'] = http_object_type
            
            # Convert log entry to JSON
            formatted_entry = json.dumps(log_entry)

            # Print the log entry
            original_print(f'<HTTP>{formatted_entry}</HTTP>', flush=True)

        except Exception as e:
            pass
        
    @staticmethod
    def log_function_call(log_entry, function_name=None, app_name=None):
        # log_entry must be a dictionary
        try:
            # Add the function name to the log information
            log_entry['function_name'] = function_name
            log_entry['app_name'] = app_name
            log_entry['log_type'] = LogType.FUNCTION_CALL.name
            
            # Convert log entry to JSON
            formatted_entry = json.dumps(log_entry)
            
            original_print(f'<DEBUG>{formatted_entry}</DEBUG>', flush=True)
            
        except Exception as e:
            pass


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