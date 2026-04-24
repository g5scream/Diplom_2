class StatusCode: # HTTP status codes
    
    HTTP_200_OK = 200
    HTTP_202_OK = 202

    BAD_REQUEST = 400
    UNAUTH = 401
    FORBIDDEN = 403

    INTERNAL_SERVER_ERROR = 500

class TextResponse: # Error messages
    
    USER_CREATED = "User created successfully"
    LOGOUT_SUCCESS = "Successful logout"
    USER_EXISTS = "User already exists"
    EMAIL_EXISTS = "User with such email already exists"
    MISSING_FIELDS = "Email, password and name are required fields"
    INVALID_CREDENTIALS = "email or password are incorrect"

    MISSING_INGREDIENTS = "Ingredient ids must be provided"
    INTERNAL_ERROR = "Internal Server Error"
    UNAUTHORIZED = "You should be authorised"

    ОК_RESET_EMAIL = "Reset email sent"
    ОК_PASS_RESET = "Password successfully reset"
    OK_DELETE = "User successfully removed"
