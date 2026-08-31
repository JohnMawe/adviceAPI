from pydantic import BaseModel, ConfigDict, field_validator

class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    author_id: int
    first_name: str
    second_name: str

class AuthorValidator(BaseModel):
    first_name: str
    second_name: str

    @field_validator('first_name', 'second_name')
    @classmethod
    def validate_author(cls, value):
        if len(value.strip()) <= 0:
            raise ValueError("Advice cannot be empty")
        return value.strip().lower()

