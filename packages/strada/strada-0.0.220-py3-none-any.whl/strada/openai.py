from io import BytesIO
import builtins
import base64
import requests
from .sdk import HttpRequestExecutor, StradaResponse, StradaError, StradaResponseStatus
from .exception_handler import exception_handler
import time
import requests
from .common import (
    build_input_schema_from_strada_param_definitions,
    hydrate_input_fields,
    validate_http_input,
    custom_print
)
from .debug_logger import debug_logger_execute

# Initialize the print function to use the logger
builtins.print = custom_print

class OpenAICustomHttpActionBuilder:
    def __init__(self):
        self._instance = None
        self.default_function_name = "OpenAIAction"

    def set_param_schema(self, param_schema):
        self._get_instance().param_schema_definition = (
            build_input_schema_from_strada_param_definitions(param_schema)
        )
        return self

    def set_url(self, url):
        self._get_instance().url = url
        return self

    def set_method(self, method):
        self._get_instance().method = method
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_headers(self, headers):
        self._instance.headers = headers
        return self

    def set_path_params(self, path_params):
        self._instance.path = path_params
        return self

    def set_query_params(self, params):
        self._instance.params = params
        return self

    def set_body(self, body):
        self._instance.body = body
        return self
    
    def set_function_name(self, function_name):
        if function_name is None:
            self._instance.function_name = self.default_function_name
        else:
            self._instance.function_name = function_name
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = OpenAICustomHttpAction()
        return self._instance


