def user_type(is_employee):
    return (1 if is_employee else 0)

def error_message(err):
    return f"Unexpected error {err} with error type {type(err)}"

def public_key(did):
    return did.split(":")[-1]
