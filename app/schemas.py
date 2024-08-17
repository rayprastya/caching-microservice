from pydantic import BaseModel

# Schema for input data
class PayloadInput(BaseModel):
    list_1: list[str]
    list_2: list[str]

# Schema for output data
class PayloadOutput(BaseModel):
    id: str
    output: str
