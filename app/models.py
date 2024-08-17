from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base

# Define the Payload model
class Payload(Base):
    __tablename__ = "payloads"

    # Columns for the Payload table
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_list_1 = Column(String, nullable=False)
    input_list_2 = Column(String, nullable=False)
    output = Column(String, nullable=False)
