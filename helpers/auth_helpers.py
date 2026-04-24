def _get_auth_headers(access_token):
    if access_token:
        return {"Authorization": access_token}
    return {}