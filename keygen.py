import secrets


def generate_secret_key(length=64):
    return secrets.token_urlsafe(length)


secret_key = generate_secret_key(64)
print(secret_key)


