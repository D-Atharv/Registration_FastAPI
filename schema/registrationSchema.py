from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    eventId: int
    studentId: int
