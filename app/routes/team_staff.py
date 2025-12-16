from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_active_user, get_db, get_role_name, user_is_staff_of_team
from app.models import Equipe, TeamStaff, Usuario

router = APIRouter(prefix="/team-staff", tags=["team_staff"])


@router.post("/", response_model=schemas.TeamStaffOut, status_code=status.HTTP_201_CREATED)
def add_team_staff(
    payload: schemas.TeamStaffCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    role_name = get_role_name(current_user)
    if role_name not in {"dirigente", "coordenador"}:
        raise HTTPException(status_code=403, detail="Permissão negada")

    equipe = db.get(Equipe, payload.equipe_id)
    user = db.get(Usuario, payload.user_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Equipe not found")
    if not user or user.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Usuário não encontrado na mesma organização")

    existing = (
        db.execute(
            select(TeamStaff).where(
                TeamStaff.equipe_id == payload.equipe_id,
                TeamStaff.user_id == payload.user_id,
                TeamStaff.staff_role == payload.staff_role,
            )
        ).scalar_one_or_none()
    )
    if existing:
        return existing

    staff = TeamStaff(
        equipe_id=payload.equipe_id,
        user_id=payload.user_id,
        staff_role=payload.staff_role,
    )
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


@router.get("/", response_model=List[schemas.TeamStaffOut])
def list_team_staff(
    equipe_id: Optional[int] = Query(None),
    user_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    role_name = get_role_name(current_user)
    stmt = select(TeamStaff).join(Equipe).where(Equipe.organization_id == current_user.organization_id)
    if equipe_id:
        stmt = stmt.where(TeamStaff.equipe_id == equipe_id)
    if user_id:
        stmt = stmt.where(TeamStaff.user_id == user_id)

    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador":
        stmt = stmt.where(TeamStaff.user_id == current_user.user_id)

    return db.execute(stmt).scalars().all()


@router.delete("/{team_staff_id}")
def delete_team_staff(
    team_staff_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    staff = db.get(TeamStaff, team_staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Team staff not found")
    equipe = db.get(Equipe, staff.equipe_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Team staff not found")
    role_name = get_role_name(current_user)
    if role_name not in {"dirigente", "coordenador"}:
        raise HTTPException(status_code=403, detail="Permissão negada")
    db.delete(staff)
    db.commit()
    return {"ok": True}
