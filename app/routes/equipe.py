from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.deps import get_active_user, get_db, get_role_name, user_is_staff_of_team
from app.models import Atleta, Equipe, Membership, TeamStaff, Usuario

router = APIRouter(prefix="/equipes", tags=["equipes"])


@router.post("/", response_model=schemas.EquipeOut, status_code=status.HTTP_201_CREATED)
def create_equipe(
    payload: schemas.EquipeCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada")

    org_id = current_user.organization_id
    treinador_id: Optional[UUID] = None

    if role_name == "treinador":
        treinador_id = current_user.user_id
    elif payload.treinador_id:
        treinador = db.get(Usuario, payload.treinador_id)
        if not treinador or treinador.organization_id != org_id:
            raise HTTPException(status_code=404, detail="Treinador not found")
        treinador_id = treinador.user_id

    equipe = Equipe(
        nome=payload.nome,
        categoria=payload.categoria,
        organization_id=org_id,
        treinador_id=treinador_id,
    )
    db.add(equipe)
    db.commit()
    db.refresh(equipe)

    if treinador_id:
        existing_staff = (
            db.execute(
                select(TeamStaff).where(
                    TeamStaff.equipe_id == equipe.id, TeamStaff.user_id == treinador_id, TeamStaff.staff_role == "treinador"
                )
            ).scalar_one_or_none()
        )
        if not existing_staff:
            staff = TeamStaff(equipe_id=equipe.id, user_id=treinador_id, staff_role="treinador")
            db.add(staff)
            db.commit()

    return equipe


@router.get("/", response_model=List[schemas.EquipeOut])
def list_equipes(
    skip: int = 0,
    limit: int = 100,
    organization_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    org_id = current_user.organization_id
    role_name = get_role_name(current_user)

    base_stmt = select(Equipe).where(Equipe.organization_id == org_id)

    if role_name == "atleta":
        atleta = db.execute(
            select(Atleta).where(Atleta.email == current_user.user_email, Atleta.organization_id == org_id)
        ).scalar_one_or_none()
        if not atleta:
            return []
        stmt = (
            select(Equipe)
            .join(Membership, Membership.equipe_id == Equipe.id)
            .where(Equipe.organization_id == org_id, Membership.atleta_id == atleta.id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    if role_name == "treinador":
        stmt = (
            select(Equipe)
            .join(TeamStaff, TeamStaff.equipe_id == Equipe.id)
            .where(Equipe.organization_id == org_id, TeamStaff.user_id == current_user.user_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    stmt = base_stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


@router.get("/{equipe_id}", response_model=schemas.EquipeOut)
def get_equipe(
    equipe_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    e = db.get(Equipe, equipe_id)
    if not e or e.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Equipe not found")
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        atleta = db.execute(
            select(Atleta).where(
                Atleta.email == current_user.user_email, Atleta.organization_id == current_user.organization_id
            )
        ).scalar_one_or_none()
        if not atleta:
            raise HTTPException(status_code=403, detail="Permissão negada")
        membership = (
            db.execute(
                select(Membership).where(Membership.equipe_id == equipe_id, Membership.atleta_id == atleta.id)
            ).scalar_one_or_none()
        )
        if not membership:
            raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador":
        if not user_is_staff_of_team(db, current_user, equipe_id):
            raise HTTPException(status_code=403, detail="Permissão negada")
    return e


@router.put("/{equipe_id}", response_model=schemas.EquipeOut)
def update_equipe(
    equipe_id: int,
    payload: schemas.EquipeCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_active_user),
):
    e = db.get(Equipe, equipe_id)
    if not e or e.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Equipe not found")

    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")

    treinador = None
    if payload.treinador_id:
        treinador = db.get(Usuario, payload.treinador_id)
        if not treinador:
            raise HTTPException(status_code=404, detail="Treinador not found")
        if treinador.organization_id != current_user.organization_id:
            raise HTTPException(status_code=403, detail="Treinador de outra organização")

    e.nome = payload.nome
    e.categoria = payload.categoria
    e.organization_id = current_user.organization_id
    e.treinador_id = treinador.user_id if payload.treinador_id else None

    db.add(e)
    db.commit()
    db.refresh(e)
    return e


@router.delete("/{equipe_id}")
def delete_equipe(
    equipe_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_active_user)
):
    e = db.get(Equipe, equipe_id)
    if not e or e.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Equipe not found")
    role_name = get_role_name(current_user)
    if role_name == "atleta":
        raise HTTPException(status_code=403, detail="Permissão negada")
    if role_name == "treinador" and not user_is_staff_of_team(db, current_user, equipe_id):
        raise HTTPException(status_code=403, detail="Permissão negada")
    db.delete(e)
    db.commit()
    return {"ok": True}
