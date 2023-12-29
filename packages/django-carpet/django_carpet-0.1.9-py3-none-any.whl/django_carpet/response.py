# Python
import json

# Django
from django.http.response import HttpResponse

# Third Party
from typing import Optional, Any

# Project
from .choices import ResponseChoices


class NotLoggedResponse(HttpResponse):

    def __init__(self):
        super().__init__(json.dumps({'result': 'not logged'}), status=401)


class APIResponse(HttpResponse):

    def __init__(self, response, request, status=200):
        if request.token is not None and request.token != '':
            super().__init__(json.dumps(response, default=str), content_type='application/json', status=status)
        else:
            super().__init__(json.dumps(response, default=str), status=status)


class NotAllowedResponse(HttpResponse):

    def __init__(self, reason: Optional[str] = None):
        super().__init__(json.dumps({'result': 'not allowed', 'reason': reason or ""}), status=405)


class VieoloResponse:

    def __init__(self, result: str, obj: str | None = None, type_of_object: str | None = None, operation: str | None = None, reason: str | None = None, message: str | None = None, status_code: int | None = None):
        self.result = result
        self.obj = obj
        self.type_of_object = type_of_object
        self.operation = operation
        self.reason = reason
        self.message = message
        self.response_object = {}
        self.status_code = status_code

    def __str__(self) -> str:
        return str(self.response_object)

    def is_successful(self) -> bool:
        return self.result == ResponseChoices.success
    
    def is_does_not_exist(self) -> bool:
        return self.result == ResponseChoices.does_not_exist

    def is_already_exists(self) -> bool:
        return self.result == ResponseChoices.already_exists

    def is_invalid(self) -> bool:
        return self.result == ResponseChoices.not_valid

    def is_not_allowed(self) -> bool:
        return self.result == ResponseChoices.not_allowed


def generate_response(result, obj=None, type_of_object=None, operation=None, reason=None, message=None) -> dict[str, Any]:
    response = {
        "result": result
    }
    if obj is not None:
        response["object"] = obj
    if type_of_object is not None:
        response["type"] = type_of_object
    if operation is not None:
        response["operation"] = operation
    if reason is not None:
        response["reason"] = reason
    if message is not None:
        response["message"] = message

    return response
