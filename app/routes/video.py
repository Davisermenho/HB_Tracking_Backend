from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_active_user, get_db, get_role_name, user_is_staff_of_team
from app.models import Atleta, Equipe, Membership, TeamStaff, Usuario, Video

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("/", response_model=schemas.VideoOut, status_code=status.HTTP_201_CREATED)
def create_video(
    payload: schemas.VideoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")

    equipe = db.get(Equipe, payload.equipe_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Equipe not found")

    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, payload.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")

    if payload.atleta_id:
        atleta = db.get(Atleta, payload.atleta_id)
        if not atleta or atleta.organization_id != current_user.organization_id:
            raise HTTPException(status_code=404, detail="Atleta not found")

    v = Video(**payload.model_dump())
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


@router.get("/", response_model=List[schemas.VideoOut])
def list_videos(
    skip: int = 0,
    limit: int = 100,
    equipe_id: Optional[int] = Query(None),
    atleta_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    role_name = get_role_name(current_user)
    org_id = current_user.organization_id
    stmt = select(Video).join(Equipe).where(Equipe.organization_id == org_id)
    if equipe_id:
        stmt = stmt.where(Video.equipe_id == equipe_id)
    if atleta_id:
        stmt = stmt.where(Video.atleta_id == atleta_id)

    if role_name == "atleta":
        atleta = db.execute(
            select(Atleta).where(Atleta.email == current_user.user_email, Atleta.organization_id == org_id)
        ).scalar_one_or_none()
        if not atleta:
            return []
        team_ids = [row[0] for row in db.execute(select(Membership.equipe_id).where(Membership.atleta_id == atleta.id)).all()]
        if not team_ids:
            return []
        stmt = stmt.where(Video.equipe_id.in_(team_ids))
        if atleta_id is None:
            stmt = stmt.where(or_(Video.atleta_id.is_(None), Video.atleta_id == atleta.id))
        else:
            stmt = stmt.where(Video.atleta_id == atleta.id)
    elif role_name == "treinador":
        team_ids = [row[0] for row in db.execute(select(TeamStaff.equipe_id).where(TeamStaff.user_id == current_user.user_id)).all()]
        stmt = stmt.where(Video.equipe_id.in_(team_ids))

    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


@router.get("/{video_id}", response_model=schemas.VideoOut)
def get_video(
    video_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    v = db.get(Video, video_id)
    if not v:
        raise HTTPException(status_code=404, detail="Video not found")
    equipe = db.get(Equipe, v.equipe_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Video not found")
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        atleta = db.execute(
            select(Atleta).where(Atleta.email == current_user.user_email, Atleta.organization_id == current_user.organization_id)
        ).scalar_one_or_none()
        team_ids = []
        if atleta:
            team_ids = [row[0] for row in db.execute(select(Membership.equipe_id).where(Membership.atleta_id == atleta.id)).all()]
        if not atleta or (v.atleta_id not in (None, atleta.id) and v.equipe_id not in team_ids):
            raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, v.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")
    return v


@router.put("/{video_id}", response_model=schemas.VideoOut)
def update_video(
    video_id: int,
    payload: schemas.VideoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    v = db.get(Video, video_id)
    if not v:
        raise HTTPException(status_code=404, detail="Video not found")
    equipe_current = db.get(Equipe, v.equipe_id)
    if not equipe_current or equipe_current.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Video not found")

    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, v.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")

    equipe_new = db.get(Equipe, payload.equipe_id)
    if not equipe_new or equipe_new.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Equipe not found")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, payload.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")

    if payload.atleta_id:
        atleta_new = db.get(Atleta, payload.atleta_id)
        if not atleta_new or atleta_new.organization_id != current_user.organization_id:
            raise HTTPException(status_code=404, detail="Atleta not found")

    for k, val in payload.model_dump().items():
        setattr(v, k, val)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


@router.delete("/{video_id}")
def delete_video(
    video_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    v = db.get(Video, video_id)
    if not v:
        raise HTTPException(status_code=404, detail="Video not found")
    equipe = db.get(Equipe, v.equipe_id)
    if not equipe or equipe.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Video not found")
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, v.equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")
    db.delete(v)
    db.commit()
    return {"ok": True}