class OpenAICustomHttpAction:
    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.headers = "{}"
        self.path = "{}"
        self.params = "{}"
        self.body = "{}"
        self.function_name = None

    def _execute_with_file(self, **kwargs):
        validate_http_input(self.param_schema_definition, **kwargs)

        headers = hydrate_input_fields(
            self.param_schema_definition, self.headers, **kwargs
        )
        query_params = hydrate_input_fields(
            self.param_schema_definition, self.params, **kwargs
        )
        body = hydrate_input_fields(self.param_schema_definition, self.body, **kwargs)

        headers["Authorization"] = f"Bearer {self.token}"

        base_64_file_str = body.get("file", None)
        if base_64_file_str is None:
            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=400,
                    statusCode=400,
                    message="No 'file' provided.'file' is required.",
                ),
            )
        MIME_type = body.get("MIME_type", None)
        if MIME_type is None:
            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=400,
                    statusCode=400,
                    message="No 'MIME_type' provided. 'MIME_type' is required.",
                ),
            )

        base_64_decoded = base64.b64decode(base_64_file_str)
        del body["file"]
        del body["MIME_type"]

        response = requests.request(
            self.method,
            self.url,
            headers=headers,
            params=query_params,
            data=body,
            files={"file": ("input_file", BytesIO(base_64_decoded), MIME_type)},
        )

        response_data = response.json()
        if response.ok:  # HTTP status code 200-299
            return StradaResponse(success=True, data=response_data)
        else:
            # If the response contains structured error information, you can parse it here
            error_message = response_data.get("message", None)
            if error_message is None:
                error_message = response_data.get("error", None)
            if error_message is None:
                error_message = response.text
            if error_message is None:
                error_message = "Error executing HTTP Request."

            error = StradaError(
                errorCode=response.status_code,
                statusCode=response.status_code,
                message=error_message,
            )
            return StradaResponse(success=False, data=response_data, error=error)

    def _execute_custom_assistant_message(self, **kwargs):
        validate_http_input(self.param_schema_definition, **kwargs)

        headers = hydrate_input_fields(
            self.param_schema_definition, self.headers, **kwargs
        )
        path_params = hydrate_input_fields(
            self.param_schema_definition, self.path, **kwargs
        )
        body = hydrate_input_fields(self.param_schema_definition, self.body, **kwargs)

        headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"
        headers["OpenAI-Beta"] = "assistants=v1"

        # Create the message and body to the
        threads_run_body = {
            "assistant_id": path_params["assistant_id"],
            "thread": {"messages": [{"role": "user", "content": body["message"]}]},
        }
        thread_run_resp = requests.post(
            "https://api.openai.com/v1/threads/runs",
            headers=headers,
            json=threads_run_body,
        )
        if thread_run_resp.ok:
            # Try 5 times to get the response
            parsed_resp = thread_run_resp.json()
            thread_id = parsed_resp["thread_id"]
            run_id = parsed_resp["id"]
            assistant_id = parsed_resp["assistant_id"]

            for index in range(20):
                time.sleep(1 + (index * 1))
                response = requests.get(
                    f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}",
                    headers=headers,
                )
                if response.ok:
                    run_response = response.json()
                    status = run_response.get("status")
                    if status in ["cancelled", "failed", "completed"]:
                        if status == "completed":
                            response = requests.get(
                                f"https://api.openai.com/v1/threads/{thread_id}/messages",
                                headers=headers,
                            )
                            if response.ok:
                                threads_messages_resp = response.json()
                                messages = threads_messages_resp.get("data", [])
                                for message in messages:
                                    if message.get("role") == "assistant":
                                        content = message.get("content")
                                        for content_message in content:
                                            if content_message.get("type") == "text":
                                                text = content_message.get("text")

                                                return StradaResponse(
                                                    success=True,
                                                    data={
                                                        "assistant_id": assistant_id,
                                                        "thread_id": thread_id,
                                                        "run_id": run_id,
                                                        "assistant_response": text,
                                                    },
                                                )
                                        # Could not find a text response.
                                        return StradaResponse(
                                            success=False,
                                            error=StradaError(
                                                errorCode=404,
                                                statusCode=404,
                                                message=f"Could not retrieve a 'text' assistant response for thread_id='{thread_id}' and run_id='{run_id}'. This implies that a file was returned instead of a text response.\n Full OpenAI message response is provided in the 'data' field.",
                                            ),
                                            data=messages,
                                        )

                                return StradaResponse(
                                    success=False,
                                    error=StradaError(
                                        errorCode=404,
                                        statusCode=404,
                                        message=f"Could not retrieve assistant response for thread_id='{thread_id}' and run_id='{run_id}'.",
                                    ),
                                    data=threads_messages_resp,
                                )
                            else:
                                return StradaResponse(
                                    success=False,
                                    error=StradaError(
                                        errorCode=response.status_code,
                                        statusCode=response.status_code,
                                        message=f"Error getting messages for thread_id='{thread_id}' and run_id='{run_id}'",
                                    ),
                                    data=run_response,
                                )
                        elif status == "cancelled":
                            return StradaResponse(
                                success=False,
                                error=StradaError(
                                    errorCode=response.status_code,
                                    statusCode=response.status_code,
                                    message=f"Run execution was cancelled by OpenAI for thread_id='{thread_id}' and run_id='{run_id}'. Please try again: {response.text}",
                                ),
                                data=run_response,
                            )
                        elif status == "failed":
                            return StradaResponse(
                                success=False,
                                error=StradaError(
                                    errorCode=response.status_code,
                                    statusCode=response.status_code,
                                    message=f"Run execution failed by OpenAI for thread_id='{thread_id}' and run_id='{run_id}'. Please try again: {response.text}",
                                ),
                                data=run_response,
                            )
                else:
                    return StradaResponse(
                        success=False,
                        error=StradaError(
                            errorCode=response.status_code,
                            statusCode=response.status_code,
                            message=f"Error getting run information for thread_id='{thread_id}' and run_id='{run_id}': {response.text}",
                        ),
                    )

            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=404,
                    statusCode=404,
                    message=f"Could not retrieve assistant response for thread_id='{thread_id}' and run_id='{run_id}' after all retry attempts.",
                ),
            )
        else:
            return StradaResponse(
                success=False,
                error=StradaError(
                    errorCode=thread_run_resp.status_code,
                    statusCode=thread_run_resp.status_code,
                    message=f"Error creating and running thread: {thread_run_resp.text}",
                ),
            )

    @exception_handler
    @debug_logger_execute
    def execute(self, **kwargs):
        if "audio/transcriptions" in self.url or "audio/translations" in self.url:
            return self._execute_with_file(**kwargs)
        elif "/assistants/{assistant_id}/message" in self.url:
            return self._execute_custom_assistant_message(**kwargs)
        else:
            return HttpRequestExecutor.execute(
                dynamic_parameter_json_schema=self.param_schema_definition,
                base_path_params=self.path,
                base_headers=self.headers,
                base_query_params=self.params,
                base_body=self.body,
                base_url=self.url,
                method=self.method,
                header_overrides={
                    "Authorization": f"Bearer {self.token}",
                    "OpenAI-Beta": "assistants=v1",
                    "Content-Type": "application/json",
                },
                function_name=self.function_name,
                app_name="openai-chatgpt",
                **kwargs,
            )

    @staticmethod
    def prepare(data):
        builder = OpenAICustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["access_token"])
            .set_path_params(data.get("path", "{}"))
            .set_headers(data.get("headers", "{}"))
            .set_query_params(data.get("query", "{}"))
            .set_body(data.get("body", "{}"))
            .set_function_name(data.get("function_name", None))
            .build()
        )
