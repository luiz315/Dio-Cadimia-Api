from typing import Annotated
from pydantic import Field,UUID4
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description = 'Centro de Treinamento', example= 'CT king', max_length= 20)]
    endereco: Annotated[str, Field(description = 'Endereço do Centro de Treinamento', example= 'Sq 11 quadra 05 casa 58', max_length= 60)]
    proprietario: Annotated[str, Field(description = 'proprietario do Centro de Treinamento', example= 'Claudin', max_length= 20)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description = 'Centro de Treinamento', example= 'CT king', max_length= 20)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='Identificador do Centro de Treinamento')]