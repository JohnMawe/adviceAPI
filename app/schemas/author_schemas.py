from pydantic import BaseModel, ConfigDict, field_validator

class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    author_id: int
    first_name: str
    second_name: str

class AuthorValidator(BaseModel):
    first_name: str
    second_name: str

    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls, value: str):
        if not value.strip():
            raise ValueError("First name cannot be empty")

        return value

    @field_validator('second_name')
    @classmethod
    def validate_second_name(cls, value: str):
        if not value.strip():
            raise ValueError("Second name cannot be empty")

        return value

