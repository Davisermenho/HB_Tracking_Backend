import datetime
import uuid

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.config import Base


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="role")


class Usuario(Base):
    __tablename__ = "usuarios"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    user_nome = Column(String(80), nullable=False)
    user_email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), nullable=False)

    failed_login_count = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    must_change_password = Column(Boolean, default=False, nullable=False)

    password_changed_at = Column(DateTime(timezone=True), nullable=True)
    temp_password_expires_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    role = relationship("Role", back_populates="usuarios")
    equipes = relationship("Equipe", back_populates="treinador")
    staff_memberships = relationship("TeamStaff", back_populates="user")
    

class Equipe(Base):
    __tablename__ = "equipes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    categoria = Column(String(50))
    organization_id = Column(UUID(as_uuid=True), nullable=False)
    treinador_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.user_id"), nullable=True)

    treinador = relationship("Usuario", back_populates="equipes")
    memberships = relationship("Membership", back_populates="equipe", cascade="all, delete-orphan")
    staff = relationship("TeamStaff", back_populates="equipe", cascade="all, delete-orphan")


class Atleta(Base):
    __tablename__ = "atletas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    nascimento = Column(Date)
    posicao = Column(String(50))
    organization_id = Column(UUID(as_uuid=True), nullable=False)

    memberships = relationship("Membership", back_populates="atleta", cascade="all, delete-orphan")


class Membership(Base):
    __tablename__ = "memberships"
    __table_args__ = (UniqueConstraint("equipe_id", "atleta_id", name="uq_membership_equipe_atleta"),)

    id = Column(Integer, primary_key=True, index=True)
    equipe_id = Column(Integer, ForeignKey("equipes.id"), nullable=False)
    atleta_id = Column(Integer, ForeignKey("atletas.id"), nullable=False)

    equipe = relationship("Equipe", back_populates="memberships")
    atleta = relationship("Atleta", back_populates="memberships")


class TeamStaff(Base):
    __tablename__ = "team_staff"
    __table_args__ = (UniqueConstraint("equipe_id", "user_id", "staff_role", name="uq_team_staff_unique"),)

    id = Column(Integer, primary_key=True, index=True)
    equipe_id = Column(Integer, ForeignKey("equipes.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.user_id"), nullable=False)
    staff_role = Column(String(50), nullable=False)

    equipe = relationship("Equipe", back_populates="staff")
    user = relationship("Usuario", back_populates="staff_memberships")


class Presenca(Base):
    __tablename__ = "presencas"

    id = Column(Integer, primary_key=True, index=True)
    atleta_id = Column(Integer, ForeignKey("atletas.id"))
    equipe_id = Column(Integer, ForeignKey("equipes.id"))
    data = Column(Date)
    tipo = Column(String(20))
    presente = Column(Boolean)
    obs = Column(String(140))


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    equipe_id = Column(Integer, ForeignKey("equipes.id"))
    atleta_id = Column(Integer, ForeignKey("atletas.id"))
    criado_em = Column(DateTime, default=datetime.datetime.utcnow)
