import inspect
from enum import Enum
import json

class HttpObjectType(Enum):
    REQUEST = 'REQUEST'
    RESPONSE = 'RESPONSE'
    
class LogType(Enum):
    FUNCTION_CALL = 'FUNCTION_CALL'
    HTTP_OBJECT = 'HTTP_OBJECT'
    
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
            print(f'<LOG>{formatted_entry}</LOG>', flush=True)

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
            
            print(f'<LOG>{formatted_entry}</LOG>', flush=True)
            
        except Exception as e:
            pass