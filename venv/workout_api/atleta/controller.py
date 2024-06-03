from fastapi import APIRouter, Body,status, HTTPException
from typing import Any
from workout_api.atleta.schemas import AtletaIn,AtletaOut,AtletaUpdate,AtletaBasicOut
from workout_api.contrib.repository.dependencies import DatabaseDependency
from workout_api.atleta.models import AtletaModel
from sqlalchemy.future import select
from workout_api.categorias.models import CategoriesModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from fastapi_pagination import LimitOffsetPage, paginate

from pydantic import Field,UUID4
from uuid import uuid4


router = APIRouter()

@router.post('/',
    summary='Criar novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model= AtletaOut
)
async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriesModel).filter_by(nome=categoria_nome))
    ).scalars().first()
    """cpf= (await db_session.execute(
        select(AtletaModel).filter_by(nome=numero_cpf))
    ).scalars().first()
    """
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'A categoria {categoria_nome} não foi encontrada.'
        )
    
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()
        
    except IntegrityError:

        db_session.rollback()

        cpf = atleta_out.cpf

        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, 
            detail=f'Já existe um atleta cadastrado com o cpf: {cpf}'
        )

    return atleta_out

@router.get(
    '/', 
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaBasicOut],
)
async def query(db_session: DatabaseDependency) -> LimitOffsetPage[AtletaBasicOut]:

    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    atletas_basic_out = [AtletaBasicOut.model_validate(atleta) for atleta in atletas]
    return paginate(atletas_basic_out)

# @router.get(
#     '/{nome}', 
#     summary='Consulta um Atleta pelo Nome',
#     status_code=status.HTTP_200_OK,
#     response_model=AtletaOut,
# )
# async def get(nome, db_session: DatabaseDependency) -> AtletaOut:
#     atleta: AtletaOut = (
#         await db_session.execute(select(AtletaModel).filter_by(nome=nome))
#     ).scalars().first()
#     return atleta



@router.get(
    '/{id}', 
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, nome: str, cpf: str, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    return atleta
@router.get(
    '/{nome}', 
    summary='Consulta um Atleta pelo nome',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_by_name(nome: str, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(nome=nome))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado com nome: {nome}'
        )

    return atleta


@router.get(
    '/{cpf}', 
    summary='Consulta um Atleta pelo cpf',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_by_cpf(cpf: str, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado com cpf: {cpf}'
        )

    return atleta



@router.patch(
    '/{id}', 
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    '/{id}', 
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    await db_session.delete(atleta)
    await db_session.commit()
