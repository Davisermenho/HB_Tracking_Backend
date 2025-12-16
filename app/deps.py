from typing import List, Union, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone
from app.models import Role, Usuario
from config.config import SessionLocal
from utils.jwt import verify_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = credentials.credentials  # aqui vem SÓ o token, sem "Bearer "
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication payload")

    user = db.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    if not user.role:
        user.role = db.get(Role, user.role_id)

    return user

PASSWORD_CHANGE_ALLOWLIST = {
    "/usuarios/login",
    "/usuarios/change-password",
    "/docs",
    "/openapi.json",
    "/ping-banco",
}

def get_active_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    if current_user.locked_until and current_user.locked_until > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account locked until {current_user.locked_until.isoformat()}",
        )
    if current_user.must_change_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password change required",
        )
    return current_user



def require_role(required_roles: List[Union[int, str]]):
    def _checker(current_user: Usuario = Depends(get_active_user)):
        allowed_ids = {r for r in required_roles if isinstance(r, int)}
        allowed_names = {r for r in required_roles if isinstance(r, str)}

        if current_user.role_id in allowed_ids:
            return current_user
        if current_user.role and current_user.role.role_name in allowed_names:
            return current_user

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return _checker


def user_is_staff_of_team(db: Session, user: Usuario, equipe_id: int) -> bool:
    stmt = select(TeamStaff).where(TeamStaff.equipe_id == equipe_id, TeamStaff.user_id == user.user_id)
    return db.execute(stmt).first() is not None


def get_role_name(user: Usuario) -> Optional[str]:
    return user.role.role_name if user.role else None
