import secrets

def custom_id():
    return secrets.token_hex(8)