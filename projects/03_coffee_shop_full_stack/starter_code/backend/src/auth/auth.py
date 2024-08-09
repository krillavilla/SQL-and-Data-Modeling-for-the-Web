from functools import wraps
from flask import request
from jose import jwt, exceptions
import json
from urllib.request import urlopen

AUTH0_DOMAIN = 'udacity-cofshp.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'dev'

# Fetch the JWKS
jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
jwks = json.loads(jsonurl.read())

## AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header
def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description": "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization header must start with Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token

## Check Permissions
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

## Verify Decode JWT
def verify_decode_jwt(token):
    try:
        unverified_header = jwt.get_unverified_header(token)
    except exceptions.JWTError as e:
        raise AuthError({"code": "invalid_header",
                         "description": "Error decoding token headers: " + str(e)}, 401)
    except Exception as e:
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to parse authentication token: " + str(e)}, 400)

    rsa_key = {}
    try:
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
    except Exception as e:
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key: " + str(e)}, 400)

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except exceptions.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "Token expired."}, 401)

        except exceptions.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                             "description": "Incorrect claims. Please, check the audience and issuer."}, 401)
        except Exception as e:
            raise AuthError({"code": "invalid_header",
                             "description": "Unable to parse authentication token: " + str(e)}, 400)
    raise AuthError({"code": "invalid_header",
                     "description": "Unable to find appropriate key"}, 400)

## Requires Auth Decorator
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator