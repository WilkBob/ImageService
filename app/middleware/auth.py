from fastapi import Request, HTTPException, Depends
import firebase_admin
from firebase_admin import auth, credentials
import os

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the full path to the JSON file
json_path = os.path.join(script_dir, 'web-size-firebase-adminsdk-n54om-d838700b79.json')

# Use the full path to initialize the credentials
cred = credentials.Certificate(json_path)
default_app = firebase_admin.initialize_app(cred)

async def verify_token(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(status_code=401, detail='Authorization header missing')

    try:
        id_token = auth_header.split(' ')[1]
        user = auth.verify_id_token(id_token)
        return user
    except Exception as e:
        raise HTTPException(status_code=403, detail='Invalid token')

async def conditional_token_verification(request: Request):
    form = await request.form()
    files = form.getlist('files')
    if len(files) > 1:
        return await verify_token(request)
    return None