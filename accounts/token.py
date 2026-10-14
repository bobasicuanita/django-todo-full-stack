from django.core import signing

SALT = "user_verification"
RESET_SALT = "password_reset"
TOKEN_MAX_AGE = 60 * 60 * 24

def generate_user_token(user_id):
    token = signing.dumps({"user_id": user_id}, salt=SALT)
    return token

def verify_user_token(token):
    try:
        data = signing.loads(token,salt=SALT,max_age=TOKEN_MAX_AGE,)
        return data
    except signing.SignatureExpired:
        return None
    except signing.BadSignature:
        return None
    
def generate_password_reset_token(user_id):
    token = signing.dumps({"user_id": user_id}, salt=RESET_SALT)
    return token

def verify_password_reset_token(token):
    try:
        data = signing.loads(token, salt=RESET_SALT, max_age=TOKEN_MAX_AGE)
        return data
    except signing.SignatureExpired:
        return None
    except signing.BadSignature:
        return None