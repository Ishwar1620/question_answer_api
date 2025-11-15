from pydantic import BaseModel, Field, field_validator


class QuestionRequest(BaseModel):
    """Request schema for question submission."""
    
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="The question to be answered"
    )
    
    @field_validator("question")
    @classmethod
    def validate_question(cls, v: str) -> str:
        """Validate question input."""
        v = v.strip()
        if not v:
            raise ValueError("Question cannot be empty")
        if len(v) < 3:
            raise ValueError("Question must be at least 3 characters long")
        if len(v) > 1000:
            raise ValueError("Question must be less than 1000 characters")
        return v


class AnswerResponse(BaseModel):
    """Response schema for answer."""
    
    answer: str = Field(
        ...,
        description="The answer to the question"
    )



