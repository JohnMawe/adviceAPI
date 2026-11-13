from pydantic import BaseModel, ConfigDict, field_validator

class AdviceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    advice_id: int
    author_id: int
    advice: str

class AdviceValidator(BaseModel):
    author_id: int
    advice: str

    @field_validator('advice')
    @classmethod
    def validate_advice(cls, value):
        if not value.strip():
            raise ValueError("Advice cannot be empty")

        return value.lower()

class AdviceDelete(BaseModel):
    author_id: int


