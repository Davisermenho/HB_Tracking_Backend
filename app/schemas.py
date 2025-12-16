from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class RoleOut(BaseModel):
    role_id: int
    role_name: str
    model_config = {"from_attributes": True}


class UsuarioBase(BaseModel):
    user_nome: str
    user_email: EmailStr
    role_id: int
 
 
class UsuarioCreate(BaseModel):
    user_nome: str
    user_email: EmailStr
    password: str
    role_id: int
    is_active: bool = True


class UsuarioUpdate(BaseModel):
    user_nome: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
    must_change_password: Optional[bool] = None
    model_config = {"extra": "forbid"}


class UsuarioOut(BaseModel):
    user_id: UUID
    user_nome: str
    user_email: EmailStr
    role_id: int
    organization_id: UUID
    is_active: bool
    must_change_password: bool
    failed_login_count: int
    locked_until: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    password_changed_at: Optional[datetime] = None
    temp_password_expires_at: Optional[datetime] = None
    
    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UsuarioLogin(BaseModel):
    user_email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    must_change_password: bool = False


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    role_id: Optional[int] = None
    organization_id: Optional[str] = None


class EquipeCreate(BaseModel):
    nome: str
    categoria: Optional[str] = None
    treinador_id: Optional[UUID] = None


class EquipeOut(BaseModel):
    id: int
    nome: str
    categoria: Optional[str]
    organization_id: UUID
    treinador_id: Optional[UUID]
    model_config = {"from_attributes": True}


class AtletaCreate(BaseModel):
    nome: str
    email: EmailStr
    nascimento: Optional[date] = None
    posicao: Optional[str] = None


class AtletaOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    nascimento: Optional[date]
    posicao: Optional[str]
    organization_id: UUID
    model_config = {"from_attributes": True}


class MembershipCreate(BaseModel):
    equipe_id: int
    atleta_id: int


class MembershipOut(BaseModel):
    id: int
    equipe_id: int
    atleta_id: int
    model_config = {"from_attributes": True}


class TeamStaffCreate(BaseModel):
    equipe_id: int
    user_id: UUID
    staff_role: str


class TeamStaffOut(BaseModel):
    id: int
    equipe_id: int
    user_id: UUID
    staff_role: str
    model_config = {"from_attributes": True}


class PresencaCreate(BaseModel):
    atleta_id: int
    equipe_id: int
    data: date
    tipo: Optional[str] = None
    presente: Optional[bool] = None
    obs: Optional[str] = None


class PresencaOut(BaseModel):
    id: int
    atleta_id: int
    equipe_id: int
    data: date
    tipo: Optional[str]
    presente: Optional[bool]
    obs: Optional[str]
    model_config = {"from_attributes": True}


class VideoCreate(BaseModel):
    url: str
    equipe_id: int
    atleta_id: Optional[int] = None


class VideoOut(BaseModel):
    id: int
    url: str
    equipe_id: int
    atleta_id: Optional[int]
    criado_em: datetime
    model_config = {"from_attributes": True}


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
