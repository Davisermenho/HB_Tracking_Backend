from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_active_user, get_db, get_role_name, user_is_staff_of_team
from app.models import Atleta, Membership, TeamStaff, Usuario

router = APIRouter(prefix="/atletas", tags=["atletas"])


@router.post("/", response_model=schemas.AtletaOut, status_code=status.HTTP_201_CREATED)
def create_atleta(
    payload: schemas.AtletaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada")

    existing = db.execute(select(Atleta).where(Atleta.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado para atleta")

    atleta = Atleta(
        nome=payload.nome,
        email=payload.email,
        nascimento=payload.nascimento,
        posicao=payload.posicao,
        organization_id=current_user.organization_id,
    )
    db.add(atleta)
    db.commit()
    db.refresh(atleta)
    return atleta


@router.get("/", response_model=List[schemas.AtletaOut])
def list_atletas(
    skip: int = 0,
    limit: int = 100,
    organization_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    org_id = current_user.organization_id
    role_name = get_role_name(current_user)

    if role_name == "atleta":
        atleta = db.execute(
            select(Atleta).where(Atleta.email == current_user.user_email, Atleta.organization_id == org_id)
        ).scalar_one_or_none()
        return [atleta] if atleta else []

    if role_name == "treinador":
        trainer_team_ids = [
            row[0] for row in db.execute(select(TeamStaff.equipe_id).where(TeamStaff.user_id == current_user.user_id)).all()
        ]
        stmt = (
            select(Atleta)
            .join(Membership, Membership.atleta_id == Atleta.id)
            .where(Atleta.organization_id == org_id, Membership.equipe_id.in_(trainer_team_ids))
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    stmt = select(Atleta).where(Atleta.organization_id == org_id).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


@router.get("/{atleta_id}", response_model=schemas.AtletaOut)
def get_atleta(
    atleta_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    atleta = db.get(Atleta, atleta_id)
    if not atleta or atleta.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Atleta not found")
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        if atleta.email != current_user.user_email:
            raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador":
        membership = (
            db.execute(
                select(Membership).where(Membership.atleta_id == atleta_id, Membership.equipe_id.in_(
                    [row[0] for row in db.execute(select(TeamStaff.equipe_id).where(TeamStaff.user_id == current_user.user_id)).all()]
                ))
            ).scalar_one_or_none()
        )
        if not membership:
            raise HTTPException(status_code=403, detail="Permissão negada")
    return atleta


@router.put("/{atleta_id}", response_model=schemas.AtletaOut)
def update_atleta(
    atleta_id: int,
    payload: schemas.AtletaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    atleta = db.get(Atleta, atleta_id)
    if not atleta or atleta.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Atleta not found")

    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador":
        if not user_is_staff_of_team(
            db,
            current_user,
            db.execute(select(Membership.equipe_id).where(Membership.atleta_id == atleta_id)).scalar_one_or_none() or -1,
        ):
            raise HTTPException(status_code=403, detail="Permissão negada")

    if payload.email != atleta.email:
        existing = db.execute(select(Atleta).where(Atleta.email == payload.email)).scalar_one_or_none()
        if existing and existing.id != atleta_id:
            raise HTTPException(status_code=400, detail="Email já cadastrado para atleta")

    atleta.nome = payload.nome
    atleta.email = payload.email
    atleta.nascimento = payload.nascimento
    atleta.posicao = payload.posicao
    atleta.organization_id = current_user.organization_id

    db.add(atleta)
    db.commit()
    db.refresh(atleta)
    return atleta


@router.delete("/{atleta_id}")
def delete_atleta(
    atleta_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    atleta = db.get(Atleta, atleta_id)
    if not atleta or atleta.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Atleta not found")
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador":
        membership = (
            db.execute(
                select(Membership).where(Membership.atleta_id == atleta_id, Membership.equipe_id.in_(
                    [row[0] for row in db.execute(select(TeamStaff.equipe_id).where(TeamStaff.user_id == current_user.user_id)).all()]
                ))
            ).scalar_one_or_none()
        )
        if not membership:
            raise HTTPException(status_code=403, detail="Permissão negada")
    db.delete(atleta)
    db.commit()
    return {"ok": True}
