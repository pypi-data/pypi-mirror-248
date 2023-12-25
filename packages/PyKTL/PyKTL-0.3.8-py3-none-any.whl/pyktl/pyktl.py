## This is not an offical Samsung library ##
## This is a python rewrite of the knox-token-library-js library written by Samsung.
## for more info please see: https://www.npmjs.com/package/knox-token-library-js?activeTab=readme
## prerequesits: pip install pycryptodome "pyjwt[crypto]"

import jwt
import json
from datetime import datetime, timedelta
from Crypto.PublicKey import RSA
import uuid
import base64

jwt_id = str(uuid.uuid4()) + str(uuid.uuid4())
expiration_time = datetime.utcnow() + timedelta(minutes=30)

def generate_signed_client_identifier_jwt(certificate_file_name, client_identifier):
    with open(certificate_file_name, 'r', encoding='utf-8') as file:
        certificate = json.load(file)

    privateKeyFromJson = certificate['Private']
    privateKeyString = generate_pem_format(privateKeyFromJson)

    publicKeyFromJson = certificate['Public']
    public_key_binary = base64.b64decode(publicKeyFromJson)
    public_key_der = RSA.import_key(public_key_binary).publickey().export_key('DER')
    public_key_base64 = base64.b64encode(public_key_der).decode('utf-8')

    payload_data = {
        'aud': 'KnoxWSM',
        'clientIdentifier': client_identifier,
        'publicKey': public_key_base64,
        'exp': expiration_time,
        'iat': datetime.utcnow(),
        'jti': jwt_id
    }

    token = jwt.encode(payload_data, privateKeyString, algorithm='RS512')
    return token

def generate_signed_access_token_jwt(certificate_file_name, access_token):
    with open(certificate_file_name, 'r') as file:
        certificate = json.load(file)
    
    privateKeyFromJson = certificate['Private']
    privateKeyString = generate_pem_format(privateKeyFromJson)

    publicKeyFromJson = certificate['Public']
    public_key_binary = base64.b64decode(publicKeyFromJson)
    public_key_der = RSA.import_key(public_key_binary).publickey().export_key('DER')
    public_key_base64 = base64.b64encode(public_key_der).decode('utf-8')

    payload_data = {
        'aud': 'KnoxWSM',
        'accessToken': access_token,
        'publicKey': public_key_base64,
        'exp': expiration_time,
        'iat': datetime.utcnow(),
        'jti': jwt_id
    }

    token = jwt.encode(payload_data, privateKeyString, algorithm='RS512')
    return token

def generate_pem_format(base64_encoded_data):
    certificate= f'-----BEGIN RSA PRIVATE KEY-----\n{base64_encoded_data}\n-----END RSA PRIVATE KEY-----'
    return certificate