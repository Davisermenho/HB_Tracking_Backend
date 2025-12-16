from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.models import Usuario
from config.config import SessionLocal
from utils.jwt import create_access_token
from utils.security import verify_password

LOCK_THRESHOLD = 5
LOCK_MINUTES = 60

router = APIRouter(tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    stmt = select(Usuario).where(Usuario.user_email == login_data.user_email)
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Dados inválidos")

    if user.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário removido")
    if user.locked_until and user.locked_until > now:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Conta bloqueada até {user.locked_until.isoformat()}",
        )

    if user.must_change_password:
        if user.temp_password_expires_at is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Senha temporária não provisionada",
            )
        if user.temp_password_expires_at and user.temp_password_expires_at < now:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Temporary password expired",
            )

    if not verify_password(login_data.password, user.password_hash):
        user.failed_login_count = (user.failed_login_count or 0) + 1
        if user.failed_login_count >= LOCK_THRESHOLD:
            user.locked_until = now + timedelta(minutes=LOCK_MINUTES)
            user.failed_login_count = 0
        db.add(user)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Dados inválidos")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

    user.failed_login_count = 0
    user.locked_until = None
    user.last_login_at = now
    db.add(user)
    db.commit()
    db.refresh(user)

    must_change = bool(user.must_change_password)
    access_token = create_access_token(
        {
            "sub": str(user.user_id),
            "role_id": user.role_id,
            "organization_id": str(user.organization_id),
            "user_email": user.user_email,
            "must_change_password": must_change,
        }
    )
    return {"access_token": access_token, "token_type": "bearer", "must_change_password": must_change}
