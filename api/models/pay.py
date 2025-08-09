from pydantic import BaseModel, Field

class PayRequest(BaseModel):
    products: list

class PayResponse(BaseModel):
    url: str = Field(..., description="Payment link.")