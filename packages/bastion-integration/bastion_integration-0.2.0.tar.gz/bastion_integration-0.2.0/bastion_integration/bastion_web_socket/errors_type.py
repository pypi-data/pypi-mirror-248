from enum import Enum


class BastionErrorTypes(Enum):
    read_message_error = {
        'message': "Read message error",
        'error_code': {'class': 1,
                       'subclass': 2}
    }
    send_message_error = {
        'message': "Send message error",
        'error_code': {'class': 1,
                       'subclass': 3}
    }
    response_error = {
        'message': "Response error",
        'error_code': {'class': 1,
                       'subclass': 4}
    }
    department_exist_error = {
        'message': "Department already exist",
        'error_code': {'class': 1,
                       'subclass': 5}
    }
    department_not_found_error = {
        'message': "Department not found",
        'error_code': {'class': 1,
                       'subclass': 6}
    }
    organization_already_exist_error = {
        "message": "Organization already exist",
        "error_code": {
            "class": 1,
            "subclass": 7
        }
    }
    organization_not_found_error = {
        "message": "Organization not found",
        "error_code": {
            "class": 1,
            "subclass": 8
        }
    }
    department_parent_not_found_error = {
        "message": "Department parent not found",
        "error_code": {
            "class": 1,
            "subclass": 9
        }
    }
    person_already_exist_error = {
        "message": "Person already exist",
        "error_code": {
            "class": 1,
            "subclass": 10
        }
    }
    pass_category_not_found_error = {
        "message": "Pass category not found",
        "error_code": {
            "class": 1,
            "subclass": 11
        }
    }
    access_level_not_found_error = {
        "message": "Access level not found",
        "error_code": {
            "class": 1,
            "subclass": 12
        }
    }
    integration_not_enabled_error = {
        "message": "Integration not enabled",
        "error_code": {
            "class": 1,
            "subclass": 13
        }
    }





def get_bastion_error(error_code: BastionErrorTypes, custom_message: str = None, add_message: str = None):
    if custom_message is not None:
        error_code.value['message'] = custom_message
    if add_message is not None:
        error_code.value['message'] = error_code.value['message'] + ": " + add_message
    return {'message': error_code.value['message'], 'context': error_code.value['error_code']}