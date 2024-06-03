from uuid import uuid4
from fastapi import APIRouter, Body,status, HTTPException
from pydantic import UUID4
from workout_api.categorias.schemas import Categoriain, CategoriaOut
from workout_api.contrib.repository.dependencies import DatabaseDependency
from workout_api.categorias.models import CategoriesModel
from sqlalchemy.future import select
router = APIRouter()

@router.post(
    '/',
    summary='Criar uma nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(db_session: DatabaseDependency,categoria_in:Categoriain = Body(...))->CategoriaOut:
    categoria_out = CategoriaOut(id = uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriesModel(**categoria_out.model_dump())

    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out
    breakpoint()
    pass

@router.get(
    '/', 
    summary='Consultar todas as Categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def query(
    db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriesModel))).scalars().all()
    return categorias

@router.get(
    '/{id}', 
    summary='Consultar uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriesModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )
    
    return categoria