

def SEND_DATA(data):
    return {"message": data, "status": "success"}



def SEND_LOGIN_MESSAGE(id, email, token):
    return {'user_id': id, 'message': 'Logged in successfully', 'email': email, "token": token, "status": "success"}


def SEND_REGISTRATION_MESSAGE(id, email, token):
    return {'user_id': id, 'message': 'Registered successfully', 'email': email, "token": token, "status": "success"}


SUCCESS_CREATED = {'message': 'Created successfully', "status": "success"}
SUCCESS_UPDATED = {'message': 'Updated successfully', "status": "success"}
SUCCESS_DELETED = {'message': 'Deleted successfully', "status": "success"}

ERROR_NOBODY_OWES = {"message": "Nobody owes nobody", "status": "error"}

ERROR_ITEM_NOT_FOUND = {'message': 'Item not found', "status": "error"}
ERROR_MISSING_VALUES = {"message": "Provide all values", "status": "error"}
ERROR_MISSIN_NUMERIC = {"message": "Provide numeric values!", "status": "error"}
ERROR_USER_EXISTS = {"message": "User already exists", "status": "error"}
ERROR_INVALID_USER = {"message": "Invalid mail or password", "status": "error"}

ERROR_PAGE_NOT_FOUND = {'message': 'Not found', "status": "error"}
ERROR_NO_AUTHENTICATION = {"message": "You need authentication", "status": "error"}
ERROR_TOKEN_EXPIRED = {"message": "Your token has expired. Please login again.", "status": "error"}
ERROR_INTERNAL_SERVER = {"message": "Internal server error", "status": "error"}
