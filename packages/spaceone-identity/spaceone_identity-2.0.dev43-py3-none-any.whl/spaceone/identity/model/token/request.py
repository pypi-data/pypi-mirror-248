from typing import Union, Literal
from pydantic import BaseModel

__all__: ["TokenIssueRequest"]

AuthType = Literal["LOCAL", "EXTERNAL"]
GrantType = Literal["API_KEY", "REFRESH_TOKEN"]
Scope = Literal["SYSTEM", "DOMAIN", "WORKSPACE", "USER"]


class TokenIssueRequest(BaseModel):
    credentials: dict
    auth_type: AuthType
    timeout: Union[int, None] = None
    verify_code: Union[str, None] = None
    domain_id: str


class TokenGrantRequest(BaseModel):
    grant_type: str
    token: str
    scope: Scope
    timeout: Union[int, None] = None
    workspace_id: Union[str, None] = None
