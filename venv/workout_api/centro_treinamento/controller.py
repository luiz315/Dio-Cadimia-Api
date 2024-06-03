from uuid import uuid4
from fastapi import APIRouter, Body,status, HTTPException
from pydantic import UUID4
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn,CentroTreinamentoOut,CentroTreinamentoAtleta
from workout_api.contrib.repository.dependencies import DatabaseDependency
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.future import select
router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo Centro de Treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(db_session: DatabaseDependency,centro_treinamento_in:CentroTreinamentoIn = Body(...))->CentroTreinamentoOut:
    centros_treinamento = CentroTreinamentoOut(id = uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centros_treinamento.model_dump())

    db_session.add(centro_treinamento_model)
    await db_session.commit()
    return centros_treinamento
    breakpoint()
    pass

@router.get(
    '/', 
    summary='Consultar todos os Centros de Treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(
    db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return centros_treinamento

@router.get(
    '/{id}', 
    summary='Consultar uma Centro de Treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centros_treinamento: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centros_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Centro de treinamento não encontrado no id: {id}'
        )
    
    return centros_treinamento