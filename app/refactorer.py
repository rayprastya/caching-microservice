from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from .models import Payload
from .schemas import PayloadInput
from typing import List

# Simulated transformer function
def transformer_function(input_string: str) -> str:
    return input_string.upper()

# Function to interleave two lists
def interleave_lists(list1: List[str], list2: List[str]) -> List[str]:
    interleaved_list = []
    for item1, item2 in zip(list1, list2):
        interleaved_list.append(item1)
        interleaved_list.append(item2)
    return interleaved_list

# Function to get or create a payload
def get_or_create_payload(session: Session, payload_input: PayloadInput) -> tuple[str, str]:
    list_1 = payload_input.list_1
    list_2 = payload_input.list_2
    
    if len(list_1) != len(list_2):
        raise ValueError("Both lists must be of the same length")
    
    transformed_1 = [transformer_function(item) for item in list_1]
    transformed_2 = [transformer_function(item) for item in list_2]
    
    interleaved_output = ', '.join(interleave_lists(transformed_1, transformed_2))
    
    try:
        payload = session.query(Payload).filter(
            Payload.input_list_1 == ','.join(list_1),
            Payload.input_list_2 == ','.join(list_2)
        ).one()
    except NoResultFound:
        payload_id = str(uuid4())
        payload = Payload(
            id=payload_id,
            input_list_1=','.join(list_1),
            input_list_2=','.join(list_2),
            output=interleaved_output
        )
        session.add(payload)
        session.commit()
        return payload_id, interleaved_output
    
    return str(payload.id), payload.output
