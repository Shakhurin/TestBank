from src.main.api.models.base_model import BaseModel


class RequestCreditRequest(BaseModel):
    accountId: int
    amount: float
    termMonths: int