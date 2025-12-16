from typing import List, Optional
from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_active_user, get_db, get_role_name, user_is_staff_of_team
from app.models import Atleta, Equipe, Membership, Presenca, TeamStaff, Usuario

router = APIRouter(prefix="/presencas", tags=["presencas"])


@router.post("/", response_model=schemas.PresencaOut, status_code=status.HTTP_201_CREATED)
def create_presenca(
    payload: schemas.PresencaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")

    equipe = db.get(Equipe, payload.equipe_id)
    atleta = db.get(Atleta, payload.atleta_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Equipe not found")
    if not atleta or atleta.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Atleta not found")

    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, payload.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")

    p = Presenca(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.get("/", response_model=List[schemas.PresencaOut])
def list_presencas(
    skip: int = 0,
    limit: int = 100,
    equipe_id: Optional[int] = Query(None),
    atleta_id: Optional[int] = Query(None),
    data: Optional[date_type] = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    role_name = get_role_name(current_user)
    org_id = current_user.organization_id
    stmt = select(Presenca).join(Equipe).where(Equipe.organization_id == org_id)
    if equipe_id:
        stmt = stmt.where(Presenca.equipe_id == equipe_id)
    if atleta_id:
        stmt = stmt.where(Presenca.atleta_id == atleta_id)
    if data:
        stmt = stmt.where(Presenca.data == data)

    if role_name == "atleta":
        atleta = db.execute(
            select(Atleta).where(Atleta.email == current_user.user_email, Atleta.organization_id == org_id)
        ).scalar_one_or_none()
        if not atleta:
            return []
        team_ids = [row[0] for row in db.execute(select(Membership.equipe_id).where(Membership.atleta_id == atleta.id)).all()]
        if not team_ids:
            return []
        stmt = stmt.where(Presenca.equipe_id.in_(team_ids), Presenca.atleta_id == atleta.id)
    elif role_name == "treinador":
        team_ids = [row[0] for row in db.execute(select(TeamStaff.equipe_id).where(TeamStaff.user_id == current_user.user_id)).all()]
        stmt = stmt.where(Presenca.equipe_id.in_(team_ids))

    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


@router.get("/{presenca_id}", response_model=schemas.PresencaOut)
def get_presenca(
    presenca_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    p = db.get(Presenca, presenca_id)
    if not p:
        raise HTTPException(status_code=404, detail="Presenca not found")
    equipe = db.get(Equipe, p.equipe_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Presenca not found")
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        atleta = db.execute(
            select(Atleta).where(Atleta.email == current_user.user_email, Atleta.organization_id == current_user.organization_id)
        ).scalar_one_or_none()
        if not atleta or atleta.id != p.atleta_id:
            raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, p.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")
    return p


@router.put("/{presenca_id}", response_model=schemas.PresencaOut)
def update_presenca(
    presenca_id: int,
    payload: schemas.PresencaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    p = db.get(Presenca, presenca_id)
    if not p:
        raise HTTPException(status_code=404, detail="Presenca not found")
    equipe = db.get(Equipe, p.equipe_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Presenca not found")

    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, p.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")

    equipe_new = db.get(Equipe, payload.equipe_id)
    atleta_new = db.get(Atleta, payload.atleta_id)
    if not equipe_new or equipe_new.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Equipe not found")
    if not atleta_new or atleta_new.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Atleta not found")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, payload.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")

    for k, v in payload.model_dump().items():
        setattr(p, k, v)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.delete("/{presenca_id}")
def delete_presenca(
    presenca_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    p = db.get(Presenca, presenca_id)
    if not p:
        raise HTTPException(status_code=404, detail="Presenca not found")
    equipe = db.get(Equipe, p.equipe_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Presenca not found")
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, p.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")
    db.delete(p)
    db.commit()
    return {"ok": True}
