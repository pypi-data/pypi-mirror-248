from pydantic import BaseModel


class CompanyVerificationInputVariables(BaseModel):
    company_id: str
    company_inn: str
    user_id: str
