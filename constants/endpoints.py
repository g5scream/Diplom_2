class Endpoints:
    BASE_URL = "https://stellarburgers.education-services.ru"

    REGISTER = f"{BASE_URL}/api/auth/register"             # POST
    LOGIN = f"{BASE_URL}/api/auth/login"                   # POST
    LOGOUT = f"{BASE_URL}/api/auth/logout"                 # POST
    PASS_RESET = f"{BASE_URL}/api/password-reset"          # POST
    USER = f"{BASE_URL}/api/auth/user"                     # GET, PATCH, DELETE
    TOKEN_UPDATE = f"{BASE_URL}/api/auth/token"            # POST

    INGREDIENTS = f"{BASE_URL}/api/ingredients"             # GET

    CREATE_ORDER  = f"{BASE_URL}/api/orders"               # POST
    ORDER = f"{BASE_URL}/api/orders/all"                   # GET

    



