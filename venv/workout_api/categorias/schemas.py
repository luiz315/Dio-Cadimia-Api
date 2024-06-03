from typing import Annotated
from pydantic import Field,UUID4
from workout_api.contrib.schemas import BaseSchema


class Categoriain(BaseSchema):
    nome: Annotated[str, Field(description = 'nome da categoria', example= 'scale', max_length= 10)]

class CategoriaOut(Categoriain):
    id: Annotated[UUID4, Field(description='Identificador da categoria ')]