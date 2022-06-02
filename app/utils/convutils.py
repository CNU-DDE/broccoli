from django.conf import settings

def user_type(is_employee):
    runmode = 0 if settings.RUNMODE == "production" else 2
    return runmode + (1 if is_employee else 0)

def error_message(err):
    return f"Unexpected error {err} with error type {type(err)}"
