from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_active_user, get_db, get_role_name, user_is_staff_of_team
from app.models import Atleta, Equipe, Membership, TeamStaff, Usuario

router = APIRouter(prefix="/memberships", tags=["memberships"])


@router.post("/", response_model=schemas.MembershipOut, status_code=status.HTTP_201_CREATED)
def add_membership(
    payload: schemas.MembershipCreate,
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

    existing = (
        db.execute(
            select(Membership).where(Membership.equipe_id == payload.equipe_id, Membership.atleta_id == payload.atleta_id)
        ).scalar_one_or_none()
    )
    if existing:
        return existing

    membership = Membership(equipe_id=payload.equipe_id, atleta_id=payload.atleta_id)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.get("/", response_model=List[schemas.MembershipOut])
def list_memberships(
    equipe_id: Optional[int] = Query(None),
    atleta_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    role_name = get_role_name(current_user)
    stmt = (
        select(Membership)
        .join(Equipe, Equipe.id == Membership.equipe_id)
        .join(Atleta, Atleta.id == Membership.atleta_id)
        .where(Equipe.organization_id == current_user.organization_id)
    )
    if equipe_id:
        stmt = stmt.where(Membership.equipe_id == equipe_id)
    if atleta_id:
        stmt = stmt.where(Membership.atleta_id == atleta_id)

    if role_name == "atleta":
        atleta = db.execute(
            select(Atleta).where(Atleta.email == current_user.user_email, Atleta.organization_id == current_user.organization_id)
        ).scalar_one_or_none()
        if not atleta:
            return []
        stmt = stmt.where(Membership.atleta_id == atleta.id)
    elif role_name == "treinador":
        trainer_team_ids = [
            row[0] for row in db.execute(select(TeamStaff.equipe_id).where(TeamStaff.user_id == current_user.user_id)).all()
        ]
        stmt = stmt.where(Membership.equipe_id.in_(trainer_team_ids))

    return db.execute(stmt).scalars().all()


@router.delete("/{membership_id}")
def delete_membership(
    membership_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    membership = db.get(Membership, membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    equipe = db.get(Equipe, membership.equipe_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Membership not found")
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, membership.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")
    db.delete(membership)
    db.commit()
    return {"ok": True}
