from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from descope import DescopeClient

client = DescopeClient(project_id="YOUR_DESCOPE_PROJECT_ID")
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        return client.validate_session(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
