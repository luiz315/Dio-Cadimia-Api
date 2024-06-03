from fastapi import APIRouter 
from workout_api.atleta.controller import router as atleta
from workout_api.categorias.controller import router as categorias
from workout_api.centro_treinamento.controller import router as centro_treinamneto

api_router=APIRouter()
api_router.include_router(atleta,prefix='/atleta',tags=['atleta'], )
api_router.include_router(categorias,prefix='/categorias',tags=['categorias'] )
api_router.include_router(centro_treinamneto,prefix='/centroTreinamento',tags=['centro_treinamento'] )


