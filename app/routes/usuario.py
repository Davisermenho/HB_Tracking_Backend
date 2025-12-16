from datetime import datetime, timedelta, timezone
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_active_user, get_current_user, get_db, require_role
from app.models import Role, Usuario
from utils.jwt import create_access_token
from utils.security import hash_password, verify_password

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

LOCK_THRESHOLD = 5
LOCK_MINUTES = 60


@router.post("/", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_usuario(
    payload: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["dirigente", "coordenador"])),
):
    role = db.get(Role, payload.role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role_id")

    existing = (
        db.execute(select(Usuario).where(Usuario.user_email == payload.user_email, Usuario.deleted_at.is_(None)))
        .scalar_one_or_none()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed = hash_password(payload.password)
   
    expires = datetime.now(timezone.utc) + timedelta(days=7)

    db_usuario = Usuario(
        user_nome=payload.user_nome,
        user_email=payload.user_email,
        password_hash=hashed,
        role_id=payload.role_id,
        organization_id=current_user.organization_id,
        is_active=payload.is_active,
        must_change_password=True,
        temp_password_expires_at=expires,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario



@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    user = db.execute(
        select(Usuario).where(Usuario.user_email == payload.user_email, Usuario.deleted_at.is_(None))
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if user.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User deleted")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")

    if user.locked_until and user.locked_until > now:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account locked until {user.locked_until.isoformat()}",
        )

    # Se está marcado para troca de senha, precisa ter expiração provisionada ou válida
    if user.must_change_password:
        if user.temp_password_expires_at is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Temporary password not provisioned",
            )
        if now > user.temp_password_expires_at:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Temporary password expired",
            )

    if not verify_password(payload.password, user.password_hash):
        user.failed_login_count = (user.failed_login_count or 0) + 1
        if user.failed_login_count >= LOCK_THRESHOLD:
            user.locked_until = now + timedelta(minutes=LOCK_MINUTES)
            user.failed_login_count = 0
        db.add(user)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    user.failed_login_count = 0
    user.locked_until = None
    user.last_login_at = now
    
    db.add(user)
    db.commit()
    db.refresh(user)
    must_change = bool(user.must_change_password)
    token = create_access_token(
        {
            "sub": str(user.user_id),
            "role_id": user.role_id,
            "organization_id": str(user.organization_id),
            "user_email": user.user_email,
            "must_change_password": must_change,
        }
    )
    return {"access_token": token, "token_type": "bearer", "must_change_password": must_change}
    


@router.get("/", response_model=List[schemas.UsuarioOut])
def list_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["dirigente", "coordenador", "treinador"])),
):
    stmt = (
        select(Usuario)
        .where(Usuario.organization_id == current_user.organization_id, Usuario.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()


@router.get("/{usuario_id}", response_model=schemas.UsuarioOut)
def get_usuario(
    usuario_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["dirigente", "coordenador", "treinador"])),
):
    u = db.get(Usuario, usuario_id)
    if not u or u.organization_id != current_user.organization_id or u.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return u


@router.put("/{usuario_id}", response_model=schemas.UsuarioOut)
def update_usuario(
    usuario_id: UUID,
    payload: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["dirigente", "coordenador"])),
):
    u = db.get(Usuario, usuario_id)
    if not u or u.organization_id != current_user.organization_id or u.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Usuario not found")

    data = payload.model_dump(exclude_unset=True)
    if "role_id" in data:
        role = db.get(Role, data["role_id"])
        if not role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role_id")
    if "password" in data:
        data["password_hash"] = hash_password(data.pop("password"))
        data["password_changed_at"] = datetime.now(timezone.utc)
        data["must_change_password"] = False
        data["temp_password_expires_at"] = None
    if "user_email" in data:
        data.pop("user_email", None)
    for k, v in data.items():
        setattr(u, k, v)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.delete("/{usuario_id}")
def delete_usuario(
    usuario_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role(["dirigente", "coordenador"])),
):
    u = db.get(Usuario, usuario_id)
    if not u or u.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Usuario not found")
    now = datetime.now(timezone.utc)
    u.deleted_at = now
    u.is_active = False
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"ok": True, "deleted_at": u.deleted_at.isoformat()}


@router.post("/change-password")
def change_password(
    payload: schemas.ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    if not verify_password(payload.old_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha atual inválida")
    current_user.password_hash = hash_password(payload.new_password)
    current_user.must_change_password = False
    current_user.password_changed_at = datetime.now(timezone.utc)
    current_user.temp_password_expires_at = None
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"ok": True}
